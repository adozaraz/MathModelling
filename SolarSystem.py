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
                prevPoint = planet.point
                planet.point = Point(planet.point.x + planet.velocity.x * self.dt,
                                     planet.point.y + planet.velocity.y * self.dt,
                                     planet.point.z + planet.velocity.z * self.dt)
                planet.velocity = Velocity(acceleration.x * self.dt,
                                           acceleration.y * self.dt,
                                           acceleration.z * self.dt)
                planet.prevPoint = prevPoint

    def updateCanvas(self, i):
        self.calculateStep()
        self.frameText.set_text(f'Frame: {i}/{self.timeLimit / self.dt}')
        for planet in self.planets:
            planet.update()

    def calculateMassCenter(self):
        planetMass = 0
        c = [0, 0, 0]
        for planet in self.planets:
            planetMass += planet.mass
            c[0] += planet.mass * planet.point.x
            c[1] += planet.mass * planet.point.y
            c[2] += planet.mass * planet.point.z
        c[0] /= planetMass
        c[1] /= planetMass
        c[2] /= planetMass
        return c

    def calculateUniversalEnergy(self):
        return self.calculatePotentialEnergy() + self.calculateKineticEnergy()

    def calculatePotentialEnergy(self):
        U = 0
        for i in range(len(self.planets)):
            for j in range(i+1, len(self.planets)):
                r = Point.calculateScalarDistance(self.planets[i].point, self.planets[j].point)
                U = G * self.planets[i].mass * self.planets[j].mass / r
        return U

    def calculateKineticEnergy(self):
        return sum(map(lambda planet: planet.mass * (planet.velocity.x**2 + planet.velocity.y ** 2 + planet.velocity.z ** 2) / 2, self.planets))
