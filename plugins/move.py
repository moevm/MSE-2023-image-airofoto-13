import numpy as np
import open3d as o3d            # type: ignore
from numpy import ndarray, dtype
from typing import Any

def move(
    data: o3d.geometry.PointCloud, x: float, y: float, z: float
) -> o3d.geometry.PointCloud:

    points = data.points

    shift: ndarray[Any, dtype[Any]] = np.array([x, y, z])
    new_points: ndarray[Any, dtype[Any]] = np.asarray(points) + shift

    new_data: o3d.geometry.PointCloud = o3d.geometry.PointCloud()
    new_data.points = o3d.utility.Vector3dVector(new_points)
    new_data.colors = o3d.utility.Vector3dVector(data.colors)
    return new_data