cp /Users/jameschen/Dropbox/photo_grid/photo_grid/*.py /Users/jameschen/Dropbox/James_Git/env/lib/python3.6/site-packages/photo_grid/
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

# img = cv2.imread(path, cv2.IMREAD_UNCHANGED).astype(np.uint8)
# img = np.array(Image.open(path)).astype(np.uint8)
# img[:,:,:3] = img[:,:,:3][:,:,[2,1,0]] # swap to rgb instead of bgr


img.mean(axis=(0,1))

''' TEST OUTPUT '''
import cv2
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json, os, sys
from PyQt5.QtWidgets import QApplication
import photo_grid

os.chdir("/Users/jameschen/Dropbox/James_Git")
img_crop = np.load("img_crop.npy")
img_bin = np.load("img_bin.npy")
anchors = json.load(open('anchors'))
map = pd.DataFrame(np.load("map.npy", allow_pickle=True))
nc = 6
nr = 9

app = QApplication(sys.argv)
pn_main = photo_grid.Panel_Output(img_raw=img_crop, img_bin=img_bin, map=map, nc=nc, nr=nr, anchors=anchors)


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
