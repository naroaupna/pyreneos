# -*- coding: utf-8 -*-
"""
Created on 18-01-2019

@author: naroairiarte
"""

from osgeo import ogr, gdal
import subprocess



outputImage = 'Result.tif'
gdalformat = 'GTiff'


def rasterize_shp(refImage, inputVector):
    #Ref image se la voy a pasar al programa, cualquiera al recorrer
    datatype = gdal.GDT_Byte
    burnVal = 1 #value for the output image pixels
    ##########################################################
    # Get projection info from reference image
    image = gdal.Open(refImage, gdal.GA_ReadOnly)

    # Open Shapefile
    Shapefile = ogr.Open(inputVector)
    Shapefile_layer = Shapefile.GetLayer()

    # Rasterise
    print("Rasterising shapefile...")
    Output = gdal.GetDriverByName(gdalformat).Create(outputImage, image.RasterXSize, image.RasterYSize, 1, datatype, options=['COMPRESS=DEFLATE'])
    Output.SetProjection(image.GetProjectionRef())
    Output.SetGeoTransform(image.GetGeoTransform())

    # Write data to band 1
    Band = Output.GetRasterBand(1)
    Band.SetNoDataValue(0)
    gdal.RasterizeLayer(Output, [1], Shapefile_layer, burn_values=[burnVal])

    # Close datasets
    Band = None
    Output = None
    image = None
    Shapefile = None

    # Build image overviews
    subprocess.call("gdaladdo --config COMPRESS_OVERVIEW DEFLATE "+outputImage+" 2 4 8 16 32 64", shell=True)
    raster_array = Output.ReadAsArray()
    print("Done.")
    return raster_array