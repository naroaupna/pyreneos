# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 12:45:39 2018

@author: ion sola

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
            if (('.jp2' in (os.path.splitext(f)[1])) or ('.tif' in (os.path.splitext(f)[1]))):
                yield os.path.join(root, f)