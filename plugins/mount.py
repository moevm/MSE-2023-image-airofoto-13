import open3d as o3d  # type: ignore
from osgeo import gdal  # type: ignore
import numpy as np


def mount(data: o3d.geometry.PointCloud, picture_path: str) -> o3d.geometry.PointCloud:
    """
     Dummy function for picture embedding of PointCloud.

    :param data: PointCloud to transform.
    :param picture_path: path to the .tiff picture to embed.
    :return: PointCloud
    """
    geotiff_dataset = gdal.Open(picture_path)
    geotiff_data = geotiff_dataset.GetRasterBand(1).ReadAsArray()
    geotransform = geotiff_dataset.GetGeoTransform()

    pixel_size_x = geotransform[1]
    pixel_size_y = geotransform[5]

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

    return cloud_result
