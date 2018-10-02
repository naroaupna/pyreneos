# -*- coding: utf-8 -*-
"""
Created on Mon May 14 11:49:48 2018

@author: naroairiarte
This module executes the needed functions to get NDVI images from the raster
images stored in the given path.
"""

import calculate_mosaic as cm
import correct_images_with_mask as ciwm


def treat_images_to_obtain_NDVI(path):
    cm.calculate_mosaic(path)
    ciwm.correct_images(path, True)


treat_images_to_obtain_NDVI('/home/naroairirarte/Desktop/test_mosaic')