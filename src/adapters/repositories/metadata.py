from abc import ABC
from typing import Optional

from src.domain.entities.metadata import Metadata
from src.domain.ports.repositories.metadata import MetadataRepositoryInterface


class MetadataRepository(MetadataRepositoryInterface, ABC):
    """Postgresql Repository for Metadata"""

    def __init__(self, session) -> None:
        super().__init__()
        self.session = session

    def _add(self, metadata: Metadata) -> None:
        pass

    def _get_by_uuid(self, uuid: str) -> Metadata:
        pass

    def _get_all(self) -> Optional[list[Metadata]]:
        pass
