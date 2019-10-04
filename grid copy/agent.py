from PyQt5.QtCore import QRect
from .Misc import Dir


class Agent():
    def __init__(self, name, row, col):
        """
        ----------
        Parameters
        ----------
        """
        self.name = name
        self.row, self.col = row, col
        self.y, self.x = 0, 0
        self.yReset, self.xReset = 0, 0
        self.preRgW, self.preRgH = range(0), range(0)
        self.border, self.borderReset = dict(), dict()
        for dir in list([Dir.NORTH, Dir.EAST, Dir.SOUTH, Dir.WEST]):
            self.border[dir.name] = 0
            self.borderReset[dir.name] = 0

    def getCoordinate(self):
        """
        ----------
        Parameters
        ----------
        """
        return self.x, self.y

    def setCoordinate(self, x, y):
        """
        ----------
        Parameters
        ----------
        """
        self.x, self.y = int(x), int(y)
        self.xReset, self.yReset = int(x), int(y)
        self.setBorder(Dir.NORTH, y)
        self.setBorder(Dir.SOUTH, y)
        self.setBorder(Dir.WEST, x)
        self.setBorder(Dir.EAST, x)

    def reset(self):
        """
        ----------
        Parameters
        ----------
        """
        self.resetCoordinate()
        self.resetBorder()

    def resetCoordinate(self):
        """
        ----------
        Parameters
        ----------
        """
        self.x = self.xReset
        self.y = self.yReset

    def setBorder(self, dir, pt):
        """
        ----------
        Parameters
        ----------
        """
        self.border[dir.name] = int(pt)
        self.check_border() # FIXME:

    def resetBorder(self):
        """
        ----------
        Parameters
        ----------
        """
        for dir in list([Dir.NORTH, Dir.WEST, Dir.SOUTH, Dir.EAST]):
            self.border[dir.name] = self.borderReset[dir.name]







    def get_pre_dim(self, isHeight=True):
        '''
        '''
        return self.pre_rg_H if isHeight else self.pre_rg_W

    def get_border(self, dir):
        return self.border[dir.name]

    def get_rect(self):
        x = self.get_border(Dir.WEST)
        y = self.get_border(Dir.NORTH)
        w = self.get_border(Dir.EAST) - x
        h = self.get_border(Dir.SOUTH) - y
        return QRect(x, y, w, h)

    def get_score_area(self, dir, img):
        '''
        Will ragne from 0 to 1
        '''
        isH = dir.value % 2  # E->1, S->0
        rg = self.get_pre_dim(isHeight=isH)
        bd = self.get_border(dir)
        # print("==== row:%d, col:%d ====" %(self.row, self.col))
        # print(rg)
        # print(bd)
        return img[rg, bd].mean() if isH else img[bd, rg].mean()

    def get_score_grid(self, dir):
        '''
        Will ragne from 0 to 1
        '''
        isWE = dir.value % 2  # is W, E or N, S
        pt_center = self.x if isWE else self.y
        pt_cur = self.get_border(dir)
        return abs(pt_cur-pt_center)

    def set_pre_dim(self, rg):
        '''
        '''
        self.pre_rg_W = range(rg['WEST'], rg['EAST'])
        self.pre_rg_H = range(rg['NORTH'], rg['SOUTH'])
        self.x = int((rg['EAST']+rg['WEST'])/2)
        self.y = int((rg['NORTH']+rg['SOUTH'])/2)
        self.x_reset, self.y_reset = self.x, self.y
        for dir in list([Dir.NORTH, Dir.WEST, Dir.SOUTH, Dir.EAST]):
            self.border_reset[dir.name] = self.border[dir.name]

    def set_border(self, dir, value):
        '''
        '''
        self.border[dir.name] = int(value)
        self.check_border()

    def update_border(self, dir, value):
        '''
        '''
        self.border[dir.name] += int(value)
        self.check_border()

    def update_coordinate(self, val, axis=0):
        '''
        '''
        val = int(val)
        if axis == 0:
            self.y += val
            self.border[Dir.NORTH.name] += val
            self.border[Dir.SOUTH.name] += val
        elif axis == 1:
            self.x += val
            self.border[Dir.WEST.name] += val
            self.border[Dir.EAST.name] += val
        self.check_border()

    def check_border(self):
        if self.border[Dir.NORTH.name] < 0:
            self.border[Dir.NORTH.name] = 0
        if self.border[Dir.WEST.name] < 0:
            self.border[Dir.WEST.name] = 0
        if self.border[Dir.SOUTH.name] >= self.imgH:
            self.border[Dir.SOUTH.name] = self.imgH-1
        if self.border[Dir.EAST.name] >= self.imgW:
            self.border[Dir.EAST.name] = self.imgW-1

    def set_save(self, save=False):
        "do nothing"

