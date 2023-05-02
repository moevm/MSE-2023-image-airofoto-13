from typing import Callable, Any

from .parser_base import IParser


class Parser(IParser):

    """
    Parser class to handle input/output from custom file formats.
    """

    def __init__(
        self,
        file_format: str,
        reader: Callable[[str], Any],
        writer: Callable[[str, Any], None],
    ):

        """
        Constructor method for Parser class.

        :param file_format: supported file format name.
        :param reader: function, providing data extraction from file.
        :param writer: function, providing data output to the file.
        """

        self.__file_format = file_format
        self._reader = reader
        self._writer = writer

    def supported_format(self) -> str:
        return self.__file_format

    def file_input(self, file_path: str) -> Any:
        return self._reader(file_path)

    def file_output(self, file_path: str, data: Any) -> None:
        self._writer(file_path, data)
