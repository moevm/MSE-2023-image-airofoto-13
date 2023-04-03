import numpy as np
import open3d as o3d
from numpy import ndarray, dtype
from typing import Any, Tuple, List


def crop_by_cycle(pc: o3d.cpu.pybind.geometry.PointCloud, crop_rx: float, crop_lx: float, crop_fy: float, crop_by: float) -> Tuple[Any, List[Any]]:
    result: list[Any] = []
    colors: list[Any] = []
    point_cloud: ndarray = np.asarray(pc.points)
    colors_pc: ndarray = np.asarray(pc.colors)

    for point, color in zip(point_cloud, colors_pc):
        if crop_lx <= abs(np.array(point)[0]) <= crop_rx and crop_by <= abs(np.array(point)[1]) <= crop_fy:
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
    pc: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(input_file)
    new_pc: Tuple[Any, List[Any]] = crop_by_cycle(pc, 30, 1, 50, 1)
    new_file = new_pc[0]
    new_colors = new_pc[1]
    new_file.colors = o3d.utility.Vector3dVector(new_colors)
    o3d.io.write_point_cloud("new_file.ply", new_file)
    o3d.visualization.draw_geometries([new_file])
    