# basic imports
import warnings
warnings.filterwarnings("ignore")

# self imports
from .guser import *
from .gimage import *
from .gmap import *
from .gagent import *
from .lib import *

class GRID():
    """
    """

    def __init__(self):
        """
        ----------
        Parameters
        ----------
        """

        # self-defined class
        self.user = GUser()
        self.imgs = GImage()
        self.map = GMap()
        self.agents = GAgent()

    def __user__(self):
        """
        ----------
        Parameters
        ----------
        """

        self.user.printInfo()

    def run(self, pathImg=None, pathMap=None, pts=None,
            k=3, features=[0, 1, 2], lsSelect=[0], valShad=0, valSmth=0,
            nRow=0, nCol=0, nSmooth=100,
            tol=5, coefGrid=.2,
            plot=False):
        """
        ----------
        Parameters
        ----------
        """
        self.loadData(pathImg=pathImg, pathMap=pathMap, plot=plot)
        self.cropImg(pts=pts, plot=plot)
        self.binarizeImg(k=k, features=features,
                         lsSelect=lsSelect, valShad=valShad, valSmth=valSmth, plot=plot)
        self.findPlots(nRow=nRow, nCol=nCol, nSmooth=nSmooth, plot=plot)
        self.cpuSeg(tol=tol, coefGrid=coefGrid, plot=plot)
        
    #=== === === === === === MAJOR WORKFLOW === === === === === ===

    def loadData(self, pathImg=None, pathMap=None, plot=False):
        """
        ----------
        Parameters
        ----------
        """
        if pathImg is None:
            self.imgs.load(
                pathImg="http://www.zzlab.net/James_Demo/seg_img.jpg")
            self.map.load(
                pathMap="http://www.zzlab.net/James_Demo/seg_map.csv")
        else:
            self.imgs.load(pathImg=pathImg)
            self.map.load(pathMap=pathMap)
        
        if plot:
            pltImShow(self.imgs.get("raw")[:,:,:3])

    def cropImg(self, pts=None, plot=False):
        """
        ----------
        Parameters
        ----------
        """

        self.imgs.crop(pts)

        if plot:
            pltImShow(self.imgs.get("crop")[:,:,:3])

    def binarizeImg(self, k=3, features=[0, 1, 2], lsSelect=[0], valShad=0, valSmth=0, plot=False):
        """
        ----------
        Parameters
        ----------
        """

        if self.imgs.get("crop") is None:
            self.cropImg()

        # KMEAN
        self.imgs.doKMeans(k=k, features=features)
        # BINARIZE
        self.imgs.binarize(k=k, features=features, lsSelect=lsSelect)
        # SMOOTH
        self.imgs.smooth(value=valSmth)
        # DESHADOW
        self.imgs.deShadow(value=valShad)
        # FINALIZE
        self.imgs.finalized()
        # Plot
        if plot:
            pltImShowMulti(
                imgs=[self.imgs.get('crop')[:, :, :3], self.imgs.get(
                    'kmean'), self.imgs.get('binOrg'), self.imgs.get('binSegSm')],
                titles=["Original", "K-Means", "Binarized", "Finalized"])

    def findPlots(self, nRow=0, nCol=0, nSmooth=100, plot=False):
        """
        ----------
        Parameters
        ----------
        """

        self.map.findPlots(GImg=self.imgs,
                           nRow=nRow, nCol=nCol, nSmooth=nSmooth)
        self.agents.setup(gmap=self.map, img=self.imgs.get('binSegSm'))
        
        if plot:
            pltSegPlot(self.agents, self.imgs.get("binSegSm"))

    def cpuSeg(self, tol=5, coefGrid=.2, plot=False):
        """
        ----------
        Parameters
        ----------
        """

        self.agents.cpuPreDim(tol=tol)
        self.agents.autoSeg(coefGrid=coefGrid)

        if plot:
            pltSegPlot(self.agents, self.imgs.get("visSeg"), isRect=True)
        
    #=== === === === === === IMAGE === === === === === ===

    def rotateImg(self, nRot):
        """
        ----------
        Parameters
        ----------
        """

        self.imgs.rotate(nRot)

    #=== === === === === === MAP === === === === === ===

    #=== === === === === === AGENTS === === === === === ===


    def fixSeg(self, width, length):
        """
        ----------
        Parameters
        ----------
        """
        self.agents.fixSeg(width, length)
  
    #=== === === === === === PLOTTING === === === === === ===

    