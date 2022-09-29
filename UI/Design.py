from PyQt5.QtWidgets import QMainWindow
from UI.lab1 import UiPlanetSettings
from UI.lab1_dialog import UiPlanetNumberChooser
from UI.lab1_main import UiMainWindow


class MainWindow(QMainWindow, UiMainWindow):
    def __init__(self):
        UiMainWindow.__init__(self)
        QMainWindow.__init__(self)

        self.setupUi(self)
        self.pushButton.clicked.connect(self.plot_data)

    def plot_data(self):
        x = range(0, 10)
        y = range(0, 20, 2)
        self.MplWidget.canvas.ax.plot(x, y)
        self.MplWidget.canvas.draw()


class PlanetNumberChooser(QMainWindow, UiPlanetNumberChooser):
    def __init__(self):
        UiPlanetNumberChooser.__init__(self)
        QMainWindow.__init__(self)

        self.setupUi(self)


class PlanetSettings(QMainWindow, UiPlanetSettings):
    def __init__(self):
        UiPlanetSettings.__init__(self)
        QMainWindow.__init__(self)

        self.setupUi(self)
