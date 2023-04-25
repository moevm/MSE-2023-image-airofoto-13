from abc import ABC, abstractmethod
from typing import Any, Callable, List, Optional, TypeVar

from importlib import import_module
from pathlib import Path

PluginCallableReturnType = TypeVar("PluginCallableReturnType")

class ILoader(ABC):

    """
    Basic import tool for plugins.
    """

    @staticmethod
    @abstractmethod
    def lookup_plugins(path: str) -> List[str]:
        """
        Returns the list of plugins inside a given directory.

        :param path: path to look for plugins.
        :return: List of plugin names.
        """
        pass

    @staticmethod
    @abstractmethod
    def load_plugin(name: str, package: Optional[str] = None) -> Callable[[Any], PluginCallableReturnType]:
        """
        Returns the target function of a specified plugin.

        :param name: Plugin name (Filename should be same as the name of target function inside it)
        :param package: Directory, where plugin file is located.
        :return: Target function of a plugin
        """
        pass


class Loader(ILoader):

    """
    Concrete implementation of ILoader interface.

    __default_plugin_package is the name of standard plugin directory.
    """

    __default_plugin_package = "plugins"

    @staticmethod
    def lookup_plugins(path: str) -> List[str]:
        directory = Path(path)

        if not directory.exists():
            raise ValueError(f"{path} does not exist!")

        plugins = []

        for plugin in directory.glob("*.py"):
            if plugin.name != "__init__.py":
                plugins.append(plugin.name)

        return plugins

    @staticmethod
    def load_plugin(name: str, package: Optional[str] = None) -> Callable[[Any], PluginCallableReturnType]:

        if package is None:
            package = Loader.__default_plugin_package

        if ".py" in name:
            name = name[:-3:]

        return import_module(f"{package}.{name}").__dict__[name]
