import matplotlib.pyplot as plt
from matplotlib import animation
from Utils import *


class SolarSystem:
    def __init__(self, planets=None, timeLimit=1E20, dt=3600, scheme=SCHEMES.EULER):
        if planets is None:
            planets = []
        self.planets = planets
        self.timeLimit = timeLimit
        self.dt = dt
        self.scheme = scheme
        self.frameText = None

    def calculateStep(self):
        if self.scheme == SCHEMES.EULER:
            for planet in self.planets:
                acceleration = Acceleration()
                for secondPlanet in self.planets:
                    if secondPlanet == planet:
                        continue
                    acceleration += Acceleration.calculateAcceleration(secondPlanet, planet)
                planet.point.updatePointRelativeToVelocityAndAcceleration(planet.velocity, self.dt, acceleration)
                planet.velocity.updateVelocityRelativeToAcceleration(acceleration, self.dt)

    def updateCanvas(self, i):
        self.calculateStep()
        self.frameText.set_text(f'Frame: {i}/{self.timeLimit / self.dt}')
        for planet in self.planets:
            planet.update()
