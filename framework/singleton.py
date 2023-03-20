from abc import ABCMeta
from typing import Any


class SingletonMeta(type):

    """
    Metaclass for any class, implementing the Singleton pattern.
    Provides a simple logic which implements and enforces the aforementioned pattern for any child class.

    _instances - is a dictionary to store any singleton class in use.
    """

    _instances: dict[type, SingletonMeta] = {}

    def __call__(cls, *args: list[Any], **kwargs: dict[str, Any]) -> Any:
        """
        Singleton business logic. Checks if the given class already exists (i.e. is inside _instances dictionary),
        if not - creates an instance,  adds it to the _instances and returns the created instance.

        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]


class EmbedSingleton(ABCMeta, SingletonMeta):
    """
    A helper class to easily embed Singleton pattern in any of the interfaces (classes derived from ABC).

    """

    pass
