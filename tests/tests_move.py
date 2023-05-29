import numpy as np
from numpy.typing import NDArray
import open3d as o3d  # type: ignore
from plugins import move

ply_file: o3d.geometry.PointCloud = o3d.io.read_point_cloud(
    "../images/model.ply"
)
ply_np: NDArray[np.float_] = np.asarray(ply_file.points)

# checking move to (0.0, 2.0, 3.0)
def test_move_1() -> None:
    move_cloud: o3d.geometry.PointCloud = move(
        ply_file, 0.0, 2.0, 3.0
    )
    move_cloud_np: NDArray[np.float_] = np.asarray(move_cloud.points)
    assert np.array_equal(np.round(np.subtract(move_cloud_np, ply_np), 2), np.round([[0.0, 2.0, 3.0]]*len(ply_np), 2))

# checking with one negative
def test_move_2() -> None:
    move_cloud_2: o3d.geometry.PointCloud = move(
        ply_file, 1.0, -2.5, 3.7
    )
    move_cloud_np_2: NDArray[np.float_] = np.asarray(move_cloud_2.points)
    assert np.array_equal(np.round(np.subtract(move_cloud_np_2, ply_np), 2), np.round([[1.0, -2.5, 3.7]]*len(ply_np), 2))

# checking with all negative
def test_move_3() -> None:
    move_cloud_3: o3d.geometry.PointCloud = move(
        ply_file, -1.0, -2.3, -3.0
    )
    move_cloud_np_3: NDArray[np.float_] = np.asarray(move_cloud_3.points)
    assert np.array_equal(np.round(np.subtract(move_cloud_np_3, ply_np), 2), np.round([[-1.0, -2.3, -3.0]]*len(ply_np), 2))

# checking when the point cloud remains unchanged
def test_move_4() -> None:
    move_cloud_4: o3d.geometry.PointCloud = move(
        ply_file, 0.0, 0.0, 0.0
    )
    move_cloud_np_4: NDArray[np.float_] = np.asarray(move_cloud_4.points)
    assert np.array_equal(np.round(move_cloud_np_4, 2), np.round(ply_np, 2))