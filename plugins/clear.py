import numpy as np
import open3d as o3d  # type: ignore
from numpy.typing import NDArray

from numpy import float_
from typing import Any


def clear(
    data: o3d.geometry.PointCloud, height: float, above: bool, below: bool
) -> o3d.geometry.PointCloud:

    pc_np: NDArray[float_] = np.asarray(data.points)
    np_colors: NDArray[float_] = np.asarray(data.colors)

    if above == below:
        raise Exception(
            "Модель не будет изменена при равных значениях параметров above и below"
        )

    if above:
        mask: list[bool] = np.where(pc_np[:, 2] <= height, True, False)

    elif below:
        mask: list[bool] = np.where(pc_np[:, 2] >= height, True, False)

    result_cloud: o3d.geometry.PointCloud = o3d.geometry.PointCloud()
    result_cloud.points = o3d.utility.Vector3dVector(pc_np[mask])
    result_cloud.colors = o3d.utility.Vector3dVector(np_colors[mask])
    result_cloud.estimate_covariances()
    result_cloud.estimate_normals()

    return result_cloud
