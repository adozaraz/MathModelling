import math
import unittest
from Utils import Characteristic, Point, Velocity, Acceleration


class TestCharacteristic(unittest.TestCase):
    def setUp(self) -> None:
        self.characteristic = Characteristic()

    def test_eq(self):
        self.assertEqual(False, self.characteristic == Characteristic(1, 1, 1))
        self.assertEqual(True, self.characteristic == Characteristic())


class TestPoint(unittest.TestCase):
    def setUp(self) -> None:
        self.point = Point()
        self.velocity = Velocity(1, 1, 1)
        self.dt = 2
        self.acceleration = Acceleration(1, 1, 1)

    def test_calculateScalarDistance(self):
        self.assertEqual(math.sqrt(12), Point.calculateScalarDistance(self.point, Point(2, 2, 2)))

    def test_updateVelocityRelativeToAcceleration(self):
        self.point.updatePointRelativeToVelocityAndAcceleration(self.velocity, self.dt, self.acceleration)
        self.assertEqual(Point(6, 6, 6), self.point)


class TestVelocity(unittest.TestCase):
    def setUp(self) -> None:
        self.velocity = Velocity()
        self.acceleration = Acceleration(1, 1, 1)
        self.dt = 2

    def test_updateVelocityRelativeToAcceleration(self):
        self.velocity.updateVelocityRelativeToAcceleration(self.acceleration, self.dt)
        self.assertEqual(Velocity(2, 2, 2), self.velocity)


class TestAcceleration(unittest.TestCase):
    def setUp(self) -> None:
        self.acceleration = Acceleration()
        self.radius = 3
        self.point = Point(3, 3, 3)
        self.newAccel = 3

    def test_recalculateAcceleration(self):
        self.acceleration.recalculateAcceleration(self.newAccel, self.radius, self.point)
        self.assertEqual(Acceleration(-3, -3, -3), self.acceleration)

