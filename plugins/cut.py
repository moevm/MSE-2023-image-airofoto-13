import open3d as o3d # type: ignore


def cut(
    data: o3d.geometry.PointCloud, ul: bool, ur: bool, ll: bool, lr: bool
) -> o3d.geometry.PointCloud:
    """
    Dummy function for cut transformation of PointCloud

    :param data: PointCloud to transform.
    :param ul: boolean flag for cutting the upper-left corner.
    :param ur: boolean flag for cutting the upper-right corner.
    :param ll: boolean flag for cutting the lower-left corner.
    :param lr: boolean flag for cutting the lower-right corner.
    :return: PointCloud
    """

    return data
