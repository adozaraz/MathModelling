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
        acceleration = Acceleration()
        for planet in self.planets:
            for secondPlanet in self.planets:
                if secondPlanet == planet:
                    continue
                acceleration += Acceleration.calculateAcceleration(secondPlanet, planet)
            if self.scheme == SCHEMES.VERLET and planet.prevPoint is not None:
                prevPoint = planet.point
                planet.point = Point(2*planet.point.x - planet.prevPoint.x + acceleration.x * self.dt ** 2,
                                     2*planet.point.y - planet.prevPoint.y + acceleration.y * self.dt ** 2,
                                     2*planet.point.z - planet.prevPoint.z + acceleration.z * self.dt ** 2)
                planet.velocity = Velocity((planet.point.x - 2 * planet.prevPoint.x) / 2,
                                           (planet.point.x - 2 * planet.prevPoint.x) / 2,
                                           (planet.point.x - 2 * planet.prevPoint.x) / 2)
                planet.prevPoint = prevPoint
            elif self.scheme == SCHEMES.EULER_KRAMER:
                planet.point = Point(planet.point.x + planet.velocity.x * self.dt + acceleration.x * self.dt ** 2,
                                     planet.point.y + planet.velocity.y * self.dt + acceleration.y * self.dt ** 2,
                                     planet.point.z + planet.velocity.z * self.dt + acceleration.z * self.dt ** 2)
            else:
                planet.point = Point(planet.point.x + planet.velocity.x * self.dt,
                                     planet.point.y + planet.velocity.y * self.dt,
                                     planet.point.z + planet.velocity.z * self.dt)
                planet.velocity = Velocity(acceleration.x * self.dt,
                                           acceleration.y * self.dt,
                                           acceleration.z * self.dt)

    def updateCanvas(self, i):
        self.calculateStep()
        self.frameText.set_text(f'Frame: {i}/{self.timeLimit / self.dt}')
        for planet in self.planets:
            planet.update()
