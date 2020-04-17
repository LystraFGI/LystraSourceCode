
import os
import numpy as np
from osgeo import gdal
import matplotlib.colors as mcolors
from PIL import Image
from matplotlib import cm
from PIL import ImageChops
from matplotlib.colors import LightSource

# create function for RGB colour scale including alpha channel
def make_colormap(seq):

    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []} #, 'alpha': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
            #cdict['alpha'].append([item, a1, a2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)

c = mcolors.ColorConverter().to_rgb #a

#elevations for color scale
values = [-200, -50, 0, 250, 400, 450]


path = '/wrk/perheent/Frames/'

fnames = []

files = os.listdir(path)

for i in files:
    a = path + i
    fnames.append(a)

fnames.sort()


for filename in fnames:
    
    read_data = gdal.Open(filename)

    read_dem = read_data.ReadAsArray()
    
    #minvalue = read_dem.min()
    wat_max = -250
    terr_max = 750
    
    dem_norm = mcolors.Normalize(vmin=wat_max,vmax=terr_max, clip=True)

    rs_dem = dem_norm(read_dem)


    scaled = []
    
    for i in values:
        new_value = dem_norm(i)
        scaled.append(new_value)

    
    #set scaled colour values
    
    cmap_dem = make_colormap(
        [c('#010071'), scaled[0], c('#010071'), c('#1f78b4'), scaled[1], c('#1f78b4'), c("#89e2ff"), scaled[2], c("#0b6e24"), c("#dfc485"), scaled[3], c("#dfc485"), c('#8d7c58'), scaled[4], c("#8d7c58"), c("#a49fa3"), scaled[5], c("#a49fa3")])  
    

    im  = Image.fromarray(np.uint8(cmap_dem(rs_dem)*255))

    
    ls = LightSource(azdeg=315, altdeg=45)

    hs = ls.hillshade(read_dem, vert_exag=0.04, fraction=1.35)

    hsimg = Image.fromarray(np.uint8(cm.gray(hs)*255))

    
    blend = ImageChops.multiply(im, hsimg)

    if len(filename) == 36:
        identifier = filename[27:32]
    elif len(filename) == 35 and filename[27] != "-":
        identifier = filename[27:31]
    elif len(filename) == 35 and filename[27] == "-":
        identifier = filename[27] + "0" + filename[28:31]
    elif len(filename) == 34 and filename[27] != "-":
        identifier = "0" + filename[27:30]
    elif len(filename) == 34 and filename[27] == "-":
        identifier = filename[27] + "00" + filename[28:30]
    elif len(filename) == 33 and filename[27] != "-":
        identifier = "00" + filename[27:29]
    elif len(filename) == 33 and filename[27] == "-":
        identifier = filename[27] + "000" + filename[28:29]
    elif len(filename) == 37 and filename[27] == "-":
        identifier = filename[27:33]
    else:
        identifier = "000" + filename[27:28]
        
    blend.save("/wrk/perheent/Future/HS_" + identifier + ".tif")
    
    