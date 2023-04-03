import numpy as np
from numpy.typing import NDArray
import open3d as o3d  # type: ignore
from filtering import filtering


# checking height filtering
def test_filtering_1() -> None:
    ply_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/model.ply"
    )
    ply_np: NDArray[np.float_] = np.asarray(ply_file.points)
    filter_cloud: o3d.cpu.pybind.geometry.PointCloud = (
        filtering.filter_point_cloud_by_height(
            ply_np, np.asarray(ply_file.colors), -3, -1.5
        )[0]
    )
    filter_cloud_np: NDArray[np.float_] = np.asarray(filter_cloud.points)
    assert len(filter_cloud_np) == sum((-3 <= i <= -1.5) for i in ply_np[:, 2])


# checking when the result is zero
def test_filtering_2() -> None:
    ply_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/model.ply"
    )
    ply_np: NDArray[np.float_] = np.asarray(ply_file.points)
    filter_cloud_2: o3d.cpu.pybind.geometry.PointCloud = (
        filtering.filter_point_cloud_by_height(
            ply_np, np.asarray(ply_file.colors), 1, 3
        )[0]
    )
    filter_cloud_np_2: NDArray[np.float_] = np.asarray(filter_cloud_2.points)
    assert len(filter_cloud_np_2) == 0


# checking when the image remains unchanged
def test_filtering_3() -> None:
    ply_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/model.ply"
    )
    ply_np: NDArray[np.float_] = np.asarray(ply_file.points)
    filter_cloud_3: o3d.cpu.pybind.geometry.PointCloud = (
        filtering.filter_point_cloud_by_height(
            ply_np, np.asarray(ply_file.colors), -100, 100
        )[0]
    )
    filter_cloud_np_3: NDArray[np.float_] = np.asarray(filter_cloud_3.points)
    assert np.array_equal(ply_np, filter_cloud_np_3)
