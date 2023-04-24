import numpy as np
from numpy.typing import NDArray
import open3d as o3d  # type: ignore
from cropping_at_the_adges import cropping_by_cycle as crop

ply_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
    "../images/model.ply"
)
ply_np: NDArray[np.float_] = np.asarray(ply_file.points)


# checking with positive arguments
def test_crop_1() -> None:
    clear_cloud: o3d.cpu.pybind.geometry.PointCloud = crop.crop_by_cycle(
        ply_file, 2.0, 1.0, 2.0, 1.0
    )[0]
    clear_cloud_np: NDArray[np.float_] = np.asarray(clear_cloud.points)
    assert len(clear_cloud_np) == sum(
        ((1.0 <= np.array(i)[0] <= 2.0) and (1.0 <= np.array(i)[1] <= 2.0))
        for i in ply_np
    )


# checking with negative arguments
def test_crop_2() -> None:
    clear_cloud_2: o3d.cpu.pybind.geometry.PointCloud = crop.crop_by_cycle(
        ply_file, -1.0, -3.0, -3.0, -13.0
    )[0]
    clear_cloud_np_2: NDArray[np.float_] = np.asarray(clear_cloud_2.points)
    assert len(clear_cloud_np_2) == sum(
        ((-3.0 <= np.array(i)[0] <= -1.0) and (-13.0 <= np.array(i)[1] <= -3.0))
        for i in ply_np
    )


# checking with positive and negative arguments
def test_crop_3() -> None:
    clear_cloud_3: o3d.cpu.pybind.geometry.PointCloud = crop.crop_by_cycle(
        ply_file, 3.0, -3.0, 13.0, -13.0
    )[0]
    clear_cloud_np_3: NDArray[np.float_] = np.asarray(clear_cloud_3.points)
    assert len(clear_cloud_np_3) == sum(
        ((-3.0 <= np.array(i)[0] <= 3.0) and (-13.0 <= np.array(i)[1] <= 13.0))
        for i in ply_np
    )


# checking when rx < lx
def test_crop_4() -> None:
    clear_cloud_4: o3d.cpu.pybind.geometry.PointCloud = crop.crop_by_cycle(
        ply_file, -3.0, 3.0, 13.0, -13.0
    )[0]
    clear_cloud_np_4: NDArray[np.float_] = np.asarray(clear_cloud_4.points)
    assert len(clear_cloud_np_4) == 0


# checking when hy < by
def test_crop_5() -> None:
    clear_cloud_5: o3d.cpu.pybind.geometry.PointCloud = crop.crop_by_cycle(
        ply_file, 3.0, -3.0, -13.0, 13.0
    )[0]
    clear_cloud_np_5: NDArray[np.float_] = np.asarray(clear_cloud_5.points)
    assert len(clear_cloud_np_5) == 0


# checking when rx < lx and hy < by
def test_crop_6() -> None:
    clear_cloud_6: o3d.cpu.pybind.geometry.PointCloud = crop.crop_by_cycle(
        ply_file, -3.0, 3.0, -13.0, 13.0
    )[0]
    clear_cloud_np_6: NDArray[np.float_] = np.asarray(clear_cloud_6.points)
    assert len(clear_cloud_np_6) == 0


# checking when the model remains unchanged
def test_crop_7() -> None:
    clear_cloud_7: o3d.cpu.pybind.geometry.PointCloud = crop.crop_by_cycle(
        ply_file, 100.0, -100.0, 100.0, -100.0
    )[0]
    clear_cloud_np_7: NDArray[np.float_] = np.asarray(clear_cloud_7.points)
    assert np.array_equal(ply_np, clear_cloud_np_7)
