import numpy as np
import open3d as o3d  # type: ignore
from numpy.typing import NDArray
from numpy import float_
import math
import itertools
from typing import Any, Tuple


def crop_by_box(
    pc: o3d.geometry.PointCloud,
    crop_rx: float,
    crop_lx: float,
    crop_fy: float,
    crop_by: float,
) -> o3d.geometry.PointCloud:

    box: o3d.geometry.AxisAlignedBoundingBox = pc.get_axis_aligned_bounding_box()
    box_points: o3d.utility.Vector3dVector = box.get_box_points()
    coord: NDArray[float_] = np.asarray(box_points)

    arr: list[NDArray[float_]] = []
    for x in np.nditer(coord, flags=["external_loop"], order="F"):
        arr.append(x)
    left_x: float = min(arr[0])
    right_x: float = max(arr[0])
    back_y: float = min(arr[1])
    front_y: float = max(arr[1])

    left_x += crop_lx
    right_x -= crop_rx
    back_y += crop_by
    front_y -= crop_fy

    bounds: list[list[float]] = [
        [left_x, right_x],
        [back_y, front_y],
        [-math.inf, math.inf],
    ]
    bounding_box_points: list[Tuple[Any]] = list(itertools.product(*bounds))
    bounding_box = o3d.geometry.AxisAlignedBoundingBox.create_from_points(
        o3d.utility.Vector3dVector(bounding_box_points)
    )
    pc_croped: o3d.geometry.PointCloud = pc.crop(bounding_box)
    return pc_croped


if __name__ == "__main__":
    input_file: str = input()
    pc: o3d.geometry.PointCloud = o3d.io.read_point_cloud(input_file)
    new_file: o3d.geometry.PointCloud = crop_by_box(pc, 10, 40, 30, 10)
    o3d.io.write_point_cloud("new_file.ply", new_file)
    o3d.visualization.draw_geometries([new_file])
