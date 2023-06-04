from typing import Any, List, Dict, Callable, TypeVar
from inspect import signature, Signature

from framework import ITarget
from .plugin_base import IPlugin


PluginCallableReturnType = TypeVar("PluginCallableReturnType")


class Plugin(IPlugin):
    def __init__(
        self,
        executable: Callable[[...], PluginCallableReturnType],
        constraints: Signature = None,
    ) -> None:

        self.__executable = executable
        self.__constraints: Signature | None = constraints

    def get_signature(self) -> Signature:
        if self.__constraints:
            return self.__constraints

        return signature(self.__executable)

    def get_help(self) -> str:
        return self.__executable.__doc__

    def execute(
        self, target: ITarget, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> None:
        target.receive(self.__executable(*args, **kwargs))
