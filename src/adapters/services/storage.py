import os

import boto3
from botocore import UNSIGNED
from botocore.client import BaseClient
from botocore.config import Config

from src.domain.ports.services.storage import StorageServiceInterface


class S3StorageService(StorageServiceInterface):
    def __init__(self, bucket_name: str, download_folder: str, catalogs: list[str]):
        self.bucket_name = bucket_name
        self.download_folder = download_folder
        self.catalogs = catalogs
        self.s3_client: BaseClient = boto3.client(
            's3', config=Config(signature_version=UNSIGNED)
        )

    def list_objects(self, prefix: str, max_objects=None):
        continuation_token = None
        objects_yielded = 0

        while True:
            params = {'Bucket': self.bucket_name, 'Prefix': prefix}
            if continuation_token:
                params['ContinuationToken'] = continuation_token

            response = self.s3_client.list_objects_v2(**params)

            if 'Contents' in response:
                for obj in response['Contents']:
                    yield obj['Key']

                    objects_yielded += 1

                    if max_objects is not None and objects_yielded == max_objects:
                        return

            if not response.get('IsTruncated'):
                break

            continuation_token = response['NextContinuationToken']

    def list_folders(self) -> list[str]:
        paginator = self.s3_client.get_paginator('list_objects_v2')
        result = paginator.paginate(Bucket=self.bucket_name, Delimiter='/')

        return [prefix.get('Prefix') for prefix in result.search('CommonPrefixes')]

    def _download_file(self, key: str):
        file_name = key.split('/')[-1]
        local_file_path = os.path.join(self.download_folder, file_name)
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        self.s3_client.download_file(self.bucket_name, key, local_file_path)

        print(f'Downloaded {file_name}')
