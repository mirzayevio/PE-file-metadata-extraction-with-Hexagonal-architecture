from abc import ABC, abstractmethod


class MetadataExtractionServiceInterface(ABC):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    def extract(self, folder_name: str):
        return self._extract(folder_name)

    @abstractmethod
    def _extract(self, folder_name: str):
        raise NotImplementedError
