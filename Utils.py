import math
from enum import Enum
from scipy.constants import G


class SCHEMES(Enum):
    EULER = 0
    VERLET = 1
    EULER_KRAMER = 2


class Characteristic:
    def __init__(self, x: float = 0., y: float = 0., z: float = 0.):
        self.__x: float = x
        self.__y: float = y
        self.__z: float = z

    def __iadd__(self, other):
        self.__x += other.x
        self.__y += other.y
        self.__z += other.z
        return self

    def __eq__(self, other):
        if not isinstance(other, Characteristic):
            return NotImplemented

        return type(self) == type(other) and self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def z(self) -> float:
        return self.__z

    @x.setter
    def x(self, x: float) -> None:
        self.__x = x

    @y.setter
    def y(self, y: float) -> None:
        self.__y = y

    @z.setter
    def z(self, z: float) -> None:
        self.__z = z


class Point(Characteristic):
    @staticmethod
    def calculateScalarDistance(firstPoint, secondPoint):
        return math.sqrt((firstPoint.x - secondPoint.x) ** 2 +
                         (firstPoint.y - secondPoint.y) ** 2 + (firstPoint.z - secondPoint.z) ** 2)


class Velocity(Characteristic):
    pass


class Acceleration(Characteristic):
    @staticmethod
    def calculateAcceleration(planet, otherPlanet):
        r = Point.calculateScalarDistance(planet.point, otherPlanet.point)
        a = planet.mass * G / (r ** 2)
        return Acceleration(x=a * (planet.point.x - otherPlanet.point.x) / r,
                            y=a * (planet.point.y - otherPlanet.point.y) / r,
                            z=a * (planet.point.z - otherPlanet.point.z) / r)
