from abc import ABC

from src.domain.entities.metadata import Metadata
from src.domain.ports.repositories.metadata import MetadataRepositoryInterface


class MetadataRepository(MetadataRepositoryInterface, ABC):
    """Postgresql Repository for Metadata"""

    def __init__(self) -> None:
        super().__init__()

    def _add(self, metadata: Metadata) -> None:
        pass

    def _get_by_uuid(self, uuid: str) -> Metadata:
        pass
