from inspect import signature, Signature
from typing import Any, List, Dict

from framework import ICommand, ITarget
from .plugin_base import IPlugin


class Plugin(ICommand, IPlugin):
    def __init__(self, executable: callable) -> None:
        self.__executable = executable

    def get_signature(self) -> Signature:
        return signature(self.__executable)

    def get_help(self) -> str:
        return self.__executable.__doc__

    def execute(
        self, target: ITarget, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> None:
        target.receive(self.__executable(*args, **kwargs))
