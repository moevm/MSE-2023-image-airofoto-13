import open3d as o3d  # type: ignore
import numpy as np
from numpy.typing import NDArray
from numpy import float_


def sewing_the_holes(
    pc: o3d.geometry.PointCloud, radius: float
) -> o3d.geometry.PointCloud:
    pc.estimate_normals()
    distances: open3d.utility.DoubleVector = pc.compute_nearest_neighbor_distance()
    avg_dist: NDArray[float_] = np.mean(distances)
    radius: float = 1.5 * avg_dist
    mesh: open3d.geometry.TriangleMesh = (
        o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
            pc, o3d.utility.DoubleVector([radius, radius * 2])
        )
    )
    filled = (
        o3d.t.geometry.TriangleMesh.from_legacy(mesh).fill_holes(radius).to_legacy()
    )
    result_cloud: o3d.geometry.PointCloud = o3d.geometry.PointCloud()
    result_cloud.points = filled.vertices
    result_cloud.colors = filled.vertex_colors
    result_cloud.normals = filled.vertex_normals

    return result_cloud


if __name__ == "__main__":
    input_file: str = input()
    pc: o3d.geometry.PointCloud = o3d.io.read_point_cloud(input_file)
    new_pc: o3d.geometry.PointCloud = sewing_the_holes(pc, 100)
    o3d.io.write_point_cloud("new_file.ply", new_pc)
    o3d.visualization.draw_geometries([new_pc])
