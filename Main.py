from Planet import Planet
from SolarSystem import SolarSystem
from Utils import *
from PyQt5.QtWidgets import QApplication
from UI.Design import MainWindow
import sys

if __name__ in "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
