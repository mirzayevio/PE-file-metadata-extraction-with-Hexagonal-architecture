from config import Session
from dependency_injector import containers, providers

from src.adapters.repositories.metadata import MetadataRepository
from src.adapters.services.metadata import MetadataService


class Container(containers.DeclarativeContainer):
    metadata_repository = providers.Singleton(MetadataRepository, session=Session)
    metadata_service = providers.Factory(
        MetadataService, repository=metadata_repository
    )
