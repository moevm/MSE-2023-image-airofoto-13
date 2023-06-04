from typing import Callable, Any, List, IO
import open3d as o3d  # type: ignore
import yaml

from .parser_base import IParserFactory
from .parser import Parser


#   Compatability wrappers for Parser creation with functions requiring file stream for file access.

def read_stream(function: Callable[[IO[str]], Any]) -> Callable[[str], Any]:

    """
    Parser compatability wrapper for input stream dependent functions.

    :param function: input function, requiring file stream.
    :return: wrapped Parser compatible function
    """

    def wrapper(path: str) -> Any:

        with open(path, "r") as source:
            data = function(source)

        return data

    return wrapper


def write_stream(
    function: Callable[[IO[str], Any], None]
) -> Callable[[str, Any], None]:

    """
    Parser compatability wrapper for output stream dependent functions.

    :param function: output function, requiring file stream.
    :return: wrapped Parser compatible function
    """

    def wrapper(path: str, data: Any) -> None:

        with open(path, "w") as source:
            function(source, data)

    return wrapper


# typing args/kwargs in typing.Callable is weird, so for now the simpler solution is in place.
def yml_write_wo_sorting(stream: Any, data: Any) -> None:
    """
    A function wrapper redefining the standard yaml dump function,
    preventing int from sorting dictionary keys.

    :param stream: IO stream to file.
    :param data: sequence to be dumped into .yml file.
    :return: None
    """

    yaml.safe_dump(data, stream, sort_keys=False)


#-----------------------------------------------------------------------------------------------------------------------


class ParserFactory(IParserFactory):

    _parsers = {
        "ply" : [o3d.io.read_point_cloud, o3d.io.write_point_cloud],
        "yml": [read_stream(yaml.safe_load), write_stream(yml_write_wo_sorting)]
    }

    @staticmethod
    def get_supported() -> List[str]:
        return list(ParserFactory._parsers.keys())

    @staticmethod
    def create(
        name: str, reader: Callable[[str], Any], writer: Callable[[str, Any], None]
    ) -> Parser:

        return Parser(file_format=name, reader=reader, writer=writer)

    @staticmethod
    def create_yml() -> Parser:
        """
        Returns a .yml file oriented Parser instance.

        Note: Writing method is modified with a wrapper to prevent dictionary keys from being sorted.

        :return: Parser
        """

        return ParserFactory.create(
            "yml", ParserFactory._parsers["yml"][0], ParserFactory._parsers["yml"][1]
        )

    @staticmethod
    def create_ply() -> Parser:
        return ParserFactory.create(
            "ply", ParserFactory._parsers["ply"][0], ParserFactory._parsers["ply"][1]
        )

    @staticmethod
    def __getitem__(self, item: str) -> Parser:

        if item not in ParserFactory._parsers:
            raise KeyError(f"{item} is not supported!")

        return Parser(
            item,
            ParserFactory._parsers[item][0],
            ParserFactory._parsers[item][1]
        )
