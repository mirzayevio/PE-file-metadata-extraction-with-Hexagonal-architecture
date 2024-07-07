from dependency_injector import containers, providers

from src.adapters.entrypoints.cli.controllers.metadata import MetadataController
from src.adapters.repositories.metadata import MetadataRepository
from src.adapters.services.metadata import MetadataService
from src.adapters.services.storage import S3StorageService

from ..adapters.tools.loggers.default_logger import LoggerDefault
from .config import BUCKET_NAME, CATALOGS, DOWNLOAD_FOLDER, Session


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    storage_service = providers.Singleton(
        S3StorageService,
        bucket_name=config.bucket_name,
        download_folder=config.download_folder,
        catalogs=config.catalogs,
    )
    metadata_repository = providers.Singleton(
        MetadataRepository, session=config.session
    )
    metadata_service = providers.Factory(
        MetadataService, repository=metadata_repository
    )

    logger = providers.Singleton(LoggerDefault)

    metadata_cli_controller = providers.Factory(
        MetadataController,
        logger=logger,
        storage_service=storage_service,
        metadata_service=metadata_service,
    )


container = Container()
container.config.bucket_name.from_value(BUCKET_NAME)
container.config.download_folder.from_value(DOWNLOAD_FOLDER)
container.config.catalogs.from_value(CATALOGS)
container.config.session.from_value(Session)
