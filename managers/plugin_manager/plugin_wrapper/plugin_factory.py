from importlib import import_module
from typing import Optional

from .plugin_base import IPluginFactory, IPlugin
from .plugin import Plugin



class PluginFactory(IPluginFactory):

    """
    Concrete implementation of IPluginFactory interface.

    __plugin_directory: a basic package, containing required plugin function definitions.
    """

    __plugin_directory = "plugins"

    @staticmethod
    def make_plugin(name: str, package: Optional[str] = None) -> IPlugin:
        if package:
            return Plugin(import_module(f"{package}.{name}").__dict__[name])

        else:
            return Plugin(import_module(f"{PluginFactory.__plugin_directory}.{name}").__dict__[name])
