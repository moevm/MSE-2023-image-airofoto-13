import numpy as np
import open3d as o3d  # type: ignore
from numpy.typing import NDArray

from numpy import ndarray, dtype, float_
from typing import Any, Tuple


def filter_point_cloud_by_height(
    point_cloud: ndarray[Any, dtype[Any]],
    colors_of_pc: ndarray[Any, dtype[Any]],
    min_height: float,
    max_height: float,
):
    result: list[Any] = []
    colors: list[Any] = []

    for point, color in zip(point_cloud, colors_of_pc):
        if min_height <= np.array(point)[2] <= max_height:
            new_point = np.array(point)
            colors.append(color)
            result.append(new_point)

    result_cloud = (
        o3d.geometry.PointCloud()
    )  
    result_cloud.points = o3d.utility.Vector3dVector(
        result
    )  

    return result_cloud, colors


if __name__ == "__main__":
    input_file: str = input()
    min_height: float = float(input())
    max_height: float = float(input())
    pc: o3d.geometry.PointCloud = o3d.io.read_point_cloud(input_file)
    pc_np: NDArray[float_] = np.asarray(pc.points)
    np_colors: NDArray[float_] = np.asarray(pc.colors)
    new: Tuple[o3d.geometry.PointCloud, NDArray[float_]] = filter_point_cloud_by_height(
        pc_np, np_colors, min_height, max_height
    )
    new_file = new[0]
    new_colors = new[1]
    new_file.colors = o3d.utility.Vector3dVector(new_colors)
    o3d.io.write_point_cloud("filtered_file.ply", new_file)
    o3d.visualization.draw_geometries([new_file])
