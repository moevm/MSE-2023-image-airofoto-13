from abc import abstractmethod, ABC
from typing import Any


class IParser(ABC):

    """
    Interface for file Parser classes. Declares the methods to read/write files and helper methods to easily create
    a Parser object and check the file format supported by the specific Parser.

    Parsers are building blocks for the FileManager, responsible for handling any file operation.
    """

    @classmethod
    @abstractmethod
    def create_parser(cls) -> "IParser":

        """
        A factory method for easy creation of parser objects.
        Needs to be overriden for each derived Parser class.

        :return: A specific Parser object.
        """

    @abstractmethod
    def supported_format(self) -> str:

        """
        Helper method, allowing to determine supported file formats.

        :return: A specific Parser's supported format.
        """

    @abstractmethod
    def file_input(self, file_path: str) -> Any:

        """
        Method to read from file along the given path.

        :raises: ValueError if the file type is not supported or if the file doesn't exist.

        :param file_path: - Path to the file to read data from.
        :return: Data from the given file.
        """

    @abstractmethod
    def file_output(self, file_path: str, data: Any) -> None:
        """
        Method to write to the file along the given path.

        Does not raise errors in assumption that desired file is accessible.

        :param file_path: Path to the file to write to.
        :param data: Data to write ti file.
        :return: None.
        """
