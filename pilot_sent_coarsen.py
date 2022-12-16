#!/usr/bin/env python
# coding: utf-8

# In[22]:


import numpy as np
import h5py as h5
from pyproj import Proj,transform
from osgeo import gdal
from osgeo import osr
from math import floor
from glob import glob
import pandas as pd
import matplotlib.pyplot as plt


# In[26]:


# Read & Coarsen Sentinel2 bands
sentList = ['/home/s1949330/Documents/initial_data/T36LWK_A025400_20200503T075551_B01.jp2', 
            '/home/s1949330/Documents/initial_data/T36LWK_A025400_20200503T075551_B02.jp2', 
            '/home/s1949330/Documents/initial_data/T36LWK_A025400_20200503T075551_B03.jp2',
            '/home/s1949330/Documents/initial_data/T36LWK_A025400_20200503T075551_B04.jp2',
            '/home/s1949330/Documents/initial_data/T36LWK_A025400_20200503T075551_B05.jp2',
            '/home/s1949330/Documents/initial_data/T36LWK_A025400_20200503T075551_B06.jp2',
            '/home/s1949330/Documents/initial_data/T36LWK_A025400_20200503T075551_B07.jp2',
            '/home/s1949330/Documents/initial_data/T36LWK_A025400_20200503T075551_B08.jp2',
            '/home/s1949330/Documents/initial_data/T36LWK_A025400_20200503T075551_B09.jp2',
            '/home/s1949330/Documents/initial_data/T36LWK_A025400_20200503T075551_B11.jp2',
            '/home/s1949330/Documents/initial_data/T36LWK_A025400_20200503T075551_B12.jp2',
            '/home/s1949330/Documents/initial_data/T36LWK_A025400_20200503T075551_B08A.jp2']

oldDir='/home/s1949330/Documents/initial_data/'
newDir='/home/s1949330/Documents/coarsened_data/'

# Write (coarsened) Sentinel2 data as geotiffs
for inFile in sentList:
    # Reading
    sent = readSentinel(inFile)
    useData=True
    if sent.pixelWidth == 60:
        useData = False
    elif sent.pixelWidth == 10:
    # Coarsening
        sent.coarsen(20)
    # Writing
    if(useData):
        outFile = inFile.replace(oldDir,newDir)
        sent.writeTiff(outFile)


# In[1]:


sentList20 = ['/home/s1949330/Documents/coarsened_data/T36LWK_A025400_20200503T075551_B02.jp2', 
              '/home/s1949330/Documents/coarsened_data/T36LWK_A025400_20200503T075551_B03.jp2',
              '/home/s1949330/Documents/coarsened_data/T36LWK_A025400_20200503T075551_B04.jp2',
              '/home/s1949330/Documents/coarsened_data/T36LWK_A025400_20200503T075551_B05.jp2', 
              '/home/s1949330/Documents/coarsened_data/T36LWK_A025400_20200503T075551_B06.jp2',
              '/home/s1949330/Documents/coarsened_data/T36LWK_A025400_20200503T075551_B07.jp2',
              '/home/s1949330/Documents/coarsened_data/T36LWK_A025400_20200503T075551_B08.jp2',
              '/home/s1949330/Documents/coarsened_data/T36LWK_A025400_20200503T075551_B11.jp2',
              '/home/s1949330/Documents/coarsened_data/T36LWK_A025400_20200503T075551_B12.jp2']


i = 0
for filename in sentList20:
    sent20 = readSentinel(filename)
    i = i + 1
    

