import numpy as np
from numpy.typing import NDArray
import open3d as o3d  # type: ignore
from plugins import sewing_the_holes

ply_file: o3d.geometry.PointCloud = o3d.io.read_point_cloud("../images/bunny.ply")
ply_np: NDArray[np.float_] = np.asarray(ply_file.points)


def test_sew_the_holes_1() -> None:
    expected_result_file: o3d.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/fill_holes_bunny_11.ply"
    )
    expected_result: NDArray[np.float_] = np.asarray(expected_result_file.points)

    sew_cloud: o3d.cpu.pybind.geometry.PointCloud = sewing_the_holes(ply_file, 11.0)
    sew_np: NDArray[np.float_] = np.asarray(sew_cloud.points)
    assert np.array_equal(np.round(sew_np[2:], 2), np.round(expected_result[2:], 2))


def test_sew_the_holes_2() -> None:
    sew_cloud_2: o3d.cpu.pybind.geometry.PointCloud = sewing_the_holes(ply_file, 0.0)
    sew_np_2: NDArray[np.float_] = np.asarray(sew_cloud_2.points)
    assert np.array_equal(np.round(sew_np_2[2:], 2), np.round(ply_np[2:], 2))


def test_sew_the_holes_3() -> None:
    sew_cloud_3: o3d.cpu.pybind.geometry.PointCloud = sewing_the_holes(ply_file, -1.0)
    sew_np_3: NDArray[np.float_] = np.asarray(sew_cloud_3.points)
    assert np.array_equal(np.round(sew_np_3[2:], 2), np.round(ply_np[2:], 2))
