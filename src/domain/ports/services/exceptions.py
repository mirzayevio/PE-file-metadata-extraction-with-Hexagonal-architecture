class MetadataExtractionError(Exception):
    """
    Exception raised for errors that occur during metadata extraction.
    """


class DownloadFileFromS3Error(Exception):
    """
    Exception raised for errors that occur during file download from S3 bucket
    """


class ListingObjectsFromS3Error(Exception):
    """
    Exception raised for errors that occur during listing objects from S3 bucket
    """


class MetadataPersistenceError(Exception):
    """
    Exception raised for errors that occur during saving metadata to table
    """
