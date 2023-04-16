import numpy as np
from numpy.typing import NDArray
import open3d as o3d  # type: ignore
from plugins import clear


# checking height filtering
def test_clear_1() -> None:
    ply_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/model.ply"
    )
    ply_np: NDArray[np.float_] = np.asarray(ply_file.points)
    clear_cloud: o3d.cpu.pybind.geometry.PointCloud = clear(
        ply_file, -3.0, True, False
    )[0]
    clear_cloud_np: NDArray[np.float_] = np.asarray(clear_cloud.points)
    assert len(clear_cloud_np) == sum((-3.0 <= i) for i in ply_np[:, 2])


# checking when the result is zero
def test_clear_2() -> None:
    ply_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/model.ply"
    )
    clear_cloud_2: o3d.cpu.pybind.geometry.PointCloud = clear(
        ply_file, 3.0, True, False
    )[0]
    clear_cloud_np_2: NDArray[np.float_] = np.asarray(clear_cloud_2.points)
    assert len(clear_cloud_np_2) == 0


# checking when the image remains unchanged
def test_clear_3() -> None:
    ply_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/model.ply"
    )
    ply_np: NDArray[np.float_] = np.asarray(ply_file.points)
    clear_cloud_3: o3d.cpu.pybind.geometry.PointCloud = clear(
        ply_file, 100.0, False, True
    )[0]
    clear_cloud_np_3: NDArray[np.float_] = np.asarray(clear_cloud_3.points)
    assert np.array_equal(ply_np, clear_cloud_np_3)


# checking when above is true and below is true
def test_clear_4() -> None:
    ply_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/model.ply"
    )
    ply_np: NDArray[np.float_] = np.asarray(ply_file.points)
    clear_cloud_4: o3d.cpu.pybind.geometry.PointCloud = clear(
        ply_file, -3.0, True, True
    )[0]
    clear_cloud_np_4: NDArray[np.float_] = np.asarray(clear_cloud_4.points)
    assert len(clear_cloud_np_4) == sum((-3.0 <= i) for i in ply_np[:, 2])


# checking when above is false and below is false
def test_clear_5() -> None:
    ply_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
        "../images/model.ply"
    )
    ply_np: NDArray[np.float_] = np.asarray(ply_file.points)
    clear_cloud_5: o3d.cpu.pybind.geometry.PointCloud = clear(
        ply_file, -3.0, False, False
    )[0]
    clear_cloud_np_5: NDArray[np.float_] = np.asarray(clear_cloud_5.points)
    assert len(clear_cloud_np_5) == 0
