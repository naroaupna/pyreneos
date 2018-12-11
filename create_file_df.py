# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 10:10:22 2018

@author: naroairiarte
This module creates a dataframe with the important data of the raster images
stored in the given path.
"""

import pandas as pd
import os


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
JP2 = '.jp2'
TIFF = '.tiff'



def create_df(path):
    """ This function generates a dataframe fulfilled with the info about the images stored in the given path.

    :param path (String): The path where all the images are stored.
    :return: image_df (pandas.DataFrame): A dataframe containing all the interesting information about the images.
    """
    cols = ['file', 'path_to_image', 'band', 'date']
    image_df = pd.DataFrame(columns=cols)
    for root, dirs, files in os.walk(path):
        for fil in files:
            file_extension = os.path.splitext(fil)[1]
            if ((file_extension == JP2) or (file_extension == TIFF)) and not (BAND_SCL in fil):
                properties = []
                image_path = os.path.join(root, fil)
                image_band = get_image_band(fil)
                image_date = get_image_date(fil)
                properties.append(fil)
                properties.append(image_path)
                properties.append(image_band)
                properties.append(image_date)
                df_row = pd.DataFrame([properties], columns=cols)
                image_df = image_df.append(df_row, ignore_index=True)
            elif (BAND_SCL in fil):
                properties = []
                image_path = os.path.join(root, fil)
                image_band = BAND_SCL
                image_date = get_image_date(fil)
                properties.append(fil)
                properties.append(image_path)
                properties.append(image_band)
                properties.append(image_date)
                df_row = pd.DataFrame([properties], columns=cols)
                image_df = image_df.append(df_row, ignore_index=True)
    return image_df


def get_image_band(filename):
    """ This function finds out the band of the given image.

    :param filename (String): the name of the file.
    :return: band (String): The band tho which the imagen belongs.
    """
    if (BAND_02 in filename) and (TEN_METERS in filename):
        band = '02'
    elif (BAND_03 in filename) and (TEN_METERS in filename):
        band = '03'
    elif (BAND_04 in filename) and (TEN_METERS in filename):
        band = '04'
    elif (BAND_05 in filename):
        band = '05'
    elif (BAND_06 in filename):
        band = '06'
    elif (BAND_07 in filename):
        band = '07'
    elif (BAND_08 in filename):
        band = '08'
    elif (BAND_8A in filename):
        band = '8A'
    elif (BAND_11 in filename):
        band = '11'
    elif (BAND_12 in filename):
        band = '12'
    else:
        band = 'none'
    return band


def get_image_date(filename):
    """

    :param filename (String): The name of the file.
    :return: date (String): The date when the image was captured in the format YYYYMMDDTHHMMSS.
    """
    if ('S2A_USER' in filename):
        ind = filename.replace('_', 'X', 6).find('_')
        filename_middle = filename[ind + 1:]
        ind_2 = filename_middle.find('_')
        date = filename_middle[:ind_2]
    elif (('2017' in filename) or ('2018' in filename)) and ('L2A' not in filename):
        ind = filename.replace('_', 'X', 1).find('X')
        filename_middle = filename[ind + 1:]
        ind_2 = filename_middle.find('_')
        date = filename_middle[:ind_2]
    else:
        ind = filename.replace('_', 'X', 1).find('_')
        filename_middle = filename[ind + 1:]
        ind_2 = filename_middle.find('_')
        date = filename_middle[:ind_2]
    return date

