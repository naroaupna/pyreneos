# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 19:31:55 2018

@author: Naroa

This function calculates the NDVI index of the bands 04 and 08.
"""

import os
import numpy as np
from osgeo import gdal, osr
import sys


MOSAIC_B04 = 'mosaic_image_B04masked_QSC.jp2'
MOSAIC_B08 = 'mosaic_image_B08masked_QSC.jp2'
NDVI = '_NDVI.tif'
JP2 = '.jp2'
BAND_04 = 'B04'
BAND_08 = 'B08'


def calculate_NDVI_V1(path):
    """ calculates the NDVI index of the bands 04 and 08. The images which will
    be used to calculate the NDVI are the ones obtained by the mosaicizing
    process of the images of the band 4 and 8.
    args:
        path (string): This is the path where all the images are stored.
    """
    b4 = None
    b8 = None
    for root, dirs, files in os.walk(path):
        for f in files:
            if (MOSAIC_B04 in f):
                b4 = f
            elif (MOSAIC_B08 in f):
                b8 = f
            if ((b8 != None) and (b4 != None)):
                path_to_b4 = os.path.join(root, b4)
                path_to_b8 = os.path.join(root, b8)
                _calcultate_ndvi_images(path_to_b4, path_to_b8)
                return


def _calcultate_ndvi_images(b4, b8):
    """This function uses the paths given as arguments to calculate the NDVI
    of the bands storedn in the list.
    """
    t = np.float32
    b4_filename = os.path.basename(b4)
    ndvi_filename_with_band = b4_filename.replace(JP2, NDVI)
    ndvi_filename = ndvi_filename_with_band.replace(BAND_04, '')
    b4_path = os.path.dirname(b4)
    ndvi_path = os.path.join(b4_path, ndvi_filename)

    b4_image = gdal.Open(b4, gdal.GA_Update)
    if b4_image is None:
        print('Image could not be opened...')
        print('Exiting the program...')
        sys.exit(1)

    b8_image = gdal.Open(b8, gdal.GA_Update)
    if b8_image is None:
        print('Image could not be opened...')
        print('Exiting the program...')
        sys.exit(1)

    transform = b4_image.GetGeoTransform()

    geotiff = gdal.GetDriverByName('GTiff')
    output = geotiff.CreateCopy(ndvi_path, b4_image, 0)

    output = geotiff.Create(
        ndvi_path,
        b4_image.RasterXSize, b4_image.RasterYSize,
        1,
        gdal.GDT_Float32)
    r = b4_image.GetRasterBand(1).ReadAsArray(0, 0, b4_image.RasterXSize, \
                                              b4_image.RasterYSize)
    n = b8_image.GetRasterBand(1).ReadAsArray(0, 0, b8_image.RasterXSize, \
                                              b8_image.RasterYSize)
    r = r.astype(t)
    n = n.astype(t)
    r = r / 10000
    n = n / 10000
    np.seterr(invalid='ignore')
    ndvi = (n - r) / (n + r)
    nan_values = np.isnan(ndvi)
    ndvi[nan_values] = -1
    output.GetRasterBand(1).WriteArray(ndvi)
    output.SetGeoTransform(transform)
    wkt = b4_image.GetProjection()
    srs = osr.SpatialReference()
    srs.ImportFromWkt(wkt)
    output.SetProjection(srs.ExportToWkt())
    b4_image = None
    b8_image = None
    output = None

