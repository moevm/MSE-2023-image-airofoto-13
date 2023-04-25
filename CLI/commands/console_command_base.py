from abc import abstractmethod, ABC
from typing import Any, List, Optional, Callable
from inspect import Signature

from click import Command


class IConsoleCommandFactory(ABC):

    """
    Interface for CLI Command serialization Factory.
    """

    @abstractmethod
    def get_plugin_names(self, package: Optional[str] = None) -> List[str]:

        """
        Returns a list of plugins located at a specified package.

        :param package: Name of the package
        :return: List of plugins inside the package.
        """

        pass

    @abstractmethod
    def kwargs_save_callback(self, name: str) -> Callable[[...], None]:

        """
        Automatically generates callback for command to save data.

        :param name: Name of the command
        :return: save-data callback
        """

        pass

    @abstractmethod
    def create_from_plugin(self, name: str, package: Optional[str] = None) -> Command:

        """
        Loads plugin from package and creates console representation for it.

        :param name: Name of the plugin.
        :param package: Name of the package.
        :return: click.Command instance, representing the plugin.
        """

        pass

    @abstractmethod
    def create_from_function(self, executable: Callable[[...], Any]) -> Command:

        """
        Creates a CLI representation for given function.

        :param executable: Callable object to represent in CLI.
        :return: click.Command instance, representing the object.
        """

        pass

    @abstractmethod
    def create_from_signature(self, name: str, help_msg: str, arguments: Signature) -> Command:

        """
        Generates the CLI command from given Signature object.

        :param name: Name of the function.
        :param help_msg: --help message. (Usually the doc_string of the function).
        :param arguments: Signature object
        :return: click.Command instance.
        """

        pass
