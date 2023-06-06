import numpy as np
import open3d as o3d  # type: ignore
from numpy.typing import NDArray
from numpy import float_
import math
import itertools
from typing import Any, Tuple, List


def crop_by_box(
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
    box: o3d.geometry.AxisAlignedBoundingBox = pc.get_axis_aligned_bounding_box()
    box_points: o3d.utility.Vector3dVector = box.get_box_points()
    coord: NDArray[float_] = np.asarray(box_points)

    arr: List[NDArray[float_]] = []
    for x in np.nditer(coord, flags=["external_loop"], order="F"):
        arr.append(x)
    left_x: float = min(arr[0])
    right_x: float = max(arr[0])
    back_y: float = min(arr[1])
    front_y: float = max(arr[1])
    left_x0: float = left_x
    right_x0: float = right_x
    back_y0: float = back_y
    front_y0: float = front_y

    left_x += crop_lx
    right_x -= crop_rx
    if left_x > right_x0 or right_x < left_x0:
        left_x = right_x = 0
    back_y += crop_by
    front_y -= crop_fy
    if back_y > front_y0 or front_y < back_y0:
        back_y = front_y = 0

    bounds: list[list[float]] = [
        [left_x, right_x],
        [back_y, front_y],
        [-math.inf, math.inf],
    ]
    bounding_box_points: List[Tuple[Any]] = list(itertools.product(*bounds))
    bounding_box = o3d.geometry.AxisAlignedBoundingBox.create_from_points(
        o3d.utility.Vector3dVector(bounding_box_points)
    )
    pc_cropped: o3d.geometry.PointCloud = pc.crop(bounding_box)
    return pc_cropped
