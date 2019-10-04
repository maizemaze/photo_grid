from .io import *
from .gimage import *
from .gmap import *
from .gchief import *
from .guser import *

class GRID():
    """
    """

    def __init__(self):
        """
        """

        # self-defined class
        self.user = GUser()
        self.imgs = GImage()
        self.map = GMap()
        self.chief = GChief()

    def __user__(self):
        """
        """

        self.user.printInfo()

    def loadData(self, pathImg, pathMap=None):
        """
        """

        self.imgs.loadImg(pathImg=pathImg)
        self.map.loadMap(pathMap=pathMap)

    def cropImg(self, pts):
        """
        """

        self.imgs.cropImg(pts)

    def binarizeImg(self, k=3, features=[0, 1, 2], lsSelect=[0], valShad=0, valSmth=0):
        """
        """

        # KMEAN
        self.imgs.doKMeans(k=k, features=features)
        # BINARIZE
        self.imgs.binarizeImg(k=k, features=features, lsSelect=lsSelect)
        # SMOOTH
        self.imgs.smoothImg(value=valSmth)
        # DESHADOW
        self.imgs.deShadowImg(value=valShad)
        # FINALIZE
        self.imgs.finalizedImg()

    def rotateImg(self, nRot):
        """
        """

        self.imgs.rotateImg(nRot)

    def findPlots(self, nRow=0, nCol=0, nSmooth=100):
        """
        """

        self.map.findPlots(img=self.imgs.get(
            key='binSeg'), nRow=nRow, nCol=nCol, nSmooth=nSmooth)

    def segmentImg(self, coefGrid=0.2):
        """
        """
   
    def getAnchorRatio(self):
        """
        GUI SPCIFIC
        """

        return self.map.getRatio()
    
    def delAnchorRatio(self, dim, index):
        """
        GUI SPCIFIC
        """

        self.map.delRatio(dim=dim, index=index)

    def addAnchorRatio(self, dim, value):
        """
        GUI SPCIFIC
        """

        self.map.addRatio(dim=dim, value=value)

    def modAnchorRatio(self, dim, index, value):
        """
        GUI SPCIFIC
        """

        self.map.modRatio(dim=dim, index=index, value=value)

    def resetAnchorRatio(self):
        """
        GUI SPCIFIC
        """

        self.map.resetRatio()
