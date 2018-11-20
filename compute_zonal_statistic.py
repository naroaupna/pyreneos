# -*- coding: utf-8 -*-
"""
Created on Mon May 14 11:49:48 2018

@author: naroairiarte
This module executes the statisticts of a year.
"""

import zonal_statistics as zs
import sys

zs.get_zonal_stats(sys.argv[1], sys.argv[2])
