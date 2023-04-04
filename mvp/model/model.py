from typing import List, Any, Dict, Optional
from os.path import join
import open3d  # type: ignore

from .model_base import IModel
from managers import PluginRegistry, FileManager, PluginInfo


class Model(IModel):
    def __init__(self, registry: Optional[PluginRegistry] = None):

        if registry is None:
            self.__operations = PluginRegistry()
            self.__operations.add_plugin("rotate")
        else:
            self.__operations = registry

        self.__operations.set_target(self)

        self.__output_name = join(".", "output.ply")

        self.__data: open3d.geometry.PointCloud | None = None

    def receive(self, result: open3d.geometry.PointCloud) -> None:
        self.__data = result

    def load_data(self, path: str) -> None:
        self.__data = FileManager().read(path)

    def save_data(self, path: str) -> None:
        if self.__data is not None:
            FileManager().write(self.__output_name, self.__data)

    def task(self, operation: str, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        self.__operations.invoke(operation, *args, **kwargs)

    def operation_info(self, name: str) -> PluginInfo:
        return self.__operations.get_info(name)

    def supported_operations(self) -> List[str]:
        return self.__operations.supported_plugins()
