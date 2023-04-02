import open3d as o3d  # type: ignore


def move(
    data: o3d.geometry.PointCloud, x: float, y: float, z: float
) -> o3d.geometry.PointCloud:
    """
    Dummy function for shift transformation of PointCloud.

    :param data: PointCloud to transform.
    :param x: x-axis shift value.
    :param y: y-axis shift value.
    :param z: z-axis shift value.
    :return: PointCloud
    """

    return data
