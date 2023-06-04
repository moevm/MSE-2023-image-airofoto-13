from importlib import import_module
from inspect import Parameter, Signature, signature
from pathlib import Path
from typing import Dict, List

from .plugin_base import IPluginFactory, IPlugin, IConstraint
from .plugin import Plugin


class PluginFactory(IPluginFactory):

    """
    Concrete implementation of IPluginFactory interface.

    _plugin_directory: a basic package, containing required plugin function definitions.
    -plugin_constraints: name of the attribute containing constraints for plugin function arguments.
    """

    _plugin_constraints = "constraints"

    @staticmethod
    def lookup(package: str) -> List[str]:
        directory = Path(package)

        if not directory.exists():
            raise ValueError(f"{package} does not exist!")

        plugins = [file.name[:-3:] for file in directory.glob("*.py")]

        if "__init__" in plugins:
            plugins.pop(plugins.index("__init__"))

        return plugins

    @staticmethod
    def _constrain(
        original: Signature, constraints: Dict[str, IConstraint]
    ) -> Signature:

        new_arguments: List[Parameter] = []

        for argument in original.parameters:

            if argument not in constraints:
                new_arguments.append(original.parameters[argument])

            else:
                new_arguments.append(
                    Parameter(
                        argument,
                        Parameter.POSITIONAL_OR_KEYWORD,
                        annotation=constraints[argument].to_click(),
                        default=original.parameters[argument].default,
                    )
                )

        return original.replace(parameters=new_arguments)

    @staticmethod
    def make_plugin(name: str, package: str) -> IPlugin:

        plugin = f"{package}.{name}"

        plugin_module = import_module(plugin)

        if name not in plugin_module.__dict__:
            raise ImportError(
                f"Module {name} does not contain a plugin function "
                f"(callable function with the same name)"
            )

        plugin_signature = signature(plugin_module.__dict__[name])

        if PluginFactory._plugin_constraints in plugin_module.__dict__:
            plugin_signature = PluginFactory._constrain(
                plugin_signature,
                plugin_module.__dict__[PluginFactory._plugin_constraints],
            )

        return Plugin(plugin_module.__dict__[name], plugin_signature)
