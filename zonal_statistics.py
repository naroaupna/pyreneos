# -*- coding: utf-8 -*-
"""
Created on 14-08-2018

@author: naroairiarte

This program has been created to compute all the stats of the NDVI images.
"""


from rasterstats import zonal_stats
import raster_finder as rf
import os
import pandas as pd
import geopandas as gpd

def get_zonal_stats(path_to_shape, path_to_rasters):
    """
    This function calculates the zonal statistics of the polygons contained in the shapefile.
    :param path_to_shape: Path where the shapefile is stored.
    :param path_to_raster: Path where the raster images are stored.
    """
    data = gpd.read_file(path_to_shape)
    working_zones = data.copy()
    for raster in rf.find_rasters(path_to_rasters):
        if ('S1A' in raster):
            metrics = "median std count".split()
            stats = zonal_stats(path_to_shape, raster, stats=metrics)
            raster_name = os.path.basename(raster)
            raster_date = _get_raster_date(raster_name)
            band = _get_raster_band(raster_name)
            new_colnames = ["{}{}".format(raster_date, metric[:1] + band) for metric in metrics]
            df = pd.DataFrame(stats)
            df2 = df.rename(columns=dict(zip(metrics, new_colnames)))
            working_zones = working_zones.join(df2)
        else:
            metrics = "mean std count".split()
            if _is_image_to_calculate_stats(raster):
                print('Este es el raster para el que esta calculando stats: ')
                print(raster)
                stats = zonal_stats(path_to_shape, raster, stats=metrics)
                raster_name =  os.path.basename(raster)
                raster_date = _get_raster_date(raster_name)
                band = _get_raster_band(raster_name)
                new_colnames = ["{}{}".format(raster_date, metric[:1] + band) for metric in metrics]
                df = pd.DataFrame(stats)
                df2 = df.rename(columns=dict(zip(metrics, new_colnames)))
                working_zones = working_zones.join(df2)
    path_to_new_shape = path_to_shape.replace('.shp', '_with_stats.shp')
    working_zones.__class__ = gpd.GeoDataFrame
    working_zones.set_geometry('geometry')
    working_zones.to_file(path_to_new_shape, driver='ESRI Shapefile')


def _get_raster_date(raster_name):
    if ('S1' in raster_name):
        raster_date = raster_name[12:18]
    else:
        raster_date = raster_name[2:8]
    return raster_date


def _get_raster_band(raster_name):
    filename, _ = os.path.splitext(raster_name)
    band_number_index = filename.rfind('_')
    band = filename[band_number_index+1:]
    if ('NDVI' in band):
        band = 'N'
    return band


def _is_image_to_calculate_stats(raster):
    return ('rmasked_B05' in raster) or ('rmasked_B06' in raster) or ('rmasked_B07' in raster) or \
           ('rmasked_B8A' in raster) or ('rmasked_B11' in raster) or ('rmasked_B12' in raster) or \
           ('_masked_B02' in raster) or ('_masked_B03' in raster) or \
           ('_masked_B04' in raster) or ('_NDVI' in raster)


get_zonal_stats('/home/naroairirarte/Desktop/stats/Dec16_V181003_buffer5m.shp', '/home/naroairirarte/Desktop/stats')