from typing import List, Dict, Any, Optional

from framework import ITarget
from .plugin_registry_base import IPluginRegistry, PluginInfo
from .plugin_wrapper import PluginFactory, IPlugin


class PluginRegistry(IPluginRegistry):
    def __init__(self, plugins: Optional[Dict[str, IPlugin]] = None):
        if plugins:
            self.__plugins = plugins
        else:
            self.__plugins = {}

        self.__target = None  # type: ignore

    def add_plugin(self, name: str, package: Optional[str] = None) -> None:
        self.__plugins[name] = PluginFactory.make_plugin(name, package)

    def set_target(self, target: ITarget) -> None:
        self.__target = target

    def supported_plugins(self) -> List[str]:
        return list(self.__plugins.keys())

    def get_info(self, plugin: str) -> PluginInfo:
        if plugin not in self.__plugins:
            raise KeyError(f"{plugin} was not found in the registry!")

        return PluginInfo(
            plugin,
            self.__plugins[plugin].get_help(),
            self.__plugins[plugin].get_signature(),
        )

    def invoke(self, plugin: str, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        if plugin not in self.__plugins:
            raise KeyError(f"{plugin} was not found in the registry!")

        self.__plugins[plugin].execute(self.__target, *args, **kwargs)
