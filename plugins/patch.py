import open3d as o3d  # type: ignore


def patch(data: o3d.geometry.PointCloud, degree: int) -> o3d.geometry.PointCloud:
    """
     Dummy function for hole interpolation of PointCloud.

    :param data: PointCloud to transform.
    :param degree: degree of interpolation.
    :return: PointCloud
    """

    return data
