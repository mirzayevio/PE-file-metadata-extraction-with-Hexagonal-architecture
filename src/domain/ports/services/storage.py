from abc import ABC, abstractmethod


class StorageServiceInterface(ABC):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    def download_files(self, count: int) -> None:
        return self._download_files(count)

    @abstractmethod
    def _download_files(self, count: int) -> None:
        raise NotImplementedError
