from PyQt5.QtWidgets import QMainWindow
from matplotlib.animation import FuncAnimation

from UI.lab1 import UiPlanetSettings
from UI.lab1_dialog import UiPlanetNumberChooser
from UI.lab1_main import UiMainWindow
from SolarSystem import SolarSystem

class MainWindow(QMainWindow, UiMainWindow):
    def __init__(self):
        UiMainWindow.__init__(self)
        QMainWindow.__init__(self)

        self.solarSystem = SolarSystem()

        self.setupUi(self)
        self.pushButton.clicked.connect(self.plot_data)

    def plot_data(self):
        for planet in self.solarSystem.planets:
            planet.plotPoint = self.MplWidget.canvas.ax.plot([planet.point.x], [planet.point.y], [planet.point.z],
                                                             marker='o', markersize=7,
                                                             markeredgecolor="black", markerfacecolor="black")
        self.anim = FuncAnimation(self.MplWidget, self.solarSystem.updateCanvas,
                                  frames=int(self.solarSystem.timeLimit / self.solarSystem.dt))
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
