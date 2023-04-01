from abc import ABC, abstractmethod
from typing import Any, List, Dict


class ITarget(ABC):

    """
    A standard receiver interface in the Command pattern hierarchy.
    """

    @abstractmethod
    def receive(self, result: object) -> None:
        """
        A method designated to receiving the result of Command invocation.

        :param result: result of Command invocation.
        :return: None
        """

        pass


class ICommand(ABC):

    """
    A standard invokable command interface in the Command pattern hierarchy.
    """

    @abstractmethod
    def execute(
        self, target: ITarget, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> None:
        """
        The invocation method for commands.

        :param target: the receiver for the result of commands invocation. (ITarget instance)
        :param args: list of positional arguments for command invocation.
        :param kwargs: dictionary of key-value arguments for command invocation.
        :return: None
        """
        pass
