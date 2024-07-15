from abc import ABC

from src.domain.ports.repositories.metadata import MetadataRepositoryInterface
from src.domain.ports.services.metadata import MetadataServiceInterface
from src.domain.ports.tools.loggers.logger import LoggerInterface


class MetadataService(MetadataServiceInterface, ABC):
    def __init__(
        self, logger: LoggerInterface, repository: MetadataRepositoryInterface
    ) -> None:
        self.logger = logger
        self.repository = repository

    def _create(self, metadata_df):
        self.repository.add(metadata_df)

    def _get_metadata_by_uuid(self, uuid: str):
        pass
