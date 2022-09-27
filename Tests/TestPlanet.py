from Planet import *
from Utils import *
from scipy.constants import G
import unittest


class TestPlanet(unittest.TestCase):
    def setUp(self) -> None:
        self.planet = Planet(mass=1000, point=Point(), velocity=Velocity(), acceleration=Acceleration())
        self.time = 1
        self.planets = [Planet(mass=10000, point=Point(2, 2, 2), velocity=Velocity(1., 1., 1.), acceleration=Acceleration()),
                        Planet(mass=200, point=Point(-4, 2, 0), velocity=Velocity(-4, 0, -2.5), acceleration=Acceleration()),
                        Planet(mass=4000, point=Point(1, 2, -2), velocity=Velocity(-2, 0.5, 2.3), acceleration=Acceleration())]

    def test_calculateStep(self):
        self.planet.calculateStep(self.time, self.planets)
        self.assertEqual(* G, self.planet)