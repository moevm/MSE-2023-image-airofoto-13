from typing import Any, List, Dict, Callable, TypeVar
from inspect import signature, Signature

from framework import ITarget
from .plugin_base import IPlugin


PluginCallableReturnType = TypeVar("PluginCallableReturnType")


class Plugin(IPlugin):
    def __init__(self, executable: Callable[[Any], PluginCallableReturnType]) -> None:
        self.__executable = executable

    def get_signature(self) -> Signature:
        return signature(self.__executable)

    def get_help(self) -> str:
        return str(self.__executable.__doc__)

    def execute(
        self, target: ITarget, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> None:
        target.receive(self.__executable(*args, **kwargs))
