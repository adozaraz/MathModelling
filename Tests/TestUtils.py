import math
import unittest
from Utils import Characteristic, Point, Velocity, Acceleration


class TestCharacteristic(unittest.TestCase):
    def setUp(self) -> None:
        self.characteristic = Characteristic()

    def test_eq(self):
        self.assertEqual(self.characteristic == Characteristic(1, 1, 1), False)
        self.assertEqual(self.characteristic == Characteristic(), True)


class TestPoint(unittest.TestCase):
    def setUp(self) -> None:
        self.point = Point()
        self.velocity = Velocity(1, 1, 1)
        self.dt = 2
        self.acceleration = Acceleration(1, 1, 1)

    def test_calculateScalarDistance(self):
        self.assertEqual(Point.calculateScalarDistance(self.point, Point(2, 2, 2)), math.sqrt(12))

    def test_updateVelocityRelativeToAcceleration(self):
        self.point.updatePointRelativeToVelocityAndAcceleration(self.velocity, self.dt, self.acceleration)
        self.assertEqual(self.point, Point(6, 6, 6))


class TestVelocity(unittest.TestCase):
    def setUp(self) -> None:
        self.velocity = Velocity()
        self.acceleration = Acceleration(1, 1, 1)
        self.dt = 2

    def test_updateVelocityRelativeToAcceleration(self):
        self.velocity.updateVelocityRelativeToAcceleration(self.acceleration, self.dt)
        self.assertEqual(self.velocity, Velocity(2, 2, 2))


class TestAcceleration(unittest.TestCase):
    def setUp(self) -> None:
        self.acceleration = Acceleration()
        self.radius = 3
        self.point = Point(3, 3, 3)
        self.newAccel = 3

    def test_recalculateAcceleration(self):
        self.acceleration.recalculateAcceleration(self.newAccel, self.radius, self.point)
        self.assertEqual(self.acceleration, Acceleration(-3, -3, -3))

