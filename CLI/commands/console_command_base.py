from abc import abstractmethod, ABC
from typing import Any, Dict, Callable
from inspect import Signature

from click import Command, Context

from managers import PluginInfo


class IConsoleCommandFactory(ABC):

    """
    Interface for CLI Command serialization Factory.
    """

    @abstractmethod
    def kwargs_save_callback(self, name: str) -> Callable[[Context, Any], None]:

        """
        Automatically generates callback for command to save data.

        :param name: Name of the command
        :return: save-data callback
        """

        pass

    @abstractmethod
    def create_from_info(self, data: PluginInfo) -> Command:
        """
        Creates CLI representation for given plugin, based on the information provided in PluginInfo instance.
        Primary method for generating CLI commands.

        :param data: PluginInfo instance

        :return: click.Command
        """

        pass

    @abstractmethod
    def create_from_function(self, executable: Callable[[Any], Any]) -> Command:

        """
        Creates a CLI representation for given function.

        :param executable: Callable object to represent in CLI.
        :return: click.Command instance, representing the object.
        """

        pass

    @abstractmethod
    def create_from_signature(
        self, name: str, help_msg: str, arguments: Signature
    ) -> Command:

        """
        Generates the CLI command from given Signature object.

        :param name: Name of the function.
        :param help_msg: --help message. (Usually the doc_string of the function).
        :param arguments: Signature object
        :return: click.Command instance.
        """

        pass
