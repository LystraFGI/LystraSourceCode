
from osgeo import gdal
import numpy as np

data = gdal.Open(fp_DEM_0)

dem = data.ReadAsArray()

data2 = gdal.Open(fp_U_0)

anc = data2.ReadAsArray()

a = 9.4000712009755716E+03
b = 3.2624206787165413E+03
c = 7.4006662440556579E+02

scale10458bp = a * (np.exp(10458/b) -1) + c

for i in range(-10000, 0, 5):
    scale_factor =  (a * (np.exp(-i/b) -1) + c) / scale10458bp
    uusi = dem - anc * scale_factor
    array2raster(outfilepath + str(i) + ".tif", data, uusi, "Float32")
