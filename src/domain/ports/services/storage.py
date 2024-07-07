from abc import ABC, abstractmethod


class StorageServiceInterface(ABC):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    def download_file(self, path: str) -> None:
        return self._download_file(path)

    @abstractmethod
    def _download_file(self, path: str) -> None:
        raise NotImplementedError
