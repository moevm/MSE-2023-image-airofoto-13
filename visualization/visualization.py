import numpy as np
import open3d as o3d  # type: ignore
from numpy import ndarray, dtype, float_
from numpy.typing import NDArray
from typing import Any


def visualization(
     point_cloud: o3d.geometry.PointCloud
) -> None:
    o3d.io.write_point_cloud("new_file.ply", point_cloud)
    o3d.visualization.draw_geometries([point_cloud])
