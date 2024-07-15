from time import perf_counter

from pyspark.sql import SparkSession

from src.configurator.config import (
    postgresql_connection_properties,
    postgresql_jdbc_url,
)
from src.domain.ports.repositories.metadata import MetadataRepositoryInterface
from src.domain.ports.services.exceptions import MetadataPersistenceError
from src.domain.ports.tools.loggers.logger import LoggerInterface


class MetadataRepository(MetadataRepositoryInterface):
    """Postgresql Repository for Metadata"""

    def __init__(self, logger: LoggerInterface, spark: SparkSession) -> None:
        self.logger = logger
        self.spark = spark

    def _add(self, metadata_df) -> None:
        """
        Adds new metadata to the database, avoiding duplicates based on the 'hash' column.

        :param metadata_df:
        :return:
        """
        start = perf_counter()
        try:
            tablename = postgresql_connection_properties.get('table')

            with self.spark as spark:
                existing_ids = spark.read.jdbc(
                    url=postgresql_jdbc_url,
                    table=tablename,
                    properties=postgresql_connection_properties,
                ).select('hash')

            metadata_df = metadata_df.join(existing_ids, 'hash', 'leftanti')
            new_records_count = metadata_df.count()

            if new_records_count:
                metadata_df.write.format('jdbc').option(
                    'url', postgresql_jdbc_url
                ).option('dbtable', 'metadata').option(
                    'user', postgresql_connection_properties.get('user')
                ).option(
                    'password', postgresql_connection_properties.get('password')
                ).option('driver', postgresql_connection_properties.get('driver')).mode(
                    'append'
                ).save()

                self.logger.log_info(
                    f'Added {new_records_count} new records to the {tablename} table.'
                )
            else:
                self.logger.log_info('No new records to add.')
        except MetadataPersistenceError as e:
            self.logger.log_info(f'An error occurred while adding metadata: {e}')
        finally:
            end = perf_counter()
            self.logger.log_info(
                f'Metadata persistence completed in {end - start:.2f} seconds.'
            )

    def _get_by_uuid(self, uuid: str):
        pass
