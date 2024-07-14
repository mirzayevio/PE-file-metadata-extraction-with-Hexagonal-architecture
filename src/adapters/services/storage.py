import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import perf_counter
from typing import Generator, TypeVar

from botocore.client import BaseClient

from src.configurator.config import ALLOWED_FILE_FORMATS
from src.domain.ports.services.storage import StorageServiceInterface
from src.domain.ports.tools.loggers.logger import LoggerInterface

T = TypeVar('T')


class S3StorageService(StorageServiceInterface):
    def __init__(
        self,
        s3_client: BaseClient,
        logger: LoggerInterface,
        bucket_name: str,
        catalogs: list,
    ):
        self.logger = logger
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.catalogs = catalogs

    def list_objects(
        self, prefix: str, max_objects: int = None
    ) -> Generator[T, None, None]:
        continuation_token = None
        objects_yielded = 0
        response = {}

        while True:
            params = {'Bucket': self.bucket_name, 'Prefix': prefix}
            if continuation_token:
                params['ContinuationToken'] = continuation_token

            try:
                response = self.s3_client.list_objects_v2(**params)
            except Exception as e:
                self.logger.log_exception(f'list_objects: {e}')

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
        paginator = self.s3_client.get_paginator('list_objects_v2')
        result = paginator.paginate(Bucket=self.bucket_name, Delimiter='/')

        return [prefix.get('Prefix') for prefix in result.search('CommonPrefixes')]

    def download_file(self, key: str, local_folder_path: str):
        file_name = key.split('/')[-1]
        local_file_path = os.path.join(local_folder_path, file_name)
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        self.s3_client.download_file(self.bucket_name, key, local_file_path)
        self.logger.log_info(f'Downloaded {local_file_path}')

    def _download_catalog_files(
        self, catalog: Generator[T, None, None], download_folder: str
    ):
        start = perf_counter()
        futures = []

        with ThreadPoolExecutor(max_workers=10) as executor:
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
        generators = []
        for catalog in self.catalogs:
            generators.append(self.list_objects(catalog, count))

        for gen in generators:
            self._download_catalog_files(gen, download_folder)
