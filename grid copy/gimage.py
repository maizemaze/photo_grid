import numpy as np
from .libImg import *
from .io import *

__all__ = ["GImage"]

class GImage():
    """
    """
    def __init__(self):
        """
        """

        # images
        self.imgs = {
            'raw'    : None,
            'rawRs'  : None,
            'crop'   : None,
            'mean'   : None,
            'kmean'  : None,
            'binOrg' : None,
            'binTemp': None,
            'binSd'  : None,
            'binSm'  : None,
            'bin'    : None,
            'binSeg' : None
        }

        # pamameters
        self.width = 0
        self.heigt = 0
        self.depth = 0
        self.widthRs = 0
        self.heightRs = 0

        # kmean param.
        self.paramKMs = {
            'k' : -1,
            'center': None,
            'features': [],
            'lsSelect' : [],
            'lsKTobin' : [],
            'valShad' : 0,
            'valSmth' : 0
        }

    def get(self, key):
        """
        """

        return self.imgs[key]

    def set(self, key, value):
        """
        """

        self.imgs[key] = value

    def loadImg(self, pathImg):
        """
        """

        isLocalImg = pathImg.find("http://") + pathImg.find("https://") == -2

        # image
        if isLocalImg:
            imgInput = loadImgLocal(pathImg)
        else:
            imgInput = loadImgWeb(pathImg)

        # assign
        self.set(key='raw', value=imgInput)
        self.height = imgInput.shape[0]
        self.width = imgInput.shape[1]
        self.depth = imgInput.shape[2] 

    def cropImg(self, pts):
        """
        """

        self.set(key  ='crop',
                    value=cropImg(self.imgs['raw'], pts))
        self.set(key  ='mean',
                    value=self.get('crop')[:,:,:3].mean(axis=2))
        self.widthRs = self.get(key='crop').shape[1]
        self.heightRs = self.get(key='crop').shape[0]

    def doKMeans(self, k=3, features=[0, 1, 2]):
        """
        """

        # Will skip if no updates on the params         
        if (k != self.paramKMs['k']) or (features != self.paramKMs['features']):            
            imgK, center = doKMeans(img=self.get('crop'),
                                    k=k,
                                    features=features)
            self.set(key='kmean', value=imgK)
            # update parameters
            self.paramKMs['center'] = center
            self.paramKMs['k'] = k
            self.paramKMs['features'] = features

    def binarizeImg(self, k=3, features=[0, 1, 2], lsSelect=[0]):
        """
        """

        if (k != self.paramKMs['k']) or (features != self.paramKMs['features']) or (lsSelect != self.paramKMs['lsSelect']):
            ratioK = [(self.paramKMs['center'][i, 0]-self.paramKMs['center'][i, 1])/self.paramKMs['center'][i, :].sum()
                      for i in range(self.paramKMs['center'].shape[0])]
            rankK = np.flip(np.argsort(ratioK), 0) 
            try:
                clusterSelected = rankK[lsSelect]
            except:
                clusterSelected = []
            self.set(key='binOrg', value=(
                (np.isin(self.get('kmean'), clusterSelected))*1).astype(np.int))
            self.set(key='binTemp', value=self.get('binOrg').copy())
            self.set(key='binSm', value=self.get('binOrg').copy())
            # udpate parameters
            self.paramKMs['k'] = k
            self.paramKMs['features'] = features
            self.paramKMs['lsSelect'] = lsSelect
            self.paramKMs['lsKToBin'] = clusterSelected
        
    def deShadowImg(self, value):
        """
        """

        if value != self.paramKMs['valShad']:
            self.set(key='binSd', value=(self.get(key='mean')>=value)*1)
            # update parameter
            self.paramKMs['valShad'] = value

    def smoothImg(self, value):
        """
        """

        if value != self.paramKMs['valSmth']:
            valSmthDiff = value - self.paramKMs['valSmth']
            if valSmthDiff > 0:
                valSmthReal = valSmthDiff
            else:
                valSmthReal = value
                self.set(key='binTemp', value=self.get(key='binOrg').copy())      
            self.set(key='binTemp', value=smoothImg(image=self.get(key='binTemp'), n=valSmthReal))
            self.set(key='binSm',   value=binarizeSmImg(self.get(key='binTemp')))
            # update parameters
            self.paramKMs['valSmth'] = value

    def finalizedImg(self):
        """
        """

        self.set(key='bin', value=np.multiply(
            self.get(key='binSm'), self.get(key='binSd')))
        imgSmth = smoothImg(image=self.get(key='bin'), n=30)
        imgBinSeg = binarizeSmImg(imgSmth)
        self.set(key='binSeg', value=imgBinSeg)

    def rotateImg(self, nRot):
        """
        """

        for key in self.imgs.keys():
            try:
                self.set(key=key, value=np.rot90(self.get(key=key), nRot))
            except:
                None
