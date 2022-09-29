from Planet import Planet
from SolarSystem import SolarSystem
from Utils import *
from PyQt5.QtWidgets import QApplication
from UI.UIParts import MainWindow
import sys

if __name__ in "__main__":
    # solarSystem = SolarSystem(planets=[Planet(name="Earth", mass=1.2166E30, point=Point(), velocity=Velocity()),
    #                                    Planet(name="Mars", mass=6.083E24, point=Point(149500000000, 0, 0),
    #                                           velocity=Velocity(0, 23297.8704870374, 0)),
    #                                    Planet(name="Mars", mass=6.083E24, point=Point(-149500000000, 0, 0),
    #                                           velocity=Velocity(0, 23297.87048703))],
    #                           dt=100000, timeLimit=31536000)
    # solarSystem.show()


    # Приложению нужен один (и только один) экземпляр QApplication.
    # Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.
    # Если не будете использовать аргументы командной строки, QApplication([]) тоже работает
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
