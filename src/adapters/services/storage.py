import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import perf_counter
from typing import Generator, TypeVar

import botocore.exceptions
from botocore.client import BaseClient
from pyspark.sql import SparkSession

from src.configurator.config import (
    ALLOWED_FILE_FORMATS,
    MULTITHREADING_WORKER_SIZE,
)
from src.domain.ports.services.exceptions import (
    DownloadFileFromS3Error,
    ListingObjectsFromS3Error,
)
from src.domain.ports.services.storage import StorageServiceInterface
from src.domain.ports.tools.loggers.logger import LoggerInterface

T = TypeVar('T')


class S3StorageService(StorageServiceInterface):
    def __init__(
        self,
        s3_client: BaseClient,
        logger: LoggerInterface,
        spark: SparkSession,
        bucket_name: str,
        catalogs: list,
    ):
        self.s3_client = s3_client
        self.logger = logger
        self.spark = spark
        self.bucket_name = bucket_name
        self.catalogs = catalogs

    def list_objects(
        self, prefix: str, max_objects: int = None
    ) -> Generator[T, None, None]:
        """
        Lists objects in an S3 bucket with a specified prefix (catalog).

        :param prefix: The prefix of the object keys to list.
        :param max_objects: Maximum number of objects to list. Defaults to None.
        :yields: Generator[T, None, None]: Yields object keys that match the prefix and allowed file formats.
        """
        continuation_token = None
        objects_yielded = 0
        response = {}

        while True:
            params = {'Bucket': self.bucket_name, 'Prefix': prefix}
            if continuation_token:
                params['ContinuationToken'] = continuation_token

            try:
                response = self.s3_client.list_objects_v2(**params)
            except ListingObjectsFromS3Error as e:
                self.logger.log_exception(
                    f'Error listing objects with prefix {prefix}: {e}'
                )

            if 'Contents' in response:
                for obj in response['Contents']:
                    if any(obj['Key'].endswith(ext) for ext in ALLOWED_FILE_FORMATS):
                        yield obj['Key']
                        objects_yielded += 1
                    if max_objects is not None and objects_yielded == max_objects:
                        return

            if not response.get('IsTruncated'):
                break

            continuation_token = response.get('NextContinuationToken')

    def list_folders(self) -> list:
        """
        Lists catalog names from s3 bucket

        :return: list of catalog names
        """
        paginator = self.s3_client.get_paginator('list_objects_v2')
        result = paginator.paginate(Bucket=self.bucket_name, Delimiter='/')

        return [prefix.get('Prefix') for prefix in result.search('CommonPrefixes')]

    def download_file(self, key: str, local_folder_path: str):
        """
        Downloads a file from S3 to a local folder.

        :param key: key in s3 bucket
        :param local_folder_path:
        :return:
        """
        try:
            file_name = key.split('/')[-1]
            local_file_path = os.path.join(local_folder_path, file_name)

            if os.path.exists(local_file_path):
                self.logger.log_info(
                    f'Skipping download. File {file_name} already exists in {local_folder_path}'
                )
                return

            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

            self.s3_client.download_file(self.bucket_name, key, local_file_path)
            self.logger.log_info(f'Downloaded {file_name} to {local_folder_path}')

        except botocore.exceptions.ClientError as e:
            self.logger.log_exception(f'Failed to download {key} from S3: {e}')
        except DownloadFileFromS3Error as e:
            self.logger.log_exception(f'Unexpected error during download of {key}: {e}')

    def _download_catalog_files(
        self, catalog: Generator[T, None, None], download_folder: str
    ):
        """
        Downloads files from a given catalog if their extensions are in the allowed formats.

        :param catalog: (Generator[T, None, None]): A generator yielding file keys to be downloaded.
        :param download_folder: The folder where the downloaded files will be saved.
        """
        start = perf_counter()
        futures = []

        with ThreadPoolExecutor(max_workers=MULTITHREADING_WORKER_SIZE) as executor:
            for key in catalog:
                if any(key.endswith(ext) for ext in ALLOWED_FILE_FORMATS):
                    future = executor.submit(self.download_file, key, download_folder)
                    futures.append(future)

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                self.logger.log_info(f'Download failed: {e}')

        end = perf_counter()

        self.logger.log_info(
            f'It took {end - start} seconds to download {len(futures)} files'
        )

    def _download_files(self, count: int, download_folder: str) -> None:
        """
        Initiates the download of files from multiple catalogs.
        Uses the _download_catalog_files method to handle the download for each catalog.

        :param count: The number of files to list from each catalog.
        :param download_folder: The folder where the downloaded files will be saved.
        """
        start = perf_counter()
        total_files = 0

        try:
            for catalog in self.catalogs:
                generator = self.list_objects(catalog, count)
                self._download_catalog_files(generator, download_folder)
                total_files += count
        except Exception as e:
            self.logger.log_exception(f'Error downloading files: {e}')
        finally:
            end = perf_counter()
            self.logger.log_info(
                f'Download completed in {end - start:.2f} seconds. '
                f'Total files downloaded: {total_files}'
            )

    def _download_files_with_spark(self, count: int, download_folder: str):
        for catalog in self.catalogs:
            generator = self.list_objects(catalog, count)
            self.worker_handler(generator, download_folder)

    def worker_handler(self, key_gen, download_folder):
        with self.spark as spark:
            sc = spark.sparkContext
            download_folder_bc = sc.broadcast(download_folder)

            file_keys_rdd = sc.parallelize(key_gen)

            def download_file_worker(key_arg):
                self.download_file(
                    key=key_arg, local_folder_path=download_folder_bc.value
                )

            file_keys_rdd.foreach(download_file_worker)
