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
        self.storage_service.download_files(task_size)
