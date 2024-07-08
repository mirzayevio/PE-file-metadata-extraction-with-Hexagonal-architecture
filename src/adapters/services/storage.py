import os

from botocore.client import BaseClient

from src.domain.ports.services.storage import StorageServiceInterface
from src.domain.ports.tools.loggers.logger import LoggerInterface


class S3StorageService(StorageServiceInterface):
    def __init__(
        self,
        s3_client: BaseClient,
        logger: LoggerInterface,
        bucket_name: str,
        download_folder: str,
        catalogs: list[str],
    ):
        self.logger = logger
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.download_folder = download_folder
        self.catalogs = catalogs

    def list_objects(self, prefix: str, max_objects: int = None):
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
                    yield obj['Key']

                    objects_yielded += 1
                    if max_objects is not None and objects_yielded == max_objects:
                        return

            if not response.get('IsTruncated'):
                break

            continuation_token = response.get('NextContinuationToken')

    def list_folders(self) -> list[str]:
        paginator = self.s3_client.get_paginator('list_objects_v2')
        result = paginator.paginate(Bucket=self.bucket_name, Delimiter='/')

        return [prefix.get('Prefix') for prefix in result.search('CommonPrefixes')]

    def download_file(self, key: str):
        file_name = key.split('/')[-1]
        local_file_path = os.path.join(self.download_folder, file_name)
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        self.s3_client.download_file(self.bucket_name, key, local_file_path)

        self.logger.log_info(f'Downloaded {file_name}')

    def _download_files(self, count: int) -> None:
        for catalog in self.catalogs:
            for key in self.list_objects(catalog, count):
                self.download_file(key)
