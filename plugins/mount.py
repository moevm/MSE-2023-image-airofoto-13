import open3d as o3d


def mount(data: o3d.geometry.PointCloud, picture_path: str) -> o3d.geometry.PointCloud:
    """
     Dummy function for picture embedding of PointCloud.

    :param data: PointCloud to transform.
    :param picture_path: path to the .tiff picture to embed.
    :return: PointCloud
    """

    return data