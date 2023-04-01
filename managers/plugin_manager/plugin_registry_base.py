from abc import ABC, abstractmethod
from dataclasses import dataclass
from inspect import Signature
from typing import Any, List, Dict, Optional

from framework import ITarget


@dataclass(init=True, repr=True)
class PluginInfo:
    """
    DTO-object for transferring IPlugin instances description.
    """

    name: str
    desc: str
    signature: Signature


class IPluginRegistry(ABC):

    """
    A registry class for IPlugin instances. Provides a uniform way to work with a group of IPlugin instances.
    """

    @abstractmethod
    def add_plugin(self, name: str, package: Optional[str] = None) -> None:
        """
        Dynamically imports the specified plugin-function from a given package.
        Adds to the current IPluginRegistry instance.

        :param name: string containing the exact name of the module AND target function.
        :param package: [Optional] name of the package to import from.
        :return: None
        """

        pass

    @abstractmethod
    def invoke(self, plugin: str, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        """
        Invoke the specified plugin passing the given positional and key-value arguments. Invocation result is then passed
        to the ITarget instance specified in the __target attribute of the current IPluginRegistry instance.

        :raises: KeyError: if the plugin with given name is not registered in current IPluginRegistry instance.

        :param plugin: name of the plugin to invoke.
        :param args: list of positional arguments to pass.
        :param kwargs: dictionary of key-value arguments to pass.
        :return: None
        """
        pass

    @abstractmethod
    def get_info(self, plugin: str) -> PluginInfo:
        """
        Returns a PluginInfor instance containing all the necessary information about the requested plugin.

        :raises: KeyError: if the plugin with given name is not registered in current IPluginRegistry instance.

        :param plugin: name of the plugin to provide information about.
        :return: PluginInfo
        """
        pass

    @abstractmethod
    def supported_plugins(self) -> List[str]:
        """
        Returns a list of registered plugins.

        :return: List[str]: list of supported plugins.
        """
        pass

    @abstractmethod
    def set_target(self, target: ITarget) -> None:
        """
        Sets the target for plugin invocation.

        :param target: ITarget instance to pass invocation results to.
        :return: None
        """
        pass
