from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from matplotlib.animation import FuncAnimation

from Planet import Planet
from UI.lab1 import UiPlanetSettings
from UI.lab1_dialog import UiPlanetNumberChooser
from UI.lab1_main import UiMainWindow
from SolarSystem import SolarSystem
from Utils import Point, Velocity


class PlanetNumberChooser(QMainWindow, UiPlanetNumberChooser):
    submitClicked = pyqtSignal(int)

    def __init__(self):
        UiPlanetNumberChooser.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)

    def confirm(self):
        self.submitClicked.emit(self.planetCount.value())


class PlanetSettings(QMainWindow, UiPlanetSettings):
    submitClicked = pyqtSignal(list)

    def __init__(self, planetNumber=4):
        UiPlanetSettings.__init__(self)
        QMainWindow.__init__(self)
        self.planetNumber = planetNumber
        self.setupUi(self)

    def confirm(self):
        self.submitClicked.emit()


class MainWindow(QMainWindow, UiMainWindow):
    def __init__(self):
        UiMainWindow.__init__(self)
        QMainWindow.__init__(self)

        self.anim = None
        self.solarSystem = SolarSystem()
        self.dialog = PlanetNumberChooser()
        self.planetSettingsWindow = PlanetSettings()
        self.dialog.submitClicked.connect(self.onPlanetNumberConfirm)

        self.setupUi(self)
        self.setupButtonFunctions()

    def setupButtonFunctions(self):
        self.pushButton.clicked.connect(self.plot_data)
        self.newSystem.clicked.connect(self.showChooser)
        self.saveSystem.clicked.connect(self.saveModelParameters)
        self.openSystem.clicked.connect(self.openModelParametersFromFile)
        self.planetParameters.clicked.connect(self.openModelParametersChangerWindow)

    def plot_data(self):
        for planet in self.solarSystem.planets:
            planet.plotPoint = self.MplWidget.canvas.ax.plot([planet.point.x], [planet.point.y], [planet.point.z],
                                                             marker='o', markersize=7,
                                                             markeredgecolor="black", markerfacecolor="black")
        self.solarSystem.frameText = self.MplWidget.canvas.ax.text2D(0.05, 0.95,
                                                                     f'Frame: 0/{int(self.solarSystem.timeLimit / self.solarSystem.dt)}',
                                                                     transform=self.MplWidget.canvas.ax.transAxes)
        self.anim = FuncAnimation(self.MplWidget, self.solarSystem.updateCanvas,
                                  frames=int(self.solarSystem.timeLimit / self.solarSystem.dt), repeat=False)
        self.MplWidget.canvas.draw()

    def showChooser(self):
        self.dialog.show()

    def onPlanetNumberConfirm(self, number):
        self.dialog.hide()
        self.planetSettingsWindow.planetNumber = int(number)
        self.planetSettingsWindow.show()

    def saveModelParameters(self):
        name = QFileDialog.getSaveFileName(self, 'Сохранить файл')
        with open(name, 'w+') as f:
            f.write(str(len(self.solarSystem.planets)))
            f.write(str(self.solarSystem.timeLimit))
            f.write(str(self.solarSystem.dt))
            f.write(str(self.solarSystem.scheme))
            for planet in self.solarSystem.planets:
                f.write(f'{planet.name} {planet.mass} {planet.point.x} {planet.point.y} {planet.point.z} {planet.velocity.x} {planet.velocity.y} {planet.velocity.z}')

    def openModelParametersFromFile(self):
        name = QFileDialog.getOpenFileName(self, "Открыть систему")
        with open(name, 'r') as f:
            self.planetSettingsWindow.planetNumber = int(f.readline())
            self.solarSystem.timeLimit = int(f.readline())
            self.solarSystem.dt = int(f.readline())
            self.solarSystem.scheme = f.readline()
            for i in range(self.planetSettingsWindow.planetNumber):
                settings = f.readline().strip('\n').split(' ')
                self.solarSystem.planets.append(Planet(name=settings[0], mass=float(settings[1]),
                                                       point=Point(float(settings[2]), float(settings[3]), float(settings[4])),
                                                       velocity=Velocity(float(settings[5]), float(settings[6]), float(settings[7]))))

    def openModelParametersChangerWindow(self):
        self.planetSettingsWindow.show()
