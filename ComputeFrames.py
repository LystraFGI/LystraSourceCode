'''
Computes ancient elevation models based on present day DEM and total occured land uplift derived from
current land uplift rates and shoreline isobases by scaling the data with formula of exponential relaxation.
'''

from osgeo import gdal
import numpy as np
from tiftools import array2raster

#filepaths to DEM_0 and U_0
fp_DEM_0 = ''
fp_U_0 = ''

#present-day elevation and bathymetry
dataDEM = gdal.Open(fp_DEM_0)
dem = dataDEM.ReadAsArray()

#raster of occured land uplift since the Ancylus Lake stage
dataU = gdal.Open(fp_U_0)
anc = dataU.ReadAsArray()

#constants obtained from exponential fit
a = 9.4000712009755716E+03
b = 3.2624206787165413E+03
c = 7.4006662440556579E+02

#scale denominator
scale10458bp = a * (np.exp(10458/b) -1) + c

#compute frames with given timeframe and timestep
for i in range('STARTYEAR', 'ENDYEAR', 5):
    scale_factor =  (a * (np.exp(-i/b) -1) + c) / scale10458bp
    newDEM = dem - anc * scale_factor
    array2raster('outfilepath' + str(i) + ".tif", dataDEM, newDEM, "Float32")
