# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 12:41:32 2018

@author: naroairiarte

This class is corrects the specified images using the masks.
It is possible to use it to correct the NDVI images only or to correct all
the images in a given path.
"""

import raster_finder as rf
from osgeo import gdal, osr
import os
import obtain_mask as om
import shutil
import vegetation_indexes as vi


JP2 = '.jp2'
RESAMPLED = 'resampled.jp2'
MASKED = 'masked_QSC.jp2'
MOSAIC_02 = 'mosaic_image_B02.jp2'
MOSAIC_03 = 'mosaic_image_B03.jp2'
MOSAIC_04 = 'mosaic_image_B04.jp2'
MOSAIC_05 = 'mosaic_image_B05.jp2'
MOSAIC_06 = 'mosaic_image_B06.jp2'
MOSAIC_07 = 'mosaic_image_B07.jp2'
MOSAIC_08 = 'mosaic_image_B08.jp2'
MOSAIC_8A = 'mosaic_image_B8A.jp2'
MOSAIC_11 = 'mosaic_image_B11.jp2'
MOSAIC_12 = 'mosaic_image_B12.jp2'


def correct_images(path, only_ndvi):
    """ Corrects the images applying a mask. It will generates tif images in
    the same folder where the original images are stored with the corrections
    of the mask applied.
    args:
        path (string): This is the path where all the images are stored.
        only_ndvi (boolean): if true, the mask will only be applied to the
                             NDVI images. If false, it will applied to all
                             the images in the path of the mask.

    """
    masks_and_paths_list = om.get_masks(path)
    len_masks_list = len(masks_and_paths_list)
    used_paths_for_ndvi = []
    for i in range(0, len_masks_list):
        actual_mask = masks_and_paths_list[i][0]
        actual_path = masks_and_paths_list[i][1]
        if (actual_path not in used_paths_for_ndvi):
            for raster in rf.find_rasters(actual_path):
                if _ten_meter_bands_condition(raster):
                    _generate_masked_rasters_10m_bands(raster, actual_mask, actual_path)
                elif _twenty_meter_bands_condition(raster):
                    _generate_masked_rasters_20m_bands(raster, actual_mask, actual_path)
            if (only_ndvi):
                if (masks_and_paths_list[i][1] not in used_paths_for_ndvi):
                    vi.ndvi_index(masks_and_paths_list[i][1])
                    used_paths_for_ndvi.append(masks_and_paths_list[i][1])


def _get_raster_array(raster):
    raster_image = gdal.Open(raster, gdal.GA_Update)
    if raster_image is None:
        print('Raster image could not be opened...')
        print('Exiting the program...')
    band = raster_image.GetRasterBand(1)
    raster_array = band.ReadAsArray()
    return raster_array, raster_image


def _get_raster_array_resampled(raster):
    img_name = os.path.basename(raster)
    #img_name = img_name.replace(JP2, RESAMPLED)
    img_name = img_name.replace('rmasked', 'resampled_masked')
    path_to_new_image = os.path.dirname(raster)
    img_name_with_path = os.path.join(path_to_new_image, img_name)
    raster_image = gdal.Open(raster, gdal.GA_Update)
    if raster_image is None:
        print('Raster image could not be opened...')
        print('Exiting the program...')
    band = raster_image.GetRasterBand(1)
    raster_array = band.ReadAsArray()

    drv = gdal.GetDriverByName("MEM")
    dst_ds = drv.Create("", raster_image.RasterXSize, raster_image.RasterYSize, \
                        1, gdal.GDT_UInt16)
    dst_ds.SetGeoTransform(raster_image.GetGeoTransform())
    dst_ds.SetProjection(raster_image.GetProjectionRef())
    dst_ds.GetRasterBand(1).WriteArray(raster_array)
    geoT = raster_image.GetGeoTransform()
    drv = gdal.GetDriverByName("GTiff")
    resampled_image = drv.Create(img_name_with_path, \
                                raster_image.RasterXSize * 2, raster_image.RasterYSize * 2, 1, gdal.GDT_UInt16)
    this_geoT = (geoT[0], geoT[1] / 2, geoT[2], geoT[3], \
                 geoT[4], geoT[5] / 2)
    resampled_image.SetGeoTransform(this_geoT)
    resampled_image.SetProjection(raster_image.GetProjectionRef())
    gdal.RegenerateOverviews(dst_ds.GetRasterBand(1), \
                             [resampled_image.GetRasterBand(1)], 'mode')
    resampled_image.GetRasterBand(1).SetNoDataValue(0)
    resampled_array = resampled_image.ReadAsArray()
    resampled_image = None
    return resampled_array, raster_image


def _store_and_create_masked_raster(out_raster, raster_image, raster):
    """ This function creates and stores the masked rasters.
    """
    band = raster_image.GetRasterBand(1)
    band.WriteArray(out_raster)
    projection = osr.SpatialReference()
    projection.ImportFromWkt(raster_image.GetProjectionRef())
    raster_image = None



def _store_and_create_masked_raster_resampled(out_raster, raster):
    """ This function creates a resampled raster and stores it.
    """
    mask_name_with_path = raster
    image = gdal.Open(raster, gdal.GA_Update)
    if image is None:
        print('Mask image could not be opened...')
        print('Exiting the program...')
        sys.exit(1)
    drv = gdal.GetDriverByName("MEM")
    dst_ds = drv.Create("", image.RasterXSize * 2, image.RasterYSize * 2, 1, gdal.GDT_UInt16)
    dst_ds.SetGeoTransform(image.GetGeoTransform())
    dst_ds.SetProjection(image.GetProjectionRef())
    dst_ds.GetRasterBand(1).WriteArray(out_raster)
    geoT = image.GetGeoTransform()
    drv = gdal.GetDriverByName("GTiff")
    resampled_image = drv.Create(mask_name_with_path, \
                                image.RasterXSize * 2, image.RasterYSize * 2, 1, gdal.GDT_UInt16)
    this_geoT = (geoT[0], geoT[1] / 2, geoT[2], geoT[3], \
                 geoT[4], geoT[5] / 2)
    resampled_image.SetGeoTransform(this_geoT)
    resampled_image.SetProjection(image.GetProjectionRef())
    gdal.RegenerateOverviews(dst_ds.GetRasterBand(1), \
                             [resampled_image.GetRasterBand(1)], 'mode')
    resampled_image.GetRasterBand(1).SetNoDataValue(0)
    resampled_image = None


def _ten_meter_bands_condition(image_name):
    """ This function is just created to contain a long boolean condition, to make the code clearer.
    """
    return ((MOSAIC_02 in image_name) or (MOSAIC_03 in image_name) or
        (MOSAIC_04 in image_name) or (MOSAIC_08 in image_name))


def _twenty_meter_bands_condition(image_name):
    """ This function is just created to contain a long boolean condition, to make the code clearer.
    """
    return ((MOSAIC_05 in image_name) or (MOSAIC_06 in image_name) or
        (MOSAIC_07 in image_name) or (MOSAIC_8A in image_name) or
        (MOSAIC_11 in image_name) or (MOSAIC_12 in image_name))


def _generate_masked_rasters_10m_bands(raster, actual_mask, actual_path):
    """ This function generates the 10 meters rasters.
    """
    filename = os.path.basename(raster)
    band_name = _get_image_band(filename)
    image_copy_name = filename.replace(band_name + JP2, 'masked_'+band_name+JP2)
    image_copy = os.path.join(actual_path, image_copy_name)
    shutil.copy(raster, image_copy)
    raster_array, raster_image = _get_raster_array(image_copy)
    out_raster = raster_array * actual_mask
    _store_and_create_masked_raster(out_raster,
                                    raster_image,
                                    image_copy)


def _generate_masked_rasters_20m_bands(raster, actual_mask, actual_path):
    """ This function generates the 20 meters rasters.
    """
    filename = os.path.basename(raster)
    band_name = _get_image_band(filename)
    image_copy_name = filename.replace(band_name + JP2, 'masked_' + band_name + JP2)
    image_copy = os.path.join(actual_path, image_copy_name)
    shutil.copy(raster, image_copy)
    raster_array, raster_image = _get_raster_array_resampled(image_copy)
    filename_2 = os.path.basename(image_copy)
    image_copy_name_2 = filename_2.replace('masked_', 'rmasked_')
    #image_copy_name_2 = filename_2.replace(JP2, MASKED)
    image_copy_2 = os.path.join(actual_path, image_copy_name_2)
    shutil.copy(image_copy, image_copy_2)
    out_raster = raster_array * actual_mask
    _store_and_create_masked_raster_resampled(out_raster,
                                              image_copy_2)


def _get_image_band(image_name):
    """This function extracts the band name of a image.
    """
    n, ext = os.path.splitext(image_name)
    ind = n.rfind('_')
    band_name = n[ind + 1:]
    return band_name