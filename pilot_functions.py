#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import h5py as h5
from pyproj import Proj,transform
from osgeo import gdal
from osgeo import osr
from math import floor
from glob import glob
import pandas as pd
import matplotlib.pyplot as plt


# In[ ]:


class readSentinel():
    
    def __init__(self,fileName):
        '''Read Sentinel2 data'''
        #dir = '/home/s1949330/Documents/initial_data'
        #bandList = glob(dir + '/*.jp2')
        #for fileName in bandList:
        ds = gdal.Open(fileName)
        proj = osr.SpatialReference(wkt = ds.GetProjection())
        self.epsg = int(proj.GetAttrValue('AUTHORITY', 1))
        self.nX = ds.RasterXSize
        self.nY = ds.RasterYSize
        transform_ds = ds.GetGeoTransform()
        self.xOrigin = transform_ds[0]
        self.yOrigin = transform_ds[3]
        self.pixelWidth = transform_ds[1]
        self.pixelHeight = transform_ds[5]
        self.data = ds.GetRasterBand(1).ReadAsArray(0, 0, self.nX, self.nY)
        return
    
    def coarsen(self,res):
        '''Coarsen resolution of non-20m Sentinel2 data'''    
        # Dimensions of output image
        newX = floor(self.nX * self.pixelWidth / res)
        newY = floor(self.nY * self.pixelHeight / (-1 * res))
        # Allocate space
        newData = np.zeros((newX,newY), dtype = float)
        contN = np.zeros((newX,newY), dtype = int)
        # Loop over input image and take rolling sum
        for i in range(0,self.nX):
            #print('Column', i , 'of', self.nX)
            for j in range(0, self.nY):
                xInd = floor(i * self.pixelWidth / res)
                yInd = floor(j * -1 * self.pixelHeight / res)
                #print(i,j,xInd,yInd,res,self.pixelWidth,self.pixelHeight)
                newData[xInd,yInd] += self.data[i,j]
                contN[xInd,yInd] += 1      
        # Normalise means
        newData[contN > 0] = newData[contN > 0] / contN[contN > 0]
        newData[contN == 0] = -999
        self.pixelWidth = res
        self.pixelHeight = -1 * res
        self.data = newData
        self.nX = self.data.shape[0]
        self.nY = self.data.shape[1]
        return

    def writeTiff(self, filename):
        '''Write geotiff for coarsened sentinel2 data'''

        # Set geolocation information
        geotransform = (self.xOrigin, self.pixelWidth, 0, self.yOrigin, 0, self.pixelHeight)
        # Load data into geotiff object
        dst_ds = gdal.GetDriverByName('GTiff').Create(filename, self.nX, self.nY, 1, gdal.GDT_Float32)
        dst_ds.SetGeoTransform(geotransform)          # Specifiy coordinates
        srs = osr.SpatialReference()                  # Establish encoding
        srs.ImportFromEPSG(self.epsg)                      # WGS84 Lat/Lon
        dst_ds.SetProjection(srs.ExportToWkt())       # Export coordinates to file
        dst_ds.GetRasterBand(1).WriteArray(self.data)  # Write image to raster
        dst_ds.GetRasterBand(1).SetNoDataValue(-999)  # Set no data value
        dst_ds.FlushCache()                           # Write to disk
        dst_ds = None
        print("Written to ", filename)
        return
        

print('Success')


# In[ ]:


class readGEDI():

    def __init__(self,fileList):
        '''Read GEDI data'''
        gedi_f = h5.File('/home/s1949330/Documents/initial_data/GEDI02_B_2020_04_30_2020124194427_O07882_01_T02809_02_003_01_V002.h5', 'r')
        beamList = ['BEAM0000','BEAM0001','BEAM0010','BEAM0011','BEAM0101','BEAM0110','BEAM1000','BEAM1011']           
        self.x = np.empty((), dtype = float)
        self.y = np.empty((), dtype = float)
        self.sens = np.empty((), dtype = float)
        self.cover = np.empty((), dtype = float)
        for beam in beamList:
            self.x = np.append(self.x, np.array(gedi_f[beam]['geolocation/lon_lowestmode']))
            self.y = np.append(self.y, np.array(gedi_f[beam]['geolocation/lat_lowestmode']))
            self.sens = np.append(self.sens, np.array(gedi_f[beam]['sensitivity']))
            self.cover = np.append(self.cover, np.array(gedi_f[beam]['cover'])) 
        return
            
    def reprojectGEDI (self,outEPSG):
        '''Reproject GEDI footprint coordinates'''
        inProj = Proj("epsg:4326")
        outProj = Proj("epsg:"+str(outEPSG))
        x, y = transform(inProj,outProj,gedi.y,gedi.x)
        gedi.x = x
        gedi.y = y
        return
    
    def dumpData(self,filename):
        '''Write GEDI and Sentinel2 (intersecting pixels) to csv'''
        f = open(filename,'w')
        for i in range(0,self.cover.shape[0]):
            if((self.cover[i] >= 0) & (self.s2out[i,0] >= 0)):
                line = str(self.cover[i]) + "," + str(self.x[i]) + "," + str(self.y[i]) + "," + str(self.sens[i])
                for j in range(0,self.s2out.shape[1]):
                    line = line + "," + str(self.s2out[i,j])
                line = line + "\n"
                f.write(line)
        f.close()
        print("Written to ",filename)
        return
    

print('Success')

