from dependency_injector import containers, providers

from src.adapters.entrypoints.cli.controllers.metadata import MetadataController
from src.adapters.repositories.metadata import MetadataRepository
from src.adapters.services.metadata import MetadataService
from src.adapters.services.storage import S3StorageService

from ..adapters.tools.loggers.default_logger import LoggerDefault
from .config import BUCKET_NAME, CATALOGS, Session, get_s3_client


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    logger = providers.Singleton(LoggerDefault)
    s3_client = providers.Singleton(get_s3_client)

    storage_service = providers.Singleton(
        S3StorageService,
        s3_client=s3_client,
        logger=logger,
        bucket_name=config.bucket_name,
        catalogs=config.catalogs,
    )

    metadata_repository = providers.Singleton(
        MetadataRepository, session=config.session
    )
    metadata_service = providers.Factory(
        MetadataService, repository=metadata_repository
    )

    metadata_cli_controller = providers.Factory(
        MetadataController,
        logger=logger,
        storage_service=storage_service,
        metadata_service=metadata_service,
    )


container = Container()
container.config.bucket_name.from_value(BUCKET_NAME)
container.config.catalogs.from_value(CATALOGS)
container.config.session.from_value(Session)
