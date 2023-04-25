from typing import Any, Dict, List, Optional
from abc import abstractmethod, ABC



class IBackbone(ABC):

    """
    CLI backbone interface.
    Declares the bare minimum of business logic needed from a business object for command-line interface.
    Enforces the Singleton pattern on derived classes.
    """

    @abstractmethod
    def set_source(self, path: str) -> None:
        """
        Sets source data location.

        :param path: path to a .ply file containing source PointCloud.
        :return: None
        """
        pass

    @abstractmethod
    def get_source(self) -> str:
        """
        Returns the stored path to source data .ply file. Either user provided or the default one.

        :return: Path to the source file
        """
        pass

    @abstractmethod
    def set_destination(self, path: str) -> None:
        """
        Sets output file location.

        :param path: Path to the output file to write program result to.
        :return: None
        """
        pass

    @abstractmethod
    def get_destination(self) -> str:
        """
        Returns the stored path to output file. Either user provided or the default one.

        :return: Path to the output file
        """
        pass

    @abstractmethod
    def get_requirements(self) -> List[str]:
        """
        Returns a list of keys required to be in config.

        :return: List of keys
        """
        pass

    @abstractmethod
    def valid_config(self, config: Dict[str | int, Any]) -> bool:
        """
        Checks if the provided config meets the requirements.

        :param config: Config dictionary
        :return: 'True' if config meets requirements, 'False' if it doesn't.
        """
        pass

    @abstractmethod
    def generate_config(self) -> Dict[str | int, Any]:
        """
        Returns the config fictionary of valid format.

        :return: Dictionary containing program configuration.
        """
        pass

    @abstractmethod
    def load_config(self, path: Optional[str] = None) -> None:
        """
        Loads config to Backbone instance from file along the given path.
        Uses default hardcoded path if none provided.

        :param path: path to config file
        :return: None
        """
        pass

    @abstractmethod
    def dump_config(self, path: Optional[str] = None) -> None:
        """
        Dumps config from Backbone instance to file along the given path.
        Uses default hardcoded path if none provided.

        :param path:
        :return:
        """
        pass

    @abstractmethod
    def enqueue(self, operation_params: Dict[str, Any]) -> None:
        """

        Adds operation invocation to program config.

        :raises: KeyError: if the operation (type) was not found among the operation_params.

        :param operation_params: Arguments to pass to the operation function along with its name
        :return: None
        """
        pass
