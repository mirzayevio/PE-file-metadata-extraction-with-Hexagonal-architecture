from dependency_injector import containers, providers

from src.adapters.entrypoints.cli.controllers.metadata import MetadataController
from src.adapters.repositories.metadata import MetadataRepository
from src.adapters.services.metadata import MetadataService
from src.adapters.services.storage import S3StorageService

from ..adapters.services.metadata_extraction import MetadataExtractionService
from ..adapters.tools.loggers.default_logger import LoggerDefault
from .config import BUCKET_NAME, CATALOGS, LOGS_FOLDER, get_s3_client, get_spark_session


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    logger = providers.Singleton(LoggerDefault, folder_path=LOGS_FOLDER)
    s3_client = providers.Singleton(get_s3_client)
    spark = providers.Factory(get_spark_session)

    metadata_repository = providers.Singleton(
        MetadataRepository, logger=logger, spark=spark
    )

    storage_service = providers.Singleton(
        S3StorageService,
        s3_client=s3_client,
        logger=logger,
        spark=spark,
        bucket_name=config.bucket_name,
        catalogs=config.catalogs,
    )

    metadata_service = providers.Factory(
        MetadataService, logger=logger, repository=metadata_repository
    )

    metadata_extraction_service = providers.Factory(
        MetadataExtractionService, logger=logger, spark=spark
    )

    metadata_cli_controller = providers.Factory(
        MetadataController,
        logger=logger,
        storage_service=storage_service,
        metadata_extraction_service=metadata_extraction_service,
        metadata_service=metadata_service,
        spark=spark,
    )


container = Container()
container.config.bucket_name.from_value(BUCKET_NAME)
container.config.catalogs.from_value(CATALOGS)
