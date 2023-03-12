from typing import List

from framework import *


class IFileManager(ABC, metaclass=EmbedSingleton):

    """
    Interface for file handler class.
    Declares methods for file existence ensurance, file creation and read/write operations.

    Read/write functionality depends on the provided Parser class objects and the file formats they support.
    """

    @abstractmethod
    def supported_formats(self) -> List[str]:

        """
        Helper method to list all the file formats supported by the specific file handler.

        :return: list of file formats (extensions) supported.
        """

        pass

    @abstractmethod
    def is_supported(self, mode: str) -> bool:

        """
        Helper method to check if the specific file format is supported by the specific file handler.

        :param mode: file extension.
        :return: boolean check result.
        """

        pass

    @abstractmethod
    def path_exists(self, path: str) -> bool:

        """
        Helper method to check if the given path exists in the file system.

        :param path: path to be checked.
        :return: boolean check result.
        """

        pass

    @abstractmethod
    def create_path(self, path: str) -> None:

        """
        Helper method to create missing directories along the given path.

        :param path: path with missing directories.
        :return: None.
        """

        pass

    @abstractmethod
    def read(self, path: str):

        """
        Extract data from file of supported format.

        :raises: ValueError: if file format is not supported or the file doesn't exist.

        :param path: path to file.
        :return: data from file.
        """

        pass

    @abstractmethod
    def write(self, path: str, data: any) -> None:

        """
        Output data to file along the given path. Creates the file if it doesn't exist.

        :param path: path to file.
        :param data: data to write to file.
        :return: None.
        """

        pass
