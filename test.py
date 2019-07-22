# /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages
cp /Users/jameschen/Dropbox/photo_grid/photo_grid/*.py /Users/jameschen/Dropbox/photo_grid/env/lib/python3.6/site-packages/photo_grid/
# sudo cp /Users/jameschen/Dropbox/photo_grid/photo_grid/*.py /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/photo_grid/


import photo_grid
photo_grid.run()

''' TEST IMAGE LOADING '''
import cv2
import rasterio
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
Image.MAX_IMAGE_PIXELS = 1e+9

path = "/Users/jameschen/Dropbox/James Chen/GRID/Prototype/AlfalfaHT.png"
path = "/Users/jameschen/Dropbox/James_Git/alfalfa_gis/data/img&map/alfalfa_0505/alfalfa_0505.tif"
path = "/Users/jameschen/Dropbox/Stick/JamesTest/Pullman/20190530_2_100feet_RGB.tif"
path = "/Users/jameschen/Dropbox/James Chen/GRID/Prototype/330pm_120ft_05_05_2019_Cherry C.jpg"

ras = rasterio.open(path)
nCh = ras.count
img_np = np.zeros((ras.height, ras.width, nCh))
for i in range(nCh):
    img_np[:,:,i] = ras.read(i+1)

img_np = img_np.astype(np.uint8)

plt.imshow(img_np)
plt.show()


''' TEST OUTPUT '''
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json, os, sys
from PyQt5.QtWidgets import QApplication
import photo_grid
import cv2
import rasterio
os.chdir("/Users/jameschen/Dropbox/James_Git")
params = dict()
params['anchors'] = json.load(open('anchors'))
params['nc'] = 26
params['nr'] = 4
# params['nc'] = 12
# params['nr'] = 23
# params['map'] = pd.DataFrame(np.load("map.npy", allow_pickle=True))
params['map'] = None
params['bin'] = np.load("img_bin.npy")
params['crop'] = np.load("img_crop.npy")
params['k'] = np.load("img_k.npy")
params['ls_bin'] = np.load("ls_bin.npy")
params['ch_nir'] = 1
params['ch_red'] = 0
app = QApplication(sys.argv)
pn_main = photo_grid.Panel_Output(**params)



#
# ==== row:8, col:0 ====
# {'NORTH': 293, 'SOUTH': 307, 'WEST': 0, 'EAST': 61}
#
# ==== row:9, col:0 ====
# {'NORTH': 179, 'SOUTH': 188, 'WEST': 13, 'EAST': 65}
#
# ==== row:9, col:0 ====
# range(13, 65)
# 156
# ==== row:8, col:0 ====
# range(0, 61)
# 325
#
