from abc import abstractmethod
from inspect import Signature
from typing import Optional

from framework import ICommand


class IPlugin(ICommand):

    """
    A generic wrapper for plug-in functions
    """

    @abstractmethod
    def get_signature(self) -> Signature:
        """
        Method to acquire signature of the function wrapped by the IPlugin instance.
        Required for internal business logic.

        :return: Signature: Signature object from inspect module, describing the wrapped function.
        """

        pass

    @abstractmethod
    def get_help(self) -> str:
        """
        Method to get a help-message about the function wrapped by the IPlugin instance.
        Required for internal business logic.

        :return: str: help message, usually the __doc__ attribute of the function.
        """
        pass


class IPluginFactory(ABC):

    """
    A Factory pattern class designated to serialization of IPlugin instances.
    """

    @staticmethod
    @abstractmethod
    def make_plugin(name: str, package: Optional[str] = None) -> IPlugin:
        """
        Static method for simple IPlugin instance creation.

        :param name: string containing the exact name of the module AND target function in the module to wrap.
        :param package: [Optional] name of the package to import from.
        If not provided the standard __plugin_directory will be used.
        :return: IPlugin: instance of the IPlugin wrapper class.
        """

        pass
