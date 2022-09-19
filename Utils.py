import math
from enum import Enum
from scipy.constants import G


class SCHEMES(Enum):
    EULER = 0
    VERLET = 1
    BIMAN = 2


class Characteristic:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
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

    def updatePointRelativeToVelocityAndAcceleration(self, velocity, dt, acceleration) -> None:
        self.x += velocity.x * dt + acceleration.x * dt ** 2
        self.y += velocity.y * dt + acceleration.y * dt ** 2
        self.z += velocity.z * dt + acceleration.z * dt ** 2


class Velocity(Characteristic):
    def updateVelocityRelativeToAcceleration(self, acceleration, dt):
        self.x += acceleration.x * dt
        self.y += acceleration.y * dt
        self.z += acceleration.z * dt


class Acceleration(Characteristic):
    def recalculateAcceleration(self, acceleration, radius, point):
        self.x += acceleration * (self.x - point.x) / radius
        self.y += acceleration * (self.y - point.y) / radius
        self.z += acceleration * (self.z - point.z) / radius

    @staticmethod
    def calculateAcceleration(planet, otherPlanet):
        r = Point.calculateScalarDistance(planet.point, otherPlanet.point)
        a = planet.mass * G / (r ** 2)
        return Acceleration(x=a * (planet.x - otherPlanet.x) / r, y=a * (planet.y - otherPlanet.y) / r,
                            z=a * (planet.z - otherPlanet.z) / r)
