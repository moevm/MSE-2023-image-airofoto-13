import numpy as np
import open3d as o3d  # type: ignore
from numpy.typing import NDArray

from numpy import ndarray, dtype, float_
from typing import Any, Tuple, List


def clear(
    data: o3d.geometry.PointCloud, height: float, above: bool, below: bool
) -> Tuple[Any, List[Any]]:
    result: list[Any] = []
    colors: list[Any] = []

    pc_np: NDArray[float_] = np.asarray(data.points)
    np_colors: NDArray[float_] = np.asarray(data.colors)

    for point, color in zip(pc_np, np_colors):
        if above:
            if height <= np.array(point)[2]:
                new_point = np.array(point)
                colors.append(color)
                result.append(new_point)
        elif below:
            if height >= np.array(point)[2]:
                new_point = np.array(point)
                colors.append(color)
                result.append(new_point)

    result_cloud = o3d.geometry.PointCloud()
    result_cloud.points = o3d.utility.Vector3dVector(result)

    return result_cloud, colors
