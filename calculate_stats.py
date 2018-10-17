# -*- coding: utf-8 -*-
"""
Created on 17-10-2018

@author: naroairiarte
This is the main class to execute the statistics from outside using arguments.
"""

import zonal_statistics as zs
import sys

zs.get_zonal_stats(sys.argv[1], sys.argv[2])