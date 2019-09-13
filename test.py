# /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages
cp -r /Users/jameschen/Dropbox/photo_gridd/grid/* /Users/jameschen/Dropbox/photo_gridd/env/lib/python3.6/site-packages/grid/
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
import cv2
import numpy as np
import pandas as pd
import json, os, sys
from PyQt5.QtWidgets import QApplication
import numpy as np
import pandas as pd
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from grid import *
from grid.CPU_Field import *
from grid.Misc import *
import rasterio
os.chdir("/Users/jameschen/Dropbox/photo_gridd")
params = dict()
params['anchors'] = json.load(open('anchors'))
params['nc'] = 19
params['nr'] = 3
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
GPU_Output.Panel_Output(**params)
app.exec_()


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

# Test collapsable panels
from PyQt4 import QtGui, QtCore

class FrameLayout(QtGui.QWidget):
    def __init__(self, parent=None, title=None):
        QtGui.QFrame.__init__(self, parent=parent)

        self._is_collasped = True
        self._title_frame = None
        self._content, self._content_layout = (None, None)

        self._main_v_layout = QtGui.QVBoxLayout(self)
        self._main_v_layout.addWidget(self.initTitleFrame(title, self._is_collasped))
        self._main_v_layout.addWidget(self.initContent(self._is_collasped))

        self.initCollapsable()

    def initTitleFrame(self, title, collapsed):
        self._title_frame = self.TitleFrame(title=title, collapsed=collapsed)

        return self._title_frame

    def initContent(self, collapsed):
        self._content = QtGui.QWidget()
        self._content_layout = QtGui.QVBoxLayout()

        self._content.setLayout(self._content_layout)
        self._content.setVisible(not collapsed)

        return self._content

    def addWidget(self, widget):
        self._content_layout.addWidget(widget)

    def initCollapsable(self):
        QtCore.QObject.connect(self._title_frame, QtCore.SIGNAL('clicked()'), self.toggleCollapsed)

    def toggleCollapsed(self):
        self._content.setVisible(self._is_collasped)
        self._is_collasped = not self._is_collasped
        self._title_frame._arrow.setArrow(int(self._is_collasped))

    ############################
    #           TITLE          #
    ############################
    class TitleFrame(QtGui.QFrame):
        def __init__(self, parent=None, title="", collapsed=False):
            QtGui.QFrame.__init__(self, parent=parent)

            self.setMinimumHeight(24)
            self.move(QtCore.QPoint(24, 0))
            self.setStyleSheet("border:1px solid rgb(41, 41, 41); ")

            self._hlayout = QtGui.QHBoxLayout(self)
            self._hlayout.setContentsMargins(0, 0, 0, 0)
            self._hlayout.setSpacing(0)

            self._arrow = None
            self._title = None

            self._hlayout.addWidget(self.initArrow(collapsed))
            self._hlayout.addWidget(self.initTitle(title))

        def initArrow(self, collapsed):
            self._arrow = FrameLayout.Arrow(collapsed=collapsed)
            self._arrow.setStyleSheet("border:0px")

            return self._arrow

        def initTitle(self, title=None):
            self._title = QtGui.QLabel(title)
            self._title.setMinimumHeight(24)
            self._title.move(QtCore.QPoint(24, 0))
            self._title.setStyleSheet("border:0px")

            return self._title

        def mousePressEvent(self, event):
            self.emit(QtCore.SIGNAL('clicked()'))

            return super(FrameLayout.TitleFrame, self).mousePressEvent(event)


    #############################
    #           ARROW           #
    #############################
    class Arrow(QtGui.QFrame):
        def __init__(self, parent=None, collapsed=False):
            QtGui.QFrame.__init__(self, parent=parent)

            self.setMaximumSize(24, 24)

            # horizontal == 0
            self._arrow_horizontal = (QtCore.QPointF(7.0, 8.0), QtCore.QPointF(17.0, 8.0), QtCore.QPointF(12.0, 13.0))
            # vertical == 1
            self._arrow_vertical = (QtCore.QPointF(8.0, 7.0), QtCore.QPointF(13.0, 12.0), QtCore.QPointF(8.0, 17.0))
            # arrow
            self._arrow = None
            self.setArrow(int(collapsed))

        def setArrow(self, arrow_dir):
            if arrow_dir:
                self._arrow = self._arrow_vertical
            else:
                self._arrow = self._arrow_horizontal

        def paintEvent(self, event):
            painter = QtGui.QPainter()
            painter.begin(self)
            painter.setBrush(QtGui.QColor(192, 192, 192))
            painter.setPen(QtGui.QColor(64, 64, 64))
            painter.drawPolygon(*self._arrow)
            painter.end()
