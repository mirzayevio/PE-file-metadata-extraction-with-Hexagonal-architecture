import os
from time import perf_counter

from pyspark.sql import SparkSession
from pyspark.sql.functions import concat, sha2

from src.adapters.tools.utils import get_metadata
from src.configurator.config import DOWNLOAD_FOLDER, SPARK_FILES_FOLDER
from src.domain.ports.services.exceptions import MetadataExtractionError
from src.domain.ports.services.metadata_extraction import (
    MetadataExtractionServiceInterface,
)
from src.domain.ports.tools.loggers.logger import LoggerInterface
from src.domain.schemas import metadata_spark_schema


class MetadataExtractionService(MetadataExtractionServiceInterface):
    def __init__(self, logger: LoggerInterface, spark: SparkSession) -> None:
        self.logger = logger
        self.spark = spark

    def _extract(self, current_batch_folder_name: str):
        """
        Extract metadata and process files from the given batch folder.

        :param current_batch_folder_name:
        :return: RDD: A Spark RDD containing processed metadata.
        :raises:
            FileNotFoundError: If the batch folder doesn't exist.
            Exception: For other unexpected errors during processing.
        """
        start = perf_counter()
        try:
            download_folder_path = os.path.join(
                DOWNLOAD_FOLDER, current_batch_folder_name
            )
            spark_folder_path = os.path.join(
                SPARK_FILES_FOLDER, current_batch_folder_name
            )

            if not os.path.exists(download_folder_path):
                raise FileNotFoundError(
                    f'Batch folder not found: {download_folder_path}'
                )

            file_names = os.listdir(download_folder_path)
            file_paths = [os.path.join(spark_folder_path, i) for i in file_names]

            with self.spark as spark:
                file_keys_rdd = spark.sparkContext.parallelize(file_paths)
                metadata_rdd = file_keys_rdd.map(
                    lambda file_path: get_metadata(file_path)
                )

                metadata_df = spark.createDataFrame(metadata_rdd, metadata_spark_schema)

                metadata_df = metadata_df.withColumn(
                    'hash',
                    sha2(
                        concat(
                            'file_path', 'file_size', 'num_of_imports', 'num_of_exports'
                        ),
                        256,
                    ),
                )

            return metadata_df

        except FileNotFoundError as e:
            self.logger.log_exception(f'Batch folder not found: {e}')
        except MetadataExtractionError as e:
            self.logger.log_exception(f'Error in _extract method: {e}')
        finally:
            end = perf_counter()
            self.logger.log_info(
                f'Metadata extraction completed in {end - start:.2f} seconds.'
            )
