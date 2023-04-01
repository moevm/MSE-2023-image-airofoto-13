import open3d as o3d


def clear(data: o3d.geometry.PointCloud, height: float, above: bool, below: bool) -> o3d.geometry.PointCloud:
    """
     Dummy function for height-filtering of PointCloud.

    :param data: PointCloud to transform.
    :param height: z-axis value to filter by.
    :param above: boolean flag to switch filtering above the given height.
    :param below: boolean flag to switch filtering below the given height.
    :return: PointCloud
    """

    return data