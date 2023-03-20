import numpy as np
from numpy.typing import NDArray
import open3d as o3d  # type: ignore
from rotation import rotate_file
import math


# checking the rotation for an angle in radians
def test_rotate_ply_file_rotates_radians() -> None:
    ply_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/model.ply"
    )
    ply_np: NDArray[np.float_] = np.asarray(ply_file.points)
    expected_result_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/rotate_z_90.ply"
    )
    expected_result: NDArray[np.float_] = np.asarray(expected_result_file.points)
    rotated_cloud: o3d.cpu.pybind.geometry.PointCloud = rotate_file(
        ply_np, "Radian", 0, 0, math.pi / 2
    )
    rotated_np: NDArray[np.float_] = np.asarray(rotated_cloud.points)
    assert np.array_equal(np.round(rotated_np, 2), np.round(expected_result, 2))


# checking the rotation at an angle of 90 degrees along the z axis
def test_rotate_ply_file_rotates_z_90() -> None:
    ply_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/model.ply"
    )
    ply_np: NDArray[np.float_] = np.asarray(ply_file.points)
    expected_result_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/rotate_z_90.ply"
    )
    expected_result: NDArray[np.float_] = np.asarray(expected_result_file.points)
    rotated_cloud: o3d.cpu.pybind.geometry.PointCloud = rotate_file(
        ply_np, "Degree", 0, 0, 90
    )
    rotated_np: NDArray[np.float_] = np.asarray(rotated_cloud.points)
    assert np.array_equal(np.round(rotated_np, 2), np.round(expected_result, 2))


# checking the rotation at an angle of 30 degrees along the x axis
def test_rotate_ply_file_rotates_x_30() -> None:
    ply_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/model.ply"
    )
    ply_np: NDArray[np.float_] = np.asarray(ply_file.points)
    expected_result_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/rotate_x_30.ply"
    )
    expected_result: NDArray[np.float_] = np.asarray(expected_result_file.points)
    rotated_cloud: o3d.cpu.pybind.geometry.PointCloud = rotate_file(
        ply_np, "Degree", 30, 0, 0
    )
    rotated_np: NDArray[np.float_] = np.asarray(rotated_cloud.points)
    assert np.array_equal(np.round(rotated_np, 2), np.round(expected_result, 2))


# checking rotation along multiple axes
def test_rotate_ply_file_rotates_x_30_z_90() -> None:
    ply_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/model.ply"
    )
    ply_np: NDArray[np.float_] = np.asarray(ply_file.points)
    expected_result_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/rotate_x_30_z_90.ply"
    )
    expected_result: NDArray[np.float_] = np.asarray(expected_result_file.points)
    rotated_cloud: o3d.cpu.pybind.geometry.PointCloud = rotate_file(
        ply_np, "Degree", 30, 0, 90
    )
    rotated_np: NDArray[np.float_] = np.asarray(rotated_cloud.points)
    assert np.array_equal(np.round(rotated_np, 2), np.round(expected_result, 2))


# checking rotation at an angle of 270.5 degrees along the y axis
def test_rotate_ply_file_rotates_y_270_5() -> None:
    ply_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/model.ply"
    )
    ply_np: NDArray[np.float_] = np.asarray(ply_file.points)
    expected_result_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/rotate_y_270_5.ply"
    )
    expected_result: NDArray[np.float_] = np.asarray(expected_result_file.points)
    rotated_cloud: o3d.cpu.pybind.geometry.PointCloud = rotate_file(
        ply_np, "Degree", 0, 270.5, 0
    )
    rotated_np: NDArray[np.float_] = np.asarray(rotated_cloud.points)
    assert np.array_equal(np.round(rotated_np), np.round(expected_result))
