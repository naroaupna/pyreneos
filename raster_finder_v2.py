# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 12:45:39 2018

@author: ion sola & Naroa Iriarte

This functions finds the raster images inside a given directory path.
"""

import os


def find_rasters(path):
    """ This function finds the raster images in a given path an returns the
        path to the found raster image.
    args:
        path (string): This is the path where all the images are stored.
    returns:
        string: a path to raster image as a string.
    """
    for root, dirs, files in os.walk(path):
        for f in files:
            if valid_image_condition(f):
                yield os.path.join(root, f)


def valid_image_condition(image_name):
    return ((('.jp2' in image_name) and ('AOT' not in image_name) and ('SCL' not in image_name) and
            ('TCI' not in image_name) and ('WVP' not in image_name) and ('VIS' not in image_name)))
