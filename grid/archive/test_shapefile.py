from io import BytesIO as StringIO
import shapefile
import numpy
import rasterio
import rasterio.mask
import fiona
import os


os.chdir("/Users/jameschen/Dropbox/photo_grid/data/shapefile")

file_sf = shapefile.Reader("IPNI_N_Trial_overlay.shp")
file_fi = fiona.open("IPNI_N_Trial_overlay.shp", "r")
len(file_sf)
i = 150
file_fi[i]

file_sf.record(0)
rec = file_sf.shapeRecords()
rec[i].__dict__
rec[i].record
rec[i].shape.points
rec[i].shape.__dict__


file_sf[i].point
file_sf.bbox
print(file_sf)

# writer
w = shapefile.Writer("test")
w.field('id', 'C', 20, 20)
w.field("mean", 'N', 8, 3)
# w.field('name2', 'C')
w.poly([[[122, 37], [117, 36], [115, 32], [118, 20], [113, 24]]])
w.record(**dict({'id': 'polygon2', "mean": 3.525}))
w.poly([[[122, 37], [118, 36], [105, 32], [118, 23], [113, 24]]])
w.record(**dict({'id': 'polygon2', "mean": 3.525}))
w.close()

r = shapefile.Reader('test')
r.record(0)
r.shapeRecords()[0].shape.points
r.record(1)

r.close()

r.__dict__


# fiona
ftest = fiona.open("/Users/jameschen/GRID.shp", "r")
ftest.__dict__
ftest[0]
ftest.close()

file_fi.__dict__
np.array(file_fi[0]["geometry"]["coordinates"][0]).round()


######

# imports
from scipy.stats import pearsonr
from sklearn.linear_model import LogisticRegressionCV, LogisticRegression
from sklearn.datasets import load_iris
from sklearn.mixture import GaussianMixture
from matplotlib.path import Path
from sklearn.cluster import KMeans
from scipy.signal import find_peaks
from scipy.signal import convolve2d
import grid as gd
from PIL import Image
import os
import sys
import numpy as np
import pandas as pd
import h5py as h5
import cv2
import random
import warnings
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

warnings.filterwarnings("ignore")

# global params
_RGB = (68, 51, 17)
_HOME = os.path.expanduser("~")

# self imports
os.chdir(os.path.join(_HOME, "Dropbox", "James_Git"))
import os
os.chdir("..")
sys.path
sys.path.remove("/Users/jameschen/Dropbox/photo_grid/grid")
import grid as gd

# load image
grid = gd.GRID()
grid.loadData(
    "/Users/jameschen/Dropbox/James Chen/Projects/GRID/Prototype/GRID_Demo_Croped.jpg")
grid.binarizeImg(k=3, features=[0, 1],
                 lsSelect=[0],
                 valShad=10, valSmth=5, outplot=True)
grid.findPlots(nRow=23, nCol=12)
grid.cpuSeg(outplot=True)

grid.save(prefix="test")


imgH = grid.map.imgH
imgW = grid.map.imgW

dt = pd.read_csv("~/test_data.csv")
cols = dt.columns

for col in cols:
    instance = dt[col][0]

    if isinstance(instance, object):
        # characters
        mode = "C"
        arg1, arg2 = 20, 20
    else:
        # integer, floating
        mode = "N"
        arg1, arg2 = 10, 10

    f.field(col, mode, arg1, arg2)

for idx, entry in dt.iterrows():
    # get agents
    row = entry["row"]
    col = entry["col"]
    agent = grid.agents.get(row, col)

    # polygon
    bN = imgH - agent.border["NORTH"]
    bW = agent.border["WEST"]
    bS = imgH - agent.border["SOUTH"]
    bE = agent.border["EAST"]
    f.poly([[[bW, bN], [bE, bN], [bE, bS], [bW, bS], [bW, bN]]])

    # attributes
    dc = {c: entry[c] for c in dt.columns}
    f.record(**dict(dc))


