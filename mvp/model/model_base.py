from abc import abstractmethod
from typing import Dict, Any, List

from framework import ITarget, EmbedSingleton
from managers import PluginInfo


class IModel(ITarget, metaclass=EmbedSingleton):

    """
    Interface for Model object from MVP pattern. Defines the essential data management and processing logic.
    """

    @abstractmethod
    def load_data(self, path: str) -> None:
        """
        Loads the PointCloud data from file along the given path. Stores internally.

        :param path: path to the raw data file.
        :return: None
        """

        pass

    @abstractmethod
    def save_data(self, path: str) -> None:
        """
        Saves the current PointCloud data stored in IModel instance to the file along the given path.

        :param path: path to save file to.
        :return: None
        """

        pass

    @abstractmethod
    def task(self, operation: str, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        """
        Perform a single task of processing the data stored.
        Updates the data stored with the result of the performed operation.

        :raises: RuntimeError: if the data was not loaded to IModel instance prior to the task() invocation.

        :param operation: name/type of the operation to perform on data.
        :param args: positional arguments.
        :param kwargs: key-value arguments.
        :return: None
        """

        pass

    # @abstractmethod
    # def execute_tasks(self, tasks: Dict[str, Dict[str, Any]]) -> None:
    #     pass

    @abstractmethod
    def operation_info(self, name: str) -> PluginInfo:
        """
        Returns the PluginInfo instance with the information about the desired operation.

        :raises: KeyError: if the desired operation is not supported.

        :param name: name/type of the operation.
        :return: PluginInfo
        """

        pass

    @abstractmethod
    def supported_operations(self) -> List[str]:
        """
        Returns a list of supported operations.

        :return: List[str]: list of supported operations.
        """

        pass
