class FileExtensionValidator:
    valid_extensions: set[str] = {'exe', 'dll'}

    @classmethod
    def update_valid_extensions(cls, extensions: set[str]):
        cls.valid_extensions = extensions
