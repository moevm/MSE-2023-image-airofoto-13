import numpy as np
import open3d as o3d  # type: ignore
from numpy import ndarray, dtype, float_
from numpy.typing import NDArray
from typing import Any


def rotation_matrix_func(
    mode: str,
    rotate_x: float,
    rotate_y: float,
    rotate_z: float
    ) -> ndarray[Any, dtype[Any]]:

    radians: dict[str, float] = {"x": rotate_x, "y": rotate_y, "z": rotate_z}

    if mode == "Degree":
        radians["x"] = np.radians(rotate_x)
        radians["y"] = np.radians(rotate_y)
        radians["z"] = np.radians(rotate_z)

    matr_x: NDArray[float_] = np.array(
        [
            [1, 0, 0],
            [0, np.cos(radians["x"]), -np.sin(radians["x"])],
            [0, np.sin(radians["x"]), np.cos(radians["x"])],
        ]
    )

    matr_y: NDArray[float_] = np.array(
        [
            [np.cos(radians["y"]), 0, np.sin(radians["y"])],
            [0, 1, 0],
            [-np.sin(radians["y"]), 0, np.cos(radians["y"])],
        ]
    )

    matr_z: NDArray[float_] = np.array(
        [
            [np.cos(radians["z"]), -np.sin(radians["z"]), 0],
            [np.sin(radians["z"]), np.cos(radians["z"]), 0],
            [0, 0, 1],
        ]
    )

    # https://en.wikipedia.org/wiki/Rotation_matrix - General rotations
    return matr_z @ matr_y @ matr_x


def rotate(
    point_cloud: o3d.geometry.PointCloud,
    mode: str,
    x: float,
    y: float,
    z: float,
    ) -> o3d.geometry.PointCloud:

    """
    Rotation transformation plugin.

    :param point_cloud:
    :param mode:
    :param x:
    :param y:
    :param z:
    :return:
    """

    rotation_matrix = rotation_matrix_func(mode, x, y, z)

    point_cloud.rotate(rotation_matrix, center=np.asarray([0, 0, 0]))

    return point_cloud
