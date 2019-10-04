# basic imports 
from enum import Enum

# 3rd party imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# self imports
# from .grid import GRID
# from .gui import *

class GRID_GUI(QMainWindow):
    """
    """

    class Panels(Enum):
        INPUTER = 0, PnInputer
        CROPPER = 1, PnCropper
        KMEANER = 2, PnKmeaner
        ANCHOR = 3, PnAnchor
        OUTPUTER = 4, PnOutputer

    def __init__(self):
        """
        ----------
        Parameters
        ----------
        """

        super().__init__()
        self.setStyleSheet("""
        QWidget {
            font: 20pt Trebuchet MS
        }
        QGroupBox::title{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;ㄊ
        }
        QGroupBox {
            border: 1px solid gray;
            border-radius: 9px;
            margin-top: 0.5em;
        }
        """)

        # CLI 
        self.grid = GRID()
        
        # GUI
        self.pnContent = QWidget()
        self.pnMain = QStackedWidget()
        self.pnNavi = QWidget()
        self.btNext = QPushButton()
        self.btPrev = QPushButton()
        self.layout = None

        # UI
        self.iniUI()

    def initUI(self):
        """
        ----------
        Parameters
        ----------
        """
        
        # window setup
        self.setWindowTitle("GRID")
        self.setMinimumSize(QSize(width=1440, height=900))
        self.centerWindow()
       
        # initialize with first panel
        self.updateMainPn(Panels.INPUTER)
        
        # show
        self.show()
    
    def updateMainPn(self, panel, isNew=True):
        """
        ----------
        Parameters
        ----------
        """

        # define events
        if panel==Panels.INPUTER:
            self.btNext.clicked.connect(lambda: self.updateMainPn(Panels.CROPPER))
            self.assembleNavigation(nameNext="Load Files ->", oneSide=True)
        elif panel==Panels.CROPPER:
            self.btPrev.clicked.connect(lambda: self.updateMainPn(Panels.INPUTER, isNew=False))
            self.btNext.clicked.connect(lambda: self.updateMainPn(Panels.KMEANER))
            self.assembleNavigation()
        elif panel==Panels.KMEANER:
            self.btPrev.clicked.connect(lambda: self.updateMainPn(Panels.CROPPER, isNew=False))
            self.btNext.clicked.connect(lambda: self.updateMainPn(Panels.ANCHOR))
            self.assembleNavigation()
        elif panel == Panels.ANCHOR:
            self.btPrev.clicked.connect(lambda: self.updateMainPn(Panels.KMEANER, isNew=False))
            self.btNext.clicked.connect(lambda: self.updateMainPn(Panels.OUTPUTER))
            self.assembleNavigation()
        elif panel==Panels.OUTPUTER:
            self.btPrev.clicked.connect(lambda: self.updateMainPn(Panels.ANCHOR, isNew=False))
            self.btNext.clicked.connect(lambda: self.finalize())
            self.assembleNavigation(nameNext="Finish")

        # traverse forward
        if isNew:
            self.pnMain.currentWidget().run()
            self.pnMain.addWidget(panel.value[1](self.grid))
        # traverse backward
        else:
            self.pnMain.removeWidget(self.pnMain.widget(panel.value[0]+1))

        # set current widget
        self.pnMain.setCurrentIndex(panel.value[0])

        # show
        self.assembleAndShow()

    def finalize(self):
        """
        ----------
        Parameters
        ----------
        """

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Start another job?")
        msgBox.setWindowTitle("Finish")
        msgBox.setStandardButtons(
            QMessageBox.Cancel | QMessageBox.Yes | QMessageBox.Save)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes:
            # TODO: action when save files
            print("option yes")
        elif returnValue == QMessageBox.Save:
            # TODO: action when startover
            print("option save")
            
    def centerWindow(self):
        """
        ----------
        Parameters
        ----------
        """

        center = QApplication.desktop().availableGeometry().center()
        rect = self.geometry()
        rect.moveCenter(center)
        self.setGeometry(rect)

    def assembleNavigation(self, nameNext="Next ->", namePrev="<- Prev", oneSide=False):
        """
        ----------
        Parameters
        ----------
        """

        self.pnNavi = QWidget()
        self.btNext = QPushButton(nameNext)
        self.btPrev = QPushButton(namePrev)
        loNavi = QHBoxLayout()
        if oneSide:
            loNavi.addStretch(1)
        else:
            loNavi.addWidget(self.btPrev)
        loNavi.addWidget(self.btNext)
        self.pnNavi.setLayout(loNavi)

    def assembleAndShow(self):
        """
        ----------
        Parameters
        ----------
        """

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.pnMain, Qt.AlignCenter)
        self.layout.addWidget(self.pnNavi)
        self.pnContent = QWidget()
        self.pnContent.setLayout(self.layout)
        self.setCentralWidget(self.pnContent)
        self.pnMain.currentWidget().run(self.grid)
        self.show()





# ARCHIVE:
# def test(self):
#     import json
#     with open('anchors', 'w') as fout:
#         json.dump(self.params['anchors'], fout)
#     np.save("img_crop", self.params['crop'])
#     np.save("img_bin", self.params['bin'])
#     np.save("map", self.params['map'])
#     np.save("img_k", self.params['k'])
#     np.save("ls_bin", self.params['ls_bin'])
#     print("nc:%d" % (self.params['nc']))
#     print("nr:%d" % (self.params['nr']))
