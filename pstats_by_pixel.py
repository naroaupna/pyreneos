# -*- coding: utf-8 -*-
"""
Created on 11-01-2019

@author: naroairiarte
"""


import time
import numpy as np
from osgeo import gdal, osr
import raster_finder_v2 as rf
import create_file_df as cfdf
from collections import defaultdict
import rasterize_shapefile as rs



raster_path = '/home/naroairirarte/Desktop/prueba'

#Path al que va la imagen
def stats_by_pixel(raster_path, shapefile):
    id = 1
    d = defaultdict(list)
    pixel_count = 0
    parcel_mean = 0
    new_parcel_mean = 0
    rasterized = False
    #TODO: lo primero sera hacer el raster desde el shape.
    for raster in rf.find_rasters(raster_path):
        #TODO: aqui quiero llamar al rasterize, pero solo una vez, y aunque sea cutre, voy a usar un flag booleano
        #if (rasterized == False):
            #array_shapefile = rs.rasterize_shp(raster, shapefile)
            #rasterized = True
        #TODO: algo con la mascara no se donde ni que
        #if ('_20m' in raster):
        #    array_image = get_resampled_array_image(raster)
        #    #print('Tamaño de las de 20 metros resampleada: ')
        #    #print(array_image.shape)
        #else:
        image = gdal.Open(raster, gdal.GA_Update)
        array_image = (image.GetRasterBand(1)).ReadAsArray()
            #print('Tamaño de las de 10metros: ')
            #print(array_image.shape)
        shape = array_image.shape
        rows = shape[0]
        cols = shape[1]
        date = cfdf.get_image_date(raster)

        #start = time.time()
        #TODO:nueva manera para ir guardando solo lo importante
        # Lo de la id va a ser recorriendo el raster sacado del shape...
        image_id = id
        old_id = image_id
        parcel_mean = array_image[0][0]
        for c in range(cols - 1):
            for r in range(rows - 1):
                if image_id == old_id:
                    #ir haciendo count++ e ir sumando los valores de pixel para hacer la media
                    #tambien cualquiera que sea la formula de la desviacion standar
                    #TODO: aqui necesito reasignar la id con la del raster
                    pixel_count += 1
                    new_parcel_mean = array_image[r][c] + parcel_mean
                    parcel_mean = new_parcel_mean
                else:
                    #En este punto ya tenemos que la id ha cambiado, hay que guardar en el diccionario el count y media de
                    # la parcela, con su id y fecha
                    # Definir la estructura: id, count, mean, fecha o algo así
                    data_tuple = []
                    data_tuple.append(date)
                    data_tuple.append(pixel_count)
                    final_mean = parcel_mean/pixel_count
                    data_tuple.append(final_mean)
                    pixel_count = 0
                    parcel_mean = 0
                    d[old_id] = data_tuple
                    old_id = image_id

        print(d)



def get_resampled_array_image(raster):
    raster_name = raster.replace('.jp2', 'resampled.jp2')
    raster_image = gdal.Open(raster, gdal.GA_Update)
    if raster_image is None:
        print('Raster image could not be opened...')
        print('Exiting the program...')
    band = raster_image.GetRasterBand(1)
    raster_array = band.ReadAsArray()
    drv = gdal.GetDriverByName("MEM")
    dst_ds = drv.Create("", raster_image.RasterXSize, raster_image.RasterYSize, \
                        1, gdal.GDT_UInt16)
    dst_ds.SetGeoTransform(raster_image.GetGeoTransform())
    dst_ds.SetProjection(raster_image.GetProjectionRef())
    dst_ds.GetRasterBand(1).WriteArray(raster_array)
    geoT = raster_image.GetGeoTransform()
    drv = gdal.GetDriverByName("GTiff")
    resampled_image = drv.Create(raster_name, \
                                 raster_image.RasterXSize * 2, raster_image.RasterYSize * 2, 1, gdal.GDT_UInt16)
    this_geoT = (geoT[0], geoT[1] / 2, geoT[2], geoT[3], \
                 geoT[4], geoT[5] / 2)
    resampled_image.SetGeoTransform(this_geoT)
    resampled_image.SetProjection(raster_image.GetProjectionRef())
    gdal.RegenerateOverviews(dst_ds.GetRasterBand(1), \
                             [resampled_image.GetRasterBand(1)], 'mode')
    resampled_image.GetRasterBand(1).SetNoDataValue(0)
    resampled_array = resampled_image.ReadAsArray()
    resampled_image = None
    return resampled_array


stats_by_pixel(raster_path, '')