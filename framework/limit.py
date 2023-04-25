from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from click import ParamType, Choice, Path

from framework import EmbedSingleton


class IConstraint(ABC):

    """
    Compatibility class representing click constraints for arguments.
    e.g. click.Path, click.Choice
    """

    @abstractmethod
    def to_click(self) -> ParamType:

        """
        Returns click argument type.
        :return: ParamType.
        """

        pass


class ILimit(ABC, metaclass=EmbedSingleton):

    """
    Registry class for plugin constraints.
    Used by ConsoleCommandFactory instances to detect special argument types.
    """

    @abstractmethod
    def has_constraints(self, plugin: str, argument: str) -> bool:

        """
        Checks if there are constraints for specified plugin's specified argument.

        :param plugin: Name of the plugin
        :param argument: Name of the argument
        :return: 'True' if there is registered constraint for argument (provided by the plugin author)
         'False' otherwise.
        """

        pass

    @abstractmethod
    def get_plugin_constraints(self, plugin: str) -> Dict[str, ParamType]:

        """
        Returns all the plugins constraints.

        :param plugin: Name of the plugin.
        :return: Dictionary of constraints.
        """

        pass

    @abstractmethod
    def get_argument_constraint(self, plugin: str, argument: str) -> ParamType:
        """
        Returns constraint for specified plugin's specified argument.

        :param plugin: Name of the plugin.
        :param argument: Name of the argument.
        :return: click.ParamType
        """

        pass

    @abstractmethod
    def constrained_plugins(self) -> List[str]:

        """
        Returns list of plugins< for which constraints exist.

        :return: List of names.
        """

        pass

    @abstractmethod
    def constrain_argument(self, plugin: str, argument: str, value: IConstraint) -> None:

        """
        Adds constraint for specified argument of specified plugin.

        :param plugin: Plugin name.
        :param argument: Argument name.
        :param value: IConstraint instance.
        :return: None.
        """

        pass

    @abstractmethod
    def constrain_plugin(self, plugin: str, arguments: Dict[str, IConstraint]) -> None:

        """
        Adds constraints for plugin.

        :param plugin: Name of the plugin.
        :param arguments: Dictionary of constraints for arguments.
        :return: None.
        """

        pass

#-----------------------------------------------------------------------------------------------------------------------

class ChoiceConstraint(IConstraint):

    def __init__(self, choices: List[str], case_sensitive: Optional[bool] =True) -> None:
        self.__click_representation = Choice(choices, case_sensitive)

    def to_click(self) -> ParamType:
        return self.__click_representation


class PathConstraint(IConstraint):

    def __init__(self, exists: Optional[bool] = False) -> None:

        self.__click_representation = Path(exists=exists)

    def to_click(self) -> ParamType:
        return self.__click_representation


class Limit(ILimit):

    _constrain_values: Dict[str, Dict[str, ParamType]] = {}

    def __init__(self, plugin: Optional[str] = None, constraints: Optional[Dict[str, IConstraint]] = None):

        if plugin is not None and constraints is not None:
            self.constrain_plugin(plugin, constraints)

    def has_constraints(self, plugin: str, argument: str) -> bool:
        if plugin in self._constrain_values:
            if argument in self._constrain_values[plugin]:
                return True

        return False

    def get_plugin_constraints(self, plugin: str) -> Dict[str, ParamType]:
        if plugin in self._constrain_values:
            return self._constrain_values[plugin]

        raise KeyError(f"constraints for '{plugin}' plugin not found!")

    def get_argument_constraint(self, plugin: str, argument: str) -> ParamType:
        if plugin in self._constrain_values:
            if argument in self._constrain_values[plugin]:
                return self._constrain_values[plugin][argument]

        raise KeyError(f"'{argument}' constraint for '{plugin}' plugin not found!")

    def constrained_plugins(self) -> List[str]:
        return list(self._constrain_values.keys())

    def constrain_argument(self, plugin: str, argument:str, value: IConstraint) -> None:
        self._constrain_values[plugin][argument] = value.to_click()

    def constrain_plugin(self, plugin: str, arguments: Dict[str, IConstraint]) -> None:
        self._constrain_values[plugin] = {}

        for arg in arguments:
            self.constrain_argument(plugin, arg, arguments[arg])
