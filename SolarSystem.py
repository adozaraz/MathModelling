from Utils import *
import copy

class SolarSystem:
    def __init__(self, planets=None, timeLimit=1E20, dt=3600, scheme=SCHEMES.EULER):
        if planets is None:
            planets = []
        self.planets = planets
        self.timeLimit = timeLimit
        self.dt = dt
        self.scheme = scheme
        self.frameText = None
        self.blit = []

    def calculateStep(self):
        acceleration = Acceleration()
        planetsCopy = copy.deepcopy(self.planets)
        for planet in self.planets:
            for secondPlanet in planetsCopy:
                if secondPlanet == planet:
                    continue
                acceleration += Acceleration.calculateAcceleration(secondPlanet, planet)
            prevPoint = planet.point
            if self.scheme == SCHEMES.VERLET and planet.prevPoint is not None:
                planet.point = Point(2*prevPoint.x - planet.prevPoint.x + acceleration.x * self.dt ** 2,
                                     2*prevPoint.y - planet.prevPoint.y + acceleration.y * self.dt ** 2,
                                     2*prevPoint.z - planet.prevPoint.z + acceleration.z * self.dt ** 2)
                planet.velocity = Velocity((prevPoint.x - 2 * planet.prevPoint.x) / 2,
                                           (prevPoint.x - 2 * planet.prevPoint.x) / 2,
                                           (prevPoint.x - 2 * planet.prevPoint.x) / 2)
                planet.prevPoint = prevPoint
            elif self.scheme == SCHEMES.EULER_KRAMER:
                planet.point = Point(prevPoint.x + planet.velocity.x * self.dt + acceleration.x * self.dt ** 2,
                                     prevPoint.y + planet.velocity.y * self.dt + acceleration.y * self.dt ** 2,
                                     prevPoint.z + planet.velocity.z * self.dt + acceleration.z * self.dt ** 2)
                planet.velocity = Velocity(planet.velocity.x + acceleration.x * self.dt,
                                           planet.velocity.y + acceleration.y * self.dt,
                                           planet.velocity.z + acceleration.z * self.dt)
            else:
                planet.point = Point(prevPoint.x + planet.velocity.x * self.dt,
                                     prevPoint.y + planet.velocity.y * self.dt,
                                     prevPoint.z + planet.velocity.z * self.dt)
                planet.velocity = Velocity(planet.velocity.x + acceleration.x * self.dt,
                                           planet.velocity.y + acceleration.y * self.dt,
                                           planet.velocity.z + acceleration.z * self.dt)
            planet.prevPoint = prevPoint
            acceleration = Acceleration()

    def updateCanvas(self, i):
        self.calculateStep()
        for index in range(len(self.planets)):
            self.planets[index].update()
            self.blit[index].set_data_3d(self.planets[index].point.x, self.planets[index].point.y, self.planets[index].point.z)
        self.blit[-1].set_text(f'Frame: {i}/{self.timeLimit / self.dt}')
        return self.blit


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
