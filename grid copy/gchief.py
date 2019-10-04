from .agent import *

class GChief():
    """
    """

    def __init__(self, gimgs, gmap):
        """
        ----------
        Parameters
        ----------
        """
        self.imgs = gimgs
        self.map = gmap
        self.agents = []
        # procedure
        self.setupAgents()

    def setupAgents(self):
        """
        ----------
        Parameters
        ----------
        """
        
        # get image info
        imgH, imgW = self.imgs.get(key="binSeg")

        for row in range(self.map.nRow):
            lsAgentsRow = []
            for col in range(self.map.nCol):
                agent = Agent(name=self.map.getName(row=row, col=col), 
                              row=self.map.nRow, col=self.map.nCol)
                agent.setCoordinate(
                    x=self.map.lsPxCol[col], y=self.map.lsPxRow[row])
                lsAgentsRow.extend([agent])
            self.agents.extend([lsAgentsRow])

    def cpuPreDim(self, tol=5):
        """
        ----------
        Parameters
        ----------
        """

        img = self.imgs.get['binSeg']
        for row in range(self.map.nRow):
            for col in range(self.map.nCol):
                agentSelf = self.getAgent(row, col)
                rgTemp = dict()
                for axis in [0, 1]:
                    # extract direction info and 1dImg
                    dir1 = Dir(axis) # axis:0, return N(0) and S(2)
                    dir2 = Dir(axis+2) # axis:1, return W(1) and E(3)
                    axisRev = (not axis)*1
                    img1d = img[agentSelf.y,:] if axis else img[:, agentSelf.x]

                    # extract agents info
                    ptSelf = agentSelf.getCoordinate()[axisRev]
                    agentNeig1 = self.getAgentNeighbor(row, col, dir1)
                    agentNeig2 = self.getAgentNeighbor(row, col, dir2)

                    # if both neighbors exists
                    if (agentNeig1!=0) & (agentNeig2!=0):
                        ptNeig1 = agentNeig1.getCoordinate()[axisRev]
                        ptNeig2 = agentNeig2.getCoordinate()[axisRev]
                        ptMid = int((ptNeig1+ptNeig2)/2)
                        ptBd1 = int((ptNeig1+ptMid)/2)
                        ptBd2 = int((ptNeig2+ptMid)/2)
                    # if only left/up side exist
                    elif agentNeig1:
                        ptNeig1 = agentNeig1.getCoordinate()[axisRev]
                        ptBd1 = int((ptSelf+ptNeig1)/2)
                        ptBd2 = img.shape[axis]
                        agentSelf.set_border(dir2, ptBd2)
                    # if only right/down side exist
                    elif agentNeig2:
                        ptNeig2 = agentNeig2.getCoordinate()[axisRev]
                        ptBd1 = 0
                        ptBd2 = int((ptSelf+ptNeig2)/2)
                        agentSelf.set_border(dir1, ptBd1)
                    # if neither side exist
                    else:
                        ptBd1 = 0
                        ptBd2 = img.shape[axis]
                        agentSelf.set_border(dir1, ptBd1)
                        agentSelf.set_border(dir2, ptBd2)

                    # negative side (neighber 1)
                    pt_cur = ptSelf
                    tol_cur = 0
                    while (tol_cur < tol) & (pt_cur > ptBd1):
                        try:
                            img_val = img1d[pt_cur]
                        except:
                            break
                        tol_cur += 1 if img_val==0 else -tol_cur #else reset to 0
                        pt_cur -= 1
                    rgTemp[dir1.name] = pt_cur
                    # positive side (neighber 2)
                    pt_cur = ptSelf
                    tol_cur = 0
                    while (tol_cur < tol) & (ptBd2 > pt_cur):
                        try:
                            img_val = img1d[pt_cur]
                        except:
                            break
                        tol_cur += 1 if img_val==0 else -tol_cur #else reset to 0
                        pt_cur += 1
                    rgTemp[dir2.name] = pt_cur
                agentSelf.set_pre_dim(rgTemp)
    
    def segmentation(self, coefGrid=.2):
        """
        ----------
        Parameters
        ----------
        """
        print(0)

    def getAgent(self, row, col):
        """
        ----------
        Parameters
        ----------
        """
        if (row < 0) | (row >= self.map.nRow) | (col < 0) | (col >= self.map.nCol):
            return 0
        else:
            return self.agents[row][col]

    def getAgentNeighbor(self, row, col, dir):
        """
        ----------
        Parameters
        ----------
        """
        if dir == Dir.NORTH:
            return self.getAgent(row-1, col)
        elif dir == Dir.EAST:
            return self.getAgent(row, col+1)
        elif dir == Dir.SOUTH:
            return self.getAgent(row+1, col)
        elif dir == Dir.WEST:
            return self.getAgent(row, col-1)
        
    def resetAgentCoordinate(self):
        """
        ----------
        Parameters
        ----------
        """
        for row in range(self.map.nRow):
            for col in range(self.map.nCol):
                self.getAgent(row=row, col=col).resetCoordinate()
