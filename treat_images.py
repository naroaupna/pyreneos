# -*- coding: utf-8 -*-
"""
Created on Mon May 14 11:49:48 2018

@author: naroairiarte
This module executes the needed functions to get NDVI images from the raster
images stored in the given path.
"""

import calculate_mosaic as cm
import correct_images_with_mask as ciwm
import sys


cm.calculate_mosaic(sys.argv[1])
ciwm.correct_images(sys.argv[1], True)
