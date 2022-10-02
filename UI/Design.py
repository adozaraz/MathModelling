from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QStyledItemDelegate
from matplotlib.animation import FuncAnimation

from Planet import Planet
from UI.lab1 import UiPlanetSettings
from UI.lab1_dialog import UiPlanetNumberChooser
from UI.lab1_main import UiMainWindow
from SolarSystem import SolarSystem
from Utils import Point, Velocity, SCHEMES


class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        print("Read only!")
        return


class PlanetNumberChooser(QMainWindow, UiPlanetNumberChooser):
    submitClicked = pyqtSignal(int)

    def __init__(self):
        UiPlanetNumberChooser.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.confirm)

    def confirm(self):
        self.submitClicked.emit(self.planetCount.value())


class PlanetSettings(QMainWindow, UiPlanetSettings):
    submitClicked = pyqtSignal(list)

    def __init__(self, planetNumber=4):
        UiPlanetSettings.__init__(self)
        QMainWindow.__init__(self)
        self.planetNumber = planetNumber
        self.solarSystem = SolarSystem()
        self.setupUi(self)
        self.setupEvents()
        self.populateTable()
        self.setValidators()
        self.populateFields()

    def confirm(self):
        self.submitClicked.emit()

    def setupEvents(self):
        self.buttonBox.accepted.connect(self.confirm)
        self.Biman.toggled.connect(self.setBiman)
        self.Euler.toggled.connect(self.setEuler)
        self.Verle.toggled.connect(self.setVerle)

    def setBiman(self, enabled):
        if enabled:
            self.solarSystem.scheme = SCHEMES.BIMAN

    def setEuler(self, enabled):
        if enabled:
            self.solarSystem.scheme = SCHEMES.EULER

    def setVerle(self, enabled):
        if enabled:
            self.solarSystem.scheme = SCHEMES.VERLET

    def setValidators(self):
        validator = QDoubleValidator()
        self.dt.setValidator(validator)
        self.timeLimit.setValidator(validator)

    def populateFields(self):
        self.dt.setText(self.solarSystem.dt)
        self.timeLimit.setText(self.solarSystem.timeLimit)

    def populateTable(self):
        self.planetsTable.setRowCount(self.planetNumber)
        tablerow = 0
        for planet in self.solarSystem.planets:
            self.planetsTable.setItem(tablerow, 0, QTableWidgetItem(tablerow + 1))
            self.planetsTable.setItem(tablerow, 1, QTableWidgetItem(planet.point.x))
            self.planetsTable.setItem(tablerow, 2, QTableWidgetItem(planet.point.y))
            self.planetsTable.setItem(tablerow, 3, QTableWidgetItem(planet.point.z))
            self.planetsTable.setItem(tablerow, 4, QTableWidgetItem(planet.velocity.x))
            self.planetsTable.setItem(tablerow, 5, QTableWidgetItem(planet.velocity.y))
            self.planetsTable.setItem(tablerow, 6, QTableWidgetItem(planet.velocity.z))
            self.planetsTable.setItem(tablerow, 7, QTableWidgetItem(planet.mass))
            tablerow += 1

        delegate = ReadOnlyDelegate(self.planetsTable)
        self.planetsTable.setItemDelegateForColumn(0, delegate)


class MainWindow(QMainWindow, UiMainWindow):
    def __init__(self):
        UiMainWindow.__init__(self)
        QMainWindow.__init__(self)

        self.anim = None
        self.dialog = PlanetNumberChooser()
        self.planetSettingsWindow = PlanetSettings()
        self.dialog.submitClicked.connect(self.onPlanetNumberConfirm)
        self.planetSettingsWindow.submitClicked.connect(self.onPlanetSettingsConfirm)

        self.setupUi(self)
        self.setupButtonFunctions()

    def setupButtonFunctions(self):
        self.pushButton.clicked.connect(self.plot_data)
        self.newSystem.clicked.connect(self.showChooser)
        self.saveSystem.clicked.connect(self.saveModelParameters)
        self.openSystem.clicked.connect(self.openModelParametersFromFile)
        self.planetParameters.clicked.connect(self.openModelParametersChangerWindow)

    def plot_data(self):
        for planet in self.planetSettingsWindow.solarSystem.planets:
            planet.plotPoint = self.MplWidget.canvas.ax.plot([planet.point.x], [planet.point.y], [planet.point.z],
                                                             marker='o', markersize=7,
                                                             markeredgecolor="black", markerfacecolor="black")
        self.planetSettingsWindow.solarSystem.frameText = self.MplWidget.canvas.ax.text2D(0.05, 0.95,
                                                                                          f'Frame: 0/{int(self.planetSettingsWindow.solarSystem.timeLimit / self.planetSettingsWindow.solarSystem.dt)}',
                                                                                          transform=self.MplWidget.canvas.ax.transAxes)
        self.anim = FuncAnimation(self.MplWidget, self.planetSettingsWindow.solarSystem.updateCanvas,
                                  frames=int(
                                      self.planetSettingsWindow.solarSystem.timeLimit / self.planetSettingsWindow.solarSystem.dt),
                                  repeat=False)
        self.MplWidget.canvas.draw()

    def showChooser(self):
        self.dialog.show()

    def onPlanetNumberConfirm(self, number):
        self.dialog.hide()
        self.planetSettingsWindow.planetNumber = int(number)
        self.planetSettingsWindow.show()

    def onPlanetSettingsConfirm(self):
        self.planetSettingsWindow.hide()

    def saveModelParameters(self):
        name = QFileDialog.getSaveFileName(self, 'Сохранить файл')
        with open(name, 'w+') as f:
            f.write(str(len(self.planetSettingsWindow.solarSystem.planets)))
            f.write(str(self.planetSettingsWindow.solarSystem.timeLimit))
            f.write(str(self.planetSettingsWindow.solarSystem.dt))
            f.write(str(self.planetSettingsWindow.solarSystem.scheme))
            for planet in self.planetSettingsWindow.solarSystem.planets:
                f.write(
                    f'{planet.name} {planet.mass} {planet.point.x} {planet.point.y} {planet.point.z} {planet.velocity.x} {planet.velocity.y} {planet.velocity.z}')

    def openModelParametersFromFile(self):
        name = QFileDialog.getOpenFileName(self, "Открыть систему")
        with open(name, 'r') as f:
            self.planetSettingsWindow.planetNumber = int(f.readline())
            self.planetSettingsWindow.solarSystem.timeLimit = int(f.readline())
            self.planetSettingsWindow.solarSystem.dt = int(f.readline())
            self.planetSettingsWindow.solarSystem.scheme = f.readline()
            for i in range(self.planetSettingsWindow.planetNumber):
                settings = f.readline().strip('\n').split(' ')
                self.planetSettingsWindow.solarSystem.planets.append(Planet(name=settings[0], mass=float(settings[1]),
                                                                            point=Point(float(settings[2]),
                                                                                        float(settings[3]),
                                                                                        float(settings[4])),
                                                                            velocity=Velocity(float(settings[5]),
                                                                                              float(settings[6]),
                                                                                              float(settings[7]))))

    def openModelParametersChangerWindow(self):
        self.planetSettingsWindow.show()
