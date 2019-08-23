from .GUI_Main import *
from PyQt5.QtWidgets import QApplication
import sys
import qdarkstyle

# if __name__ == '__main__':
def run():
    app = None
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # run main
    Window_Main()
    app.exec_()
