import numpy as np
import open3d as o3d  # type: ignore
from numpy import ndarray, dtype, float_
from numpy.typing import NDArray
from typing import Any


def rotation_matrix_func(
    string: str, rotate_x: float, rotate_y: float, rotate_z: float
) -> list[ndarray[Any, dtype[Any]]]:
    radians: dict[str, float] = {"x": rotate_x, "y": rotate_y, "z": rotate_z}
    if string == "Degree":
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
    matrices = [matr_x, matr_y, matr_z]
    return matrices


def rotate(
    point_cloud: ndarray[Any, dtype[Any]],
    string: str,
    rotate_x: float,
    rotate_y: float,
    rotate_z: float,
) -> o3d.geometry.PointCloud:

    """
    Rotation transformation plugin.

    :param point_cloud:
    :param string:
    :param rotate_x:
    :param rotate_y:
    :param rotate_z:
    :return:
    """

    rotation_matrix = rotation_matrix_func(string, rotate_x, rotate_y, rotate_z)
    rotated: list[Any] = []

    for point in point_cloud:
        new_point = np.array(point)
        for (
            matr
        ) in (
            rotation_matrix
        ):  # поворачиваем по каждой оси, т.е. применяем каждую матрицу поворота
            new_point = np.dot(matr, new_point)
        rotated.append(new_point)
    rotated_cloud = (
        o3d.geometry.PointCloud()
    )  # PointCloud class. A point cloud consists of point coordinates, and optionally point colors and point normals.
    rotated_cloud.points = o3d.utility.Vector3dVector(
        rotated
    )  # Convert float64 numpy array of shape (n, 3) to Open3D format
    return rotated_cloud
