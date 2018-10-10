# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 12:35:32 2018

@author: naroairiarte

This module is implemented to create the mosaic of the raster images of
TWM, TWN, TXM and TXN tiles.
"""

import os
import create_file_df as cfdf
from osgeo import gdal
import sys


BAND_02 = 'B02'
BAND_03 = 'B03'
BAND_04 = 'B04'
BAND_05 = 'B05'
BAND_06 = 'B06'
BAND_07 = 'B07'
BAND_08 = 'B08'
BAND_8A = 'B8A'
BAND_11 = 'B11'
BAND_12 = 'B12'
BAND_SCL = 'SCL'
TEN_METERS = '_10m'
TWENTY_METERS = '_20m'
XML = '.xml'
JP2 = '.jp2'
YEAR_2017 = '/2017'
YEAR_2016 = '/2016'



def calculate_mosaic(path):
    """ Generates the mosaic of all the bands, it is needed to resample the bands which are at 20 meters.
    args:
        path (string): This is the path where all the images are stored.
    """
    dataFrame = cfdf.create_df(path)
    dataFrame_copy = dataFrame.copy()
    path_band04, path_band08, path_band03, path_band05, path_band02, path_band06, path_band07, path_band8A, \
    path_band11, path_band12, path_band_SCL = _obtain_path_arrays(dataFrame_copy)
    _generate_quartets(path_band02, BAND_02)
    _generate_quartets(path_band03, BAND_03)
    _generate_quartets(path_band04, BAND_04)
    _generate_quartets(path_band05, BAND_05)
    _generate_quartets(path_band06, BAND_06)
    _generate_quartets(path_band07, BAND_07)
    _generate_quartets(path_band08, BAND_08)
    _generate_quartets(path_band8A, BAND_8A)
    _generate_quartets(path_band11, BAND_11)
    _generate_quartets(path_band12, BAND_12)
    _generate_bandSCL_quartets(path_band_SCL)



def _obtain_path_arrays(df):
    """ Obtains the path to the images stored in the dataframe.
    Returns lists one containing the path to the elements of the
    bands.
    """
    path_array_band08 = []
    path_array_band04 = []
    path_array_band03 = []
    path_array_band05 = []
    path_array_band02 = []
    path_array_band06 = []
    path_array_band07 = []
    path_array_band8A = []
    path_array_band11 = []
    path_array_band12 = []
    path_array_SCLband = []
    for index, row in df.iterrows():
        actual_band = row['band']
        path_to_file = df.get_value(index, 'path_to_image')
        if (actual_band == '04' and TEN_METERS in path_to_file):
            path_array_band04.append(path_to_file)
        elif (actual_band == '08' and TEN_METERS in path_to_file):
            path_array_band08.append(path_to_file)
        elif (actual_band == '03' and TEN_METERS in path_to_file):
            path_array_band03.append(path_to_file)
        elif (actual_band == '05' and TWENTY_METERS in path_to_file):
            path_array_band05.append(path_to_file)
        elif (actual_band == '02' and TEN_METERS in path_to_file):
            path_array_band02.append(path_to_file)
        elif (actual_band == '06' and TWENTY_METERS in path_to_file):
            path_array_band06.append(path_to_file)
        elif (actual_band == '07' and TWENTY_METERS in path_to_file):
            path_array_band07.append(path_to_file)
        elif (actual_band == '8A' and TWENTY_METERS in path_to_file):
            path_array_band8A.append(path_to_file)
        elif (actual_band == '11' and TWENTY_METERS in path_to_file):
            path_array_band11.append(path_to_file)
        elif (actual_band == '12' and TWENTY_METERS in path_to_file):
            path_array_band12.append(path_to_file)
        elif (actual_band == BAND_SCL):
            path_array_SCLband.append(path_to_file)
    return path_array_band04, path_array_band08, path_array_band03, path_array_band05, path_array_band02,\
           path_array_band06, path_array_band07, path_array_band8A, \
           path_array_band11, path_array_band12, path_array_SCLband



def _generate_quartets(band_path, band):
    """ This function generates lists of 4 elements which are the tiles that
    will be used to generate the mosaic, and when the four images are found,
    the function to generate the mosaic is invoked.
    """
    images_for_mosaic = []
    for i in range(len(band_path)):
        if (band_path[i] == 'deleted'):
            continue
        else:
            images_for_mosaic.append(band_path[i])
            actual_date = cfdf.get_image_date(os.path.basename(band_path[i]))
            for j in range(i + 1, len(band_path)):
                if ((actual_date in band_path[j]) and
                        (band in band_path[j]) and
                        (XML not in band_path[j])):
                    images_for_mosaic.append(band_path[j])
                    band_path[j] = 'deleted'
                if len(images_for_mosaic) == 4:
                    _generate_mosaic(images_for_mosaic)
                    del images_for_mosaic[:]
                    break


def _generate_bandSCL_quartets(path_SCL_band):
    """ This function generates the mosaic of the SCL files.
    """
    images_for_mosaic = []
    for i in range(len(path_SCL_band)):
        if (path_SCL_band[i] == 'deleted'):
            continue
        elif ((BAND_SCL in path_SCL_band[i]) and
                  (XML not in path_SCL_band[i]) and
                  (TWENTY_METERS in path_SCL_band[i])):
            images_for_mosaic.append(path_SCL_band[i])
            actual_date = cfdf.get_image_date(os.path.basename(
                path_SCL_band[i]))
            for j in range(i + 1, len(path_SCL_band)):
                if ((actual_date in path_SCL_band[j]) and
                        (BAND_SCL in path_SCL_band[j]) and
                        (XML not in path_SCL_band[j]) and
                        (TWENTY_METERS in path_SCL_band[j])):
                    images_for_mosaic.append(path_SCL_band[j])
                    path_SCL_band[j] = 'deleted'
                if len(images_for_mosaic) == 4:
                    _generate_mosaic(images_for_mosaic)
                    del images_for_mosaic[:]
                    break
        else:
            continue


def _get_filename(path):
    """ This function gets the filename of a complete path name.
    """
    directory = ''
    if (YEAR_2017 in path):
        directory = os.path.dirname(os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(path))))))
    elif ((YEAR_2016 in path) and ('image_SCL' not in path)):
        directory = os.path.dirname(os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(path)))))
    elif ((YEAR_2016 in path) and ('image_SCL' in path)):
        directory = os.path.dirname(os.path.dirname(
            os.path.dirname(
                os.path.dirname(path))))
    return directory


def _generate_mosaic(array_of_quartet):
    """ This function generates a mosaic image based on the four images
    contained in the array which the function needs as argument.
    """
    if (BAND_04 + TEN_METERS in array_of_quartet[1]):
        raster_name = os.path.basename(array_of_quartet[1])
        filename = _generate_filename(BAND_04, raster_name)
    elif (BAND_08 + TEN_METERS in array_of_quartet[1]):
        raster_name = os.path.basename(array_of_quartet[1])
        filename =_generate_filename(BAND_08, raster_name)
    elif (BAND_SCL in array_of_quartet[1]):
        raster_name = os.path.basename(array_of_quartet[1])
        filename =_generate_filename(BAND_SCL, raster_name)
    elif (BAND_03 + TEN_METERS in array_of_quartet[1]):
        raster_name = os.path.basename(array_of_quartet[1])
        filename =_generate_filename(BAND_03, raster_name)
    elif (BAND_05 + TWENTY_METERS in array_of_quartet[1]):
        raster_name = os.path.basename(array_of_quartet[1])
        filename =_generate_filename(BAND_05, raster_name)
    elif (BAND_02 + TEN_METERS in array_of_quartet[1]):
        raster_name = os.path.basename(array_of_quartet[1])
        filename =_generate_filename(BAND_02, raster_name)
    elif (BAND_06 + TWENTY_METERS in array_of_quartet[1]):
        raster_name = os.path.basename(array_of_quartet[1])
        filename =_generate_filename(BAND_06, raster_name)
    elif (BAND_07 + TWENTY_METERS in array_of_quartet[1]):
        raster_name = os.path.basename(array_of_quartet[1])
        filename =_generate_filename(BAND_07, raster_name)
    elif (BAND_8A + TWENTY_METERS in array_of_quartet[1]):
        raster_name = os.path.basename(array_of_quartet[1])
        filename =_generate_filename(BAND_8A, raster_name)
    elif (BAND_11 + TWENTY_METERS in array_of_quartet[1]):
        raster_name = os.path.basename(array_of_quartet[1])
        filename =_generate_filename(BAND_11, raster_name)
    elif (BAND_12 + TWENTY_METERS in array_of_quartet[1]):
        raster_name = os.path.basename(array_of_quartet[1])
        filename =_generate_filename(BAND_12, raster_name)
    filename_path = os.path.dirname(array_of_quartet[1])
    output_path = _get_filename(os.path.join(filename_path, filename))
    output_intermediate_filename = os.path.basename(filename)
    output_filename = os.path.basename(output_intermediate_filename)
    output_filename_path = os.path.join(output_path, output_filename)
    _create_mosaic(output_filename_path, array_of_quartet)


def _generate_filename(band, element):
    """ This function generates the filename which will be used to create the output path.
    """
    date = cfdf.get_image_date(element)
    filename = date + '_mosaic_image_' + band + JP2
    return filename


def _create_mosaic(output_filename, array_of_quartet):
    """ This function creates the mosaic using a gdal function.
    """
    os.system('gdal_merge.py -o ' + output_filename + ' ' + array_of_quartet[0]
              + ' ' + array_of_quartet[1] + ' ' + array_of_quartet[2] + ' ' + array_of_quartet[3])