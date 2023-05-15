import numpy as np
from numpy.typing import NDArray
import open3d as o3d  # type: ignore
from plugins import crop_by_box

ply_file: o3d.cpu.pybind.geometry.PointCloud = o3d.io.read_point_cloud(
    "../images/model.ply"
)
ply_np: NDArray[np.float_] = np.asarray(ply_file.points)
left_x: float = np.amin(ply_np, 0)[0]
right_x: float = np.amax(ply_np, 0)[0]
back_y: float = np.amin(ply_np, 0)[1]
front_y: float = np.amax(ply_np, 0)[1]


# checking cropping
def test_crop_1() -> None:
    clear_cloud: o3d.cpu.pybind.geometry.PointCloud = crop_by_box(
        ply_file, 3.0, 3.0, 3.0, 3.0
    )
    clear_cloud_np: NDArray[np.float_] = np.asarray(clear_cloud.points)
    assert len(clear_cloud_np) == sum(
        (
            (left_x + 3.0 <= np.array(i)[0] <= right_x - 3.0)
            and (back_y + 3.0 <= np.array(i)[1] <= front_y - 3.0)
        )
        for i in ply_np
    )


# checking negative values
def test_crop_2() -> None:
    clear_cloud_2: o3d.cpu.pybind.geometry.PointCloud = crop_by_box(
        ply_file, -3.0, 2.0, 3.0, -2.0
    )
    clear_cloud_np_2: NDArray[np.float_] = np.asarray(clear_cloud_2.points)
    assert len(clear_cloud_np_2) == sum(
        (
            (left_x + 2.0 <= np.array(i)[0] <= right_x + 3.0)
            and (back_y - 2.0 <= np.array(i)[1] <= front_y - 3.0)
        )
        for i in ply_np
    )


# checking when the entered values for the x-axis are greater than the difference between the maximum and minimum coordinates
# (the resulting crop boundaries will intersect)
def test_crop_3() -> None:
    clear_cloud_3: o3d.cpu.pybind.geometry.PointCloud = crop_by_box(
        ply_file, 10.0, 10.0, 3.0, 2.0
    )
    clear_cloud_np_3: NDArray[np.float_] = np.asarray(clear_cloud_3.points)
    assert len(clear_cloud_np_3) == sum(
        (back_y + 2.0 <= np.array(i)[1] <= front_y - 3.0) for i in ply_np
    )


# checking when the entered values for the y-axis are greater than the difference between the maximum and minimum coordinates
# (the resulting crop boundaries will intersect)
def test_crop_4() -> None:
    clear_cloud_4: o3d.cpu.pybind.geometry.PointCloud = crop_by_box(
        ply_file, 3.0, 2.0, 100.0, 100.0
    )
    clear_cloud_np_4: NDArray[np.float_] = np.asarray(clear_cloud_4.points)
    assert len(clear_cloud_np_4) == sum(
        (left_x + 2.0 <= np.array(i)[0] <= right_x - 3.0) for i in ply_np
    )


# checking when the resulting crop boundaries for both axes will intersect (empty result)
def test_crop_5() -> None:
    clear_cloud_5: o3d.cpu.pybind.geometry.PointCloud = crop_by_box(
        ply_file, 10.0, 10.0, 100.0, 100.0
    )
    clear_cloud_np_5: NDArray[np.float_] = np.asarray(clear_cloud_5.points)
    assert len(clear_cloud_np_5) == 0


# checking when the model remains unchanged
def test_crop_6() -> None:
    clear_cloud_6: o3d.cpu.pybind.geometry.PointCloud = crop_by_box(
        ply_file, -3.0, -3.0, -3.0, -3.0
    )
    clear_cloud_np_6: NDArray[np.float_] = np.asarray(clear_cloud_6.points)
    assert np.array_equal(ply_np, clear_cloud_np_6)
