from abc import ABC, abstractmethod
from typing import Any


class IFactory(ABC):

    """
    A standard Abstract Factory class interface.
    """

    @staticmethod
    @abstractmethod
    def create() -> Any:
        """
        Standard method to create objects. Needs to be overriden for the object-specific factory.

        :return: - Custom object.
        """
