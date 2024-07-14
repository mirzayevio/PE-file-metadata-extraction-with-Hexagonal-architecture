import os
from abc import ABC

import pefile
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    FloatType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

from src.configurator.config import DOWNLOAD_FOLDER, SPARK_FILES_FOLDER, Status
from src.domain.ports.services.metadata_extraction import (
    MetadataExtractionServiceInterface,
)


class MetadataExtractionService(MetadataExtractionServiceInterface, ABC):
    def __init__(self, spark: SparkSession) -> None:
        self.spark = spark

    def _extract(self, current_batch_folder_name: str):
        file_names = os.listdir(
            os.path.join(DOWNLOAD_FOLDER, current_batch_folder_name)
        )

        spark_folder_path = os.path.join(SPARK_FILES_FOLDER, current_batch_folder_name)
        file_paths = [os.path.join(spark_folder_path, i) for i in file_names]

        with self.spark as spark:
            sc = spark.sparkContext

            file_keys_rdd = sc.parallelize(file_paths)
            metadata_rdd = file_keys_rdd.mapPartitions(self.process_partition)

            # Define the schema for your metadata
            schema = StructType(
                [
                    StructField('file_path', StringType(), True),
                    StructField('file_type', StringType(), True),
                    StructField('file_size', FloatType(), True),
                    StructField('architecture', StringType(), True),
                    StructField('num_of_imports', IntegerType(), True),
                    StructField('num_of_exports', IntegerType(), True),
                    StructField('status', StringType(), True),
                    StructField('error', StringType(), True),
                ]
            )

            metadata_df = spark.createDataFrame(metadata_rdd, schema)

            metadata_df.show()

    @staticmethod
    def get_metadata(file_path):
        result = {
            'file_path': file_path,
            'file_type': '',
            'file_size': 0.0,
            'architecture': '',
            'num_of_imports': 0,
            'num_of_exports': 0,
            'status': Status.FAIL.value,
            'error': '',
        }
        if not os.path.isfile(file_path):
            print(f'The file {file_path} does not exist.')
            result['error'] = 'file does not exist.'
            return result

        if not MetadataExtractionService.is_pe_file(file_path):
            print(
                f"The file {file_path} is not a valid PE file (missing 'MZ' signature)."
            )
            result['error'] = "not a valid PE file (missing 'MZ' signature)."
            return result

        try:
            with pefile.PE(file_path, fast_load=True) as pe:
                pe.parse_data_directories(
                    directories=[
                        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],
                        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT'],
                    ]
                )

                file_size_bytes = os.path.getsize(file_path)
                file_size = file_size_bytes / (1024 * 1024)
                file_type = 'DLL' if pe.is_dll() else 'EXE'
                architecture = (
                    'x64'
                    if pe.PE_TYPE == pefile.OPTIONAL_HEADER_MAGIC_PE_PLUS
                    else 'x32'
                )

                import_count = (
                    sum(len(entry.imports) for entry in pe.DIRECTORY_ENTRY_IMPORT)
                    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT')
                    else 0
                )

                export_count = (
                    len(pe.DIRECTORY_ENTRY_EXPORT.symbols)
                    if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT')
                    else 0
                )

                return {
                    'file_path': file_path,
                    'file_type': file_type,
                    'file_size': file_size,
                    'architecture': architecture,
                    'num_of_imports': import_count,
                    'num_of_exports': export_count,
                    'status': Status.SUCCESS.value,
                    'error': '',
                }

        except pefile.PEFormatError as e:
            result['error'] = f'pefile.PEFormatError {e}'

        except Exception as e:
            result['error'] = f'An error occurred {e}'

        return result

    @staticmethod
    def is_pe_file(file_path):
        try:
            with open(file_path, 'rb') as f:
                magic = f.read(2)
            return magic == b'MZ'
        except Exception as e:
            print(f'Error reading file {file_path}: {e}')
            return False

    @staticmethod
    def process_partition(iterator):
        return [
            metadata
            for metadata in (
                MetadataExtractionService.get_metadata(file_path)
                for file_path in iterator
            )
            if metadata is not None
        ]
