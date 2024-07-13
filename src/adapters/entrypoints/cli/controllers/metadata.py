import os
from datetime import datetime

from src.configurator.config import DOWNLOAD_FOLDER
from src.domain.ports.services.metadata import MetadataServiceInterface
from src.domain.ports.services.storage import StorageServiceInterface
from src.domain.ports.tools.loggers.logger import LoggerInterface


class MetadataController:
    def __init__(
        self,
        logger: LoggerInterface,
        storage_service: StorageServiceInterface,
        metadata_service: MetadataServiceInterface,
    ):
        self.logger = logger
        self.storage_service = storage_service
        self.metadata_service = metadata_service

    def execute(self, task_size: int):
        current_batch_folder = os.path.join(
            DOWNLOAD_FOLDER, datetime.now().strftime('%Y%m%d_%H%M%S')
        )
        os.makedirs(current_batch_folder, exist_ok=True)
        self.storage_service.download_files(task_size, current_batch_folder)
        self.metadata_service.extract_metadata(current_batch_folder)
