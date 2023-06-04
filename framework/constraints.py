from abc import ABC, abstractmethod
from typing import List, Optional

from click import ParamType, Choice, Path


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

#-----------------------------------------------------------------------------------------------------------------------

class ChoiceConstraint(IConstraint):

    def __init__(self, choices: List[str], case_sensitive: Optional[bool] = True) -> None:
        self.__click_representation = Choice(choices, case_sensitive)

    def to_click(self) -> ParamType:
        return self.__click_representation


class PathConstraint(IConstraint):

    def __init__(self, exists: Optional[bool] = False) -> None:

        self.__click_representation = Path(exists=exists)

    def to_click(self) -> ParamType:
        return self.__click_representation
