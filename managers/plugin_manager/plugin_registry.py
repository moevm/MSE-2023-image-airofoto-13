from typing import List, Dict, Any, Optional

from framework import ITarget
from .plugin_registry_base import IPluginRegistry, PluginInfo
from .plugin_wrapper import PluginFactory, IPlugin


class PluginRegistry(IPluginRegistry):

    _default_plugin_package = "plugins"

    def __init__(self, plugins: Dict[str, IPlugin]):
        self._plugins: Dict[str, IPlugin] = plugins
        self._target: ITarget | None = None

    @classmethod
    def build(cls, package: Optional[str] = None) -> IPluginRegistry:

        plugin_names = PluginFactory.lookup(
            package if package else cls._default_plugin_package
        )

        plugins = {}

        for name in plugin_names:
            plugins[name] = PluginFactory.make_plugin(
                name, package if package else cls._default_plugin_package
            )

        return cls(plugins)

    def add_plugin(self, name: str, package: Optional[str] = None) -> None:
        self._plugins[name] = PluginFactory.make_plugin(
            name, package if package else PluginRegistry._default_plugin_package
        )

    def set_target(self, target: ITarget) -> None:
        self._target = target

    def supported_plugins(self) -> List[str]:
        return list(self._plugins.keys())

    def get_info(self, plugin: str) -> PluginInfo:
        if plugin not in self._plugins:
            raise KeyError(f"{plugin} was not found in the registry!")

        return PluginInfo(
            plugin,
            self._plugins[plugin].get_help(),
            self._plugins[plugin].get_signature(),
        )

    def invoke(self, plugin: str, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        if plugin not in self._plugins:
            raise KeyError(f"{plugin} was not found in the registry!")

        if self._target is None:
            raise TypeError("No target for plugin invocation!")

        self._plugins[plugin].execute(self._target, *args, **kwargs)
