from Planet import *
from Utils import *
import unittest


class TestPlanet(unittest.TestCase):
    def setUp(self) -> None:
        self.planet = Planet(name="Earth", mass=100, point=Point(), velocity=Velocity())

    def test_eq(self) -> None:
        self.assertEqual(True, self.planet == Planet(name="Earth", mass=1000, point=Point(), velocity=Velocity()))