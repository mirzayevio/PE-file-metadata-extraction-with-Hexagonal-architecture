from src.configurator.config import ALLOWED_FILE_FORMATS


class FileExtensionValidator:
    valid_extensions = ALLOWED_FILE_FORMATS

    @classmethod
    def update_valid_extensions(cls, extensions):
        cls.valid_extensions = extensions
