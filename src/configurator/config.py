import os
from contextlib import contextmanager
from enum import Enum
from typing import Union

import boto3
import yaml
from botocore import UNSIGNED
from botocore.client import BaseClient
from botocore.config import Config
from dotenv import load_dotenv
from pyspark.sql import SparkSession

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')


def get_s3_client() -> BaseClient:
    return boto3.client('s3', config=Config(signature_version=UNSIGNED))


def get_spark_session() -> SparkSession:
    return spark_session(SPARK_CONFIG)


@contextmanager
def spark_session(config_path: Union[str, os.PathLike]):
    if not (config_path.endswith('.yaml') or config_path.endswith('.yml')):
        raise ValueError(
            'The provided file is not a YAML file. Please provide a file with a .yaml or .yml extension.'
        )

    if not os.path.isfile(config_path):
        raise FileNotFoundError(f'The file {config_path} does not exist.')

    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    os.environ['PYSPARK_PYTHON'] = config['pyspark_python']

    builder = SparkSession.builder.appName(config['spark']['app_name']).master(
        config['spark']['master']
    )

    for key, value in config['spark']['config'].items():
        builder = builder.config(key, value)

    spark = builder.getOrCreate()

    for py_file in config['spark']['py_files']:
        spark.sparkContext.addPyFile(py_file)

    try:
        yield spark
    finally:
        spark.stop()


BUCKET_NAME = 's3-nord-challenge-data'
CATALOGS = ('0/',)
ALLOWED_FILE_FORMATS = ('exe', 'dll')


class Status(str, Enum):
    SUCCESS = 'success'
    FAIL = 'fail'


# Folders setup
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

DOWNLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'downloads')
LOGS_FOLDER = os.path.join(PROJECT_ROOT, 'logs')
SPARK_CONFIG = os.path.join(PROJECT_ROOT, 'spark_config.yaml')
SPARK_FILES_FOLDER = '/opt/spark/data'
