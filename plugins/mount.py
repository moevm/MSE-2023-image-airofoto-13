import open3d as o3d  # type: ignore
from osgeo import gdal  # type: ignore
import numpy as np
from numpy.typing import NDArray
from numpy import float_


def mount(data: o3d.geometry.PointCloud, picture_path: str) -> o3d.geometry.PointCloud:
    """
     Dummy function for picture embedding of PointCloud.

    :param data: PointCloud to transform.
    :param picture_path: path to the .tiff picture to embed.
    :return: PointCloud
    """
    geotiff_dataset: gdal.Dataset = gdal.Open(picture_path)
    geotiff_data: NDArray[float_] = geotiff_dataset.GetRasterBand(1).ReadAsArray()

    geotiff_data_rgb:  NDArray[float_] = np.stack([geotiff_data]*3, axis=-1)

<<<<<<< Updated upstream
    origin_x = geotransform[0]
    origin_y = geotransform[3]

    geotiff_data_rgb = np.stack([geotiff_data] * 3, axis=-1)

    image = o3d.geometry.Image(geotiff_data_rgb)
    image_data = o3d.geometry.imageData()
    image_data.set_data(image)
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
        image_data, data, depth_scale=1.0, convert_rgb_to_intensity=False
    )
    cloud_result = o3d.geometry.PointCloud.create_from_rgbd_image(
        rgbd_image, o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault
    )
=======
    image: o3d.geometry.Image = o3d.geometry.Image(geotiff_data_rgb)
    image_data: o3d.geometry.imageData = o3d.geometry.imageData()
    image_data.set_data(image)
    rgbd_image: o3d.geometry.RGBDImage = o3d.geometry.RGBDImage.create_from_color_and_depth(image_data, data, depth_scale = 1.0, convert_rgb_to_intensity=False)
    cloud_result: o3d.geometry.PointCloud = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault)
>>>>>>> Stashed changes

    return cloud_result
