from abc import ABC, abstractmethod
from inspect import Signature
from typing import Dict, List

from framework import ICommand, IConstraint


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
    def _constrain(
        original: Signature, constraints: Dict[str, IConstraint]
    ) -> Signature:
        """
        Returns a modified Signature object, containing all the provided argument constraints.

        :param original: Signature object of the original plugin
        :param constraints: Dictionary of IConstraint instances

        :return: Signature
        """

        pass

    @staticmethod
    @abstractmethod
    def lookup(package: str) -> List[str]:
        """
        Returns a list of plugins located at a specified package (or the default one if None was provided).

        :param package: Name of the package
        :return: List of plugins inside the package.
        """

        pass

    @staticmethod
    @abstractmethod
    def make_plugin(name: str, package: str) -> IPlugin:
        """
        Static method for simple IPlugin instance creation.

        :param name: string containing the exact name of the module AND target function in the module to wrap.
        :param package: [Optional] name of the package to import from.
        If not provided the standard __plugin_directory will be used.
        :return: IPlugin: instance of the IPlugin wrapper class.
        """

        pass
