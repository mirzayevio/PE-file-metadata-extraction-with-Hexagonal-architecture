import os
from datetime import datetime

from pyspark.sql import SparkSession

from src.configurator.config import DOWNLOAD_FOLDER
from src.domain.ports.services.metadata import MetadataServiceInterface
from src.domain.ports.services.metadata_extraction import (
    MetadataExtractionServiceInterface,
)
from src.domain.ports.services.storage import StorageServiceInterface
from src.domain.ports.tools.loggers.logger import LoggerInterface


class MetadataController:
    def __init__(
        self,
        logger: LoggerInterface,
        storage_service: StorageServiceInterface,
        metadata_extraction_service: MetadataExtractionServiceInterface,
        metadata_service: MetadataServiceInterface,
        spark: SparkSession,
    ):
        self.logger = logger
        self.storage_service = storage_service
        self.metadata_extraction_service = metadata_extraction_service
        self.metadata_service = metadata_service
        self.spark = spark

    def execute(self, task_size: int):
        """
        Executes the task by downloading files and extracting metadata.

        :param task_size:
        :return:
        """

        current_batch_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        current_batch_folder = os.path.join(DOWNLOAD_FOLDER, current_batch_timestamp)

        self.storage_service.download_files(task_size, current_batch_folder)
        metadata_df = self.metadata_extraction_service.extract(current_batch_timestamp)

        self.metadata_service.create(metadata_df)
