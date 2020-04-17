'''
Converts GeoTIFFs to RGB images with elevation dependent colour scale,
creates relief shading and blends them by multiplication.
'''

import os
import numpy as np
from osgeo import gdal
import matplotlib.colors as mcolors
from PIL import Image
from matplotlib import cm
from PIL import ImageChops
from matplotlib.colors import LightSource

# create function for RGB colour scale 
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
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)

c = mcolors.ColorConverter().to_rgb #a

#elevations for colour scale
values = [-200, -50, 0, 250, 400, 450]

#file path to raw GeoTIFFs
path = ''

fnames = []

files = os.listdir(path)

for i in files:
    fnames.append(path + i)

fnames.sort()

for filename in fnames:   
    read_data = gdal.Open(filename)
    read_dem = read_data.ReadAsArray()
    
    #fixed limits to fit the colour scale
    wat_max = -250
    terr_max = 750
    
    #normalize colour scale
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
    
    #create hillshade
    ls = LightSource(azdeg=315, altdeg=45)
    hs = ls.hillshade(read_dem, vert_exag=0.04, fraction=1.35)
    hsimg = Image.fromarray(np.uint8(cm.gray(hs)*255))
  
    #blend hillshade to RGB image using multiplication
    blend = ImageChops.multiply(im, hsimg)
        
    #write image to disc   
    blend.save('OUTFILEPATH.tif')
    
    
