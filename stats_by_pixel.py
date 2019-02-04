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
import time


raster_path = '/home/naroairirarte/Desktop/prueba'

def stats_by_pixel(raster_path, shapefile):
    d = defaultdict(list)
    old_id_list = []
    pixel_count = 0
    parcel_mean = 0
    new_parcel_mean = 0
    #rasterized = False

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
        #TODO: esto hay que borrar porque estoy creando una matriz aleatoria con el tamaño del raster solo para hacer
        # como que es el raster del shape y testear el codigo
        shp_matrix = np.random.randint(500, size=(rows, cols))
        id = shp_matrix[0][0]
        shp = shp_matrix.shape
        shp_rows = shp[0]
        shp_cols = shp[1]
        #Aunque esto de arriba es redundante lo hago porque puede que tenga que recorrerlo independientemente
        date = cfdf.get_image_date(raster)
        # Lo de la id va a ser recorriendo el raster sacado del shape...
        old_id_list.append(id)
        image_id = id
        #parcel_mean = array_image[0][0]
        #Cacho de codigo para calcular el coste temporal de recorrer y calcular
        start = time.time()
        #TODO: aqui empiezo a recorrer mi raster de shape a la vez, es decir que creo que coinciden
        for c in range(cols - 1):
            for r in range(rows - 1):
                image_id = shp_matrix[r][c]
                if image_id in old_id_list:
                    #ir haciendo count++ e ir sumando los valores de pixel para hacer la media
                    #tambien cualquiera que sea la formula de la desviacion standar
                    #TODO: aqui necesito reasignar la id con la del raster, es decir, avanzar el array del raster shp y
                    #reasignar el image_id
                    pixel_count += 1
                    new_parcel_mean = array_image[r][c] + parcel_mean
                    parcel_mean = new_parcel_mean
                    old_id_list.append(image_id)
                else:
                    #En este punto ya tenemos que la id ha cambiado, hay que guardar en el diccionario el count y media de
                    # la parcela, con su id y fecha
                    # Definir la estructura: id, count, mean, fecha o algo así
                    data_tuple = []
                    data_tuple.append(date)
                    data_tuple.append(pixel_count)
                    final_mean = parcel_mean/pixel_count
                    data_tuple.append(final_mean)
                    #TODO: como es una nueva parcela, no podemos olvidar que el count es 1 no 0 y el parcel mean hay que
                    #calcularlo como arriba
                    pixel_count = 1
                    parcel_mean = array_image[r][c]
                    d[old_id_list[-1]] = data_tuple
                    old_id_list.append(image_id)
        #TODO: aqui ya el posttratamiento para meter el ultimo
        data_tuple = []
        data_tuple.append(date)
        data_tuple.append(pixel_count)
        final_mean = parcel_mean / pixel_count
        data_tuple.append(final_mean)
        d[old_id_list[-1]] = data_tuple
        old_id_list.append(image_id)
        end = time.time()
        print(end - start)
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