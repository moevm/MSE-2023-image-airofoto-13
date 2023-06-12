from abc import ABC, abstractmethod
from typing import Any, Callable, List


class IParser(ABC):

    """
    Interface for file Parser classes. Declares the methods to read/write files and helper methods to easily create
    a Parser object and check the file format supported by the specific Parser.

    Parsers are building blocks for the FileManager, responsible for handling any file operation.
    """

    @abstractmethod
    def supported_format(self) -> str:

        """
        Helper method, allowing to determine supported file formats.

        :return: A specific Parser's supported format.
        """

        pass

    @abstractmethod
    def file_input(self, file_path: str) -> Any:

        """
        Method to read from file along the given path.

        :raises: ValueError if the file type is not supported or if the file doesn't exist.

        :param file_path: - Path to the file to read data from.
        :return: Data from the given file.
        """

        pass

    @abstractmethod
    def file_output(self, file_path: str, data: Any) -> None:
        """
        Method to write to the file along the given path.

        Does not raise errors in assumption that desired file is accessible.

        :param file_path: Path to the file to write to.
        :param data: Data to write ti file.
        :return: None.
        """

        pass


class IParserFactory(ABC):

    """
    A Factory class for IParser instances.
    """

    @staticmethod
    @abstractmethod
    def get_supported() -> List[str]:
        """
        Returns a list of supported file-formats (
        """
        pass

    @staticmethod
    @abstractmethod
    def create(
        name: str, reader: Callable[[str], Any], writer: Callable[[str, Any], None]
    ) -> IParser:
        """
        A factory method for easy creation of parser objects.
        Needs to be overriden for each derived Parser class.

        :param name: file format.
        :param reader: function to read from specified file.
        :param writer: function to write to specified file.

        :return: A configured IParser instance.
        """

        pass

    @staticmethod
    @abstractmethod
    def create_yml() -> IParser:
        """
        Returns a .yml file oriented IParser instance.

        :return: IParser
        """

        pass

    @staticmethod
    @abstractmethod
    def create_ply() -> IParser:
        """
        Returns a .ply file oriented IParser instance.

        :return: IParser
        """

        pass

    @staticmethod
    @abstractmethod
    def __getitem__(item: str) -> IParser:
        pass
