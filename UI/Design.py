from IPython.external.qt_for_kernel import QtCore
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
from UI.mplwidget import MplWidget


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
        self.buttonBox.rejected.connect(self.close)

    def confirm(self):
        self.submitClicked.emit(self.planetCount.value())


class PlanetSettings(QMainWindow, UiPlanetSettings):
    submitClicked = pyqtSignal(list)

    def __init__(self, planetNumber=2):
        UiPlanetSettings.__init__(self)
        QMainWindow.__init__(self)
        print('started')
        self.newSystem = True
        self.planetNumber = planetNumber
        self.solarSystem = SolarSystem()
        self.setupUi(self)
        self.setupEvents()
        self.populateTable()
        self.setValidators()
        self.populateFields()
        self.Euler.toggle()

    def confirm(self):
        self.solarSystem.dt = float(self.dt.text())
        self.solarSystem.timeLimit = float(self.timeLimit.text())
        for row in range(self.planetNumber):
            if self.newSystem:
                self.solarSystem.planets.append(Planet(name=self.planetsTable.item(row, 0).text(),
                                                       mass=float(self.planetsTable.item(row, 7).text()),
                                                       point=Point(float(self.planetsTable.item(row, 1).text()),
                                                                   float(self.planetsTable.item(row, 2).text()),
                                                                   float(self.planetsTable.item(row, 3).text())),
                                                       velocity=Velocity(float(self.planetsTable.item(row, 4).text()),
                                                                         float(self.planetsTable.item(row, 5).text()),
                                                                         float(self.planetsTable.item(row, 6).text()))))
            else:
                self.solarSystem.planets[row].mass = float(self.planetsTable.item(row, 7).text())
                self.solarSystem.planets[row].point = Point(float(self.planetsTable.item(row, 1).text()),
                                                            float(self.planetsTable.item(row, 2).text()),
                                                            float(self.planetsTable.item(row, 3).text()))
                self.solarSystem.planets[row].velocity = Velocity(float(self.planetsTable.item(row, 4).text()),
                                                                  float(self.planetsTable.item(row, 5).text()),
                                                                  float(self.planetsTable.item(row, 6).text()))
        self.newSystem = False
        self.close()

    def cancel(self):
        self.close()

    def setupEvents(self):
        self.buttonBox.accepted.connect(self.confirm)
        self.buttonBox.rejected.connect(self.cancel)
        self.EulerKramer.toggled.connect(self.setEulerKramer)
        self.Euler.toggled.connect(self.setEuler)
        self.Verle.toggled.connect(self.setVerle)

    def setEulerKramer(self, enabled):
        if enabled:
            self.solarSystem.scheme = SCHEMES.EULER_KRAMER

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
        self.dt.setText(str(self.solarSystem.dt))
        self.timeLimit.setText(str(self.solarSystem.timeLimit))

    def populateTable(self):
        tablerow = 0
        data = [0, 23297.8704870374, 16474.0822085901,
                13451.0317972361, 11648.9352435187,
                10419.1244280004, 9511.31579778152,
                8805.76734087033, 8237.04110429505,
                7765.95682901247, 7367.43353706546,
                7024.57225634525, 6725.51589861805,
                6461.66666539482, 6226.61780028044,
                6015.48429322621, 5824.46762175936]
        if self.newSystem:
            self.planetsTable.setRowCount(self.planetNumber)
            self.solarSystem.planets = []
            for i in range(self.planetNumber):
                self.planetsTable.setItem(tablerow, 0, QTableWidgetItem(str(tablerow + 1)))
                self.planetsTable.setItem(tablerow, 1, QTableWidgetItem(str(149500000000 * i)))
                self.planetsTable.setItem(tablerow, 2, QTableWidgetItem(str(0)))
                self.planetsTable.setItem(tablerow, 3, QTableWidgetItem(str(0)))
                self.planetsTable.setItem(tablerow, 4, QTableWidgetItem(str(0)))
                if i < len(data):
                    self.planetsTable.setItem(tablerow, 5, QTableWidgetItem(str(data[i])))
                else:
                    self.planetsTable.setItem(tablerow, 5, QTableWidgetItem(str(data[len(data)-1] - 500)))
                self.planetsTable.setItem(tablerow, 6, QTableWidgetItem(str(0)))
                self.planetsTable.setItem(tablerow, 7, QTableWidgetItem(str(1.2166E30 - 1E29 * i)))
                tablerow += 1
        else:
            self.planetsTable.setRowCount(len(self.solarSystem.planets))
            for planet in self.solarSystem.planets:
                self.planetsTable.setItem(tablerow, 0, QTableWidgetItem(planet.name))
                self.planetsTable.setItem(tablerow, 1, QTableWidgetItem(str(planet.point.x)))
                self.planetsTable.setItem(tablerow, 2, QTableWidgetItem(str(planet.point.y)))
                self.planetsTable.setItem(tablerow, 3, QTableWidgetItem(str(planet.point.z)))
                self.planetsTable.setItem(tablerow, 4, QTableWidgetItem(str(planet.velocity.x)))
                self.planetsTable.setItem(tablerow, 5, QTableWidgetItem(str(planet.velocity.y)))
                self.planetsTable.setItem(tablerow, 6, QTableWidgetItem(str(planet.velocity.z)))
                self.planetsTable.setItem(tablerow, 7, QTableWidgetItem(str(planet.mass)))
                tablerow += 1

        delegate = ReadOnlyDelegate(self.planetsTable)
        self.planetsTable.setItemDelegateForColumn(0, delegate)


class MainWindow(QMainWindow, UiMainWindow):
    def __init__(self):
        UiMainWindow.__init__(self)
        QMainWindow.__init__(self)

        self.isRunning = False
        self.anim = None
        self.dialog = PlanetNumberChooser()
        self.planetSettingsWindow = PlanetSettings()

        self.setupUi(self)
        self.setupButtonFunctions()
        self.setupEvents()

    # Setup functions
    def setupEvents(self):
        self.dialog.submitClicked.connect(self.onPlanetNumber)
        self.planetSettingsWindow.submitClicked.connect(self.onPlanetSettings)

    def setupButtonFunctions(self):
        self.pushButton.clicked.connect(self.plot_data)
        self.newSystem.triggered.connect(self.showChooser)
        self.saveSystem.triggered.connect(self.saveModelParameters)
        self.openSystem.triggered.connect(self.openModelParametersFromFile)
        self.planetParameters.triggered.connect(self.openModelParametersChangerWindow)

    # Event Functions
    def onPlanetNumber(self, number):
        self.dialog.hide()
        self.planetSettingsWindow.planetNumber = int(number)
        self.planetSettingsWindow.newSystem = True
        self.planetSettingsWindow.populateTable()
        self.planetSettingsWindow.show()

    def onPlanetSettings(self, number):
        self.planetSettingsWindow.hide()

    # Button functions
    def showChooser(self):
        if self.isRunning:
            self.anim.pause()
            self.clearAxes()
            self.isRunning = False
        self.dialog.show()

    def saveModelParameters(self):
        if self.isRunning:
            self.anim.pause()
            self.clearAxes()
            self.isRunning = False
        name = QFileDialog.getSaveFileName(self, 'Сохранить систему', '', '*.ussr')
        if name[0] != '':
            with open(f'{name[0]}.ussr', 'w+') as f:
                f.write(str(len(self.planetSettingsWindow.solarSystem.planets)))
                f.write('\n')
                f.write(str(self.planetSettingsWindow.solarSystem.timeLimit))
                f.write('\n')
                f.write(str(self.planetSettingsWindow.solarSystem.dt))
                f.write('\n')
                f.write(str(self.planetSettingsWindow.solarSystem.scheme))
                f.write('\n')
                for planet in self.planetSettingsWindow.solarSystem.planets:
                    f.write(
                        f'{planet.name} {planet.mass} {planet.point.x} {planet.point.y} {planet.point.z} {planet.velocity.x} {planet.velocity.y} {planet.velocity.z}')
                    f.write('\n')

    def openModelParametersFromFile(self):
        if self.isRunning:
            self.anim.pause()
            self.clearAxes()
            self.isRunning = False
        name = QFileDialog.getOpenFileName(self, 'Открыть систему', '', '*.ussr')
        if name[0] != '':
            with open(name[0], 'r') as f:
                self.planetSettingsWindow.planetNumber = int(f.readline())
                self.planetSettingsWindow.solarSystem.timeLimit = float(f.readline())
                self.planetSettingsWindow.solarSystem.dt = float(f.readline())
                scheme = f.readline()
                if scheme == 'SCHEMES.EULER':
                    self.planetSettingsWindow.solarSystem.scheme = SCHEMES.EULER
                elif scheme == 'SCHEMES.BIMAN':
                    self.planetSettingsWindow.solarSystem.scheme = SCHEMES.BIMAN
                elif scheme == 'SCHEMES.VERLET':
                    self.planetSettingsWindow.solarSystem.scheme = SCHEMES.VERLET
                for i in range(self.planetSettingsWindow.planetNumber):
                    settings = f.readline().strip('\n').split(' ')
                    self.planetSettingsWindow.solarSystem.planets.append(
                        Planet(name=settings[0], mass=float(settings[1]),
                               point=Point(float(settings[2]),
                                           float(settings[3]),
                                           float(settings[4])),
                               velocity=Velocity(float(settings[5]),
                                                 float(settings[6]),
                                                 float(settings[7]))))
            self.planetSettingsWindow.newSystem = False
            self.planetSettingsWindow.populateTable()

    def openModelParametersChangerWindow(self):
        if self.isRunning:
            self.anim.pause()
            self.clearAxes()
            self.isRunning = False
        self.planetSettingsWindow.show()

    # Other functions
    def plot_data(self):
        if self.isRunning:
            self.anim.pause()
        first = True
        for planet in self.planetSettingsWindow.solarSystem.planets:
            if first:
                planet.plotPoint = self.MplWidget.canvas.ax.plot([planet.point.x], [planet.point.y], [planet.point.z],
                                                                 marker='o', markersize=10,
                                                                 markeredgecolor="black", markerfacecolor="red")
                first = False
            else:
                planet.plotPoint = self.MplWidget.canvas.ax.plot([planet.point.x], [planet.point.y], [planet.point.z],
                                                                 marker='o', markersize=7,
                                                                 markeredgecolor="black", markerfacecolor="black")
            self.planetSettingsWindow.solarSystem.blit.append(planet.plotPoint[0])
        self.planetSettingsWindow.solarSystem.frameText = self.MplWidget.canvas.ax.text2D(0.05, 0.95,
                                                                                          f'Frame: 0/{int(self.planetSettingsWindow.solarSystem.timeLimit / self.planetSettingsWindow.solarSystem.dt)}',
                                                                                          transform=self.MplWidget.canvas.ax.transAxes)
        self.planetSettingsWindow.solarSystem.blit.append(self.planetSettingsWindow.solarSystem.frameText)
        self.anim = FuncAnimation(self.MplWidget, self.updateData,
                                  frames=int(
                                      self.planetSettingsWindow.solarSystem.timeLimit / self.planetSettingsWindow.solarSystem.dt),
                                  repeat=False, blit=True)
        self.MplWidget.canvas.draw()
        self.isRunning = True

    def clearAxes(self):
        for i in self.planetSettingsWindow.solarSystem.blit:
            i.remove()
        self.planetSettingsWindow.solarSystem.blit = []

    def updateData(self, i):
        artists = self.planetSettingsWindow.solarSystem.updateCanvas(i)
        self.calculateAndDisplayMassCenter()
        self.calculateAndDisplayEnergy()
        return artists

    def calculateAndDisplayMassCenter(self):
        xc, yc, zc = self.planetSettingsWindow.solarSystem.calculateMassCenter()
        self.textBrowser.setText(str(xc))
        self.textBrowser_2.setText(str(yc))
        self.textBrowser_3.setText(str(zc))

    def calculateAndDisplayEnergy(self):
        energy = self.planetSettingsWindow.solarSystem.calculateUniversalEnergy()
        self.textBrowser_4.setText(str(energy))
