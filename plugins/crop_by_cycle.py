import numpy as np
import open3d as o3d  # type: ignore
from numpy.typing import NDArray
from numpy import float_
from typing import Any, Tuple


def crop_by_cycle(
    pc: o3d.geometry.PointCloud,
    crop_rx: float,
    crop_lx: float,
    crop_fy: float,
    crop_by: float,
) -> o3d.geometry.PointCloud:
    """
    Dummy function for cut transformation of PointCloud

    :param data: PointCloud to transform.
    :param ul: float flag for cutting the upper-left corner.
    :param ur: float flag for cutting the upper-right corner.
    :param ll: float flag for cutting the lower-left corner.
    :param lr: float flag for cutting the lower-right corner.
    :return: PointCloud
    """
    result: list[Any] = []
    colors: list[Any] = []
    point_cloud: NDArray[float_] = np.asarray(pc.points)
    colors_pc: NDArray[float_] = np.asarray(pc.colors)

    for point, color in zip(point_cloud, colors_pc):
        if (
            crop_lx <= np.array(point)[0] <= crop_rx
            and crop_by <= np.array(point)[1] <= crop_fy
        ):
            new_point = np.array(point)
            colors.append(color)
            result.append(new_point)

    result_cloud = o3d.geometry.PointCloud()
    result_cloud.points = o3d.utility.Vector3dVector(result)
    result_cloud.colors = o3d.utility.Vector3dVector(colors)
    return result_cloud
