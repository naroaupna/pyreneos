# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 12:20:08 2018

@author: naroairiarte

This program finds the mask in the folders and generates the appropriate mask
for the 20meters resolution images and for the 10 meter resolution images.
"""

import os
import sys
from osgeo import gdal
import numpy as np


def get_masks(path):
    """ This function finds the mask image in a given path and modifies
    it to obtain only de desired values. This function resamples the masks to
    10 meters resolution images.
    args:
        path (string): This is the path where all the images are stored.
    returns:
        mask_list (list): This is a list of lists. Every list inside the
        general list contains three elements:
                                               1- The 20 meters mask.
                                               2- The 10 meters mask.
                                               3- The path in which the mask
                                               must be applied.
    """
    masks_list = []
    mask_and_path_group = []
    for root, dirs, files in os.walk(path):
        for fil in files:
            fil_ext = os.path.splitext(fil)[1]
            if (('mosaic_image_SCL' in fil) and ((fil_ext == '.jp2') or
                                                     (fil_ext == '.tif'))):
                mask_and_path_group = []
                path_to_mask = os.path.join(root, fil)
                mask_image = _generate_mask_image(path_to_mask)
                mask_and_path_group.append(mask_image)
                mask_and_path_group.append(os.path.dirname(path_to_mask))
            if not not mask_and_path_group:
                masks_list.append(mask_and_path_group)
    return masks_list


def _generate_mask_image(mask_path):
    """ Generates the mask and adapts the size to the original file."""
    mask_name = os.path.basename(mask_path)
    mask_name = mask_name.replace('.jp2', 'mask.tif')
    path_to_new_image = os.path.dirname(mask_path)
    mask_name_with_path = os.path.join(path_to_new_image, mask_name)
    mask = gdal.Open(mask_path, gdal.GA_Update)
    if mask is None:
        print('Mask image could not be opened...')
        print('Exiting the program...')
        sys.exit(1)
    mask_array = mask.ReadAsArray()
    mask_array[mask_array == 4] = 1
    mask_array[mask_array == 5] = 1
    mask_array[mask_array != 1] = 0
    drv = gdal.GetDriverByName("MEM")
    dst_ds = drv.Create("", mask.RasterXSize, mask.RasterYSize, \
                        1, gdal.GDT_UInt16)
    dst_ds.SetGeoTransform(mask.GetGeoTransform())
    dst_ds.SetProjection(mask.GetProjectionRef())
    dst_ds.GetRasterBand(1).WriteArray(mask_array)
    geoT = mask.GetGeoTransform()
    drv = gdal.GetDriverByName("GTiff")
    resampled_mask = drv.Create(mask_name_with_path, \
                                mask.RasterXSize * 2, mask.RasterYSize * 2, 1, gdal.GDT_UInt16)
    this_geoT = (geoT[0], geoT[1] / 2, geoT[2], geoT[3], \
                 geoT[4], geoT[5] / 2)
    resampled_mask.SetGeoTransform(this_geoT)
    resampled_mask.SetProjection(mask.GetProjectionRef())
    gdal.RegenerateOverviews(dst_ds.GetRasterBand(1), \
                             [resampled_mask.GetRasterBand(1)], 'mode')
    resampled_mask.GetRasterBand(1).SetNoDataValue(0)
    resampled_mask_array = resampled_mask.ReadAsArray()
    resampled_mask = None
    return resampled_mask_array

