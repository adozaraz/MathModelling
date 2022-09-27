import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib
from Utils import *
from Planet import Planet

matplotlib.use("TkAgg")
AU = 1.5e11


class SolarSystem:
    def __init__(self, planets=None, timeLimit=1E20, dt=3600, scheme=SCHEMES.EULER):
        if planets is None:
            planets = []
        self.planets = planets
        self.timeLimit = timeLimit
        self.dt = dt
        self.scheme = scheme
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = plt.axes(projection='3d')
        self.ax.axis('auto')
        self.axis_size = 10
        self.ax.set_xlim(-self.axis_size * AU, self.axis_size * AU)
        self.ax.set_ylim(-self.axis_size * AU, self.axis_size * AU)
        self.ax.set_zlim(-self.axis_size * AU, self.axis_size * AU)

    def calculateStep(self):
        if self.scheme == SCHEMES.EULER:
            for planet in self.planets:
                acceleration = Acceleration()
                for secondPlanet in self.planets:
                    if secondPlanet == planet:
                        continue
                    acceleration += Acceleration.calculateAcceleration(planet, secondPlanet)
                planet.updatePointRelativeToVelocityAndAcceleration(planet.velocity, self.dt, acceleration)
                planet.velocity.updateVelocityRelativeToAcceleration(acceleration, self.dt)

    def updateCanvas(self, i):
        self.calculateStep()
        for planet in self.planets:
            planet.update()
    def show(self):
        for planet in self.planets:
            planet.plotPoint = self.ax.plot([planet.point.x], [planet.point.y], [planet.point.z], marker='o', markersize=7,
                         markeredgecolor="black", markerfacecolor="black")
        ani = animation.FuncAnimation(self.fig, self.updateCanvas, frames=self.timeLimit)
        plt.show()


if __name__ in "__main__":
    solarSystem = SolarSystem(planets=[Planet(name="Earth", mass=1.2166E30, point=Point(), velocity=Velocity()),
                                       Planet(name="Mars", mass=6.083E24, point=Point(149500000000, 0, 0),
                                              velocity=Velocity(0, 23297.8704870374, 0)),
                                       Planet(name="Mars", mass=6.083E24, point=Point(-149500000000, 0, 0),
                                              velocity=Velocity(0, 23297.87048703))],
                              dt=3600, timeLimit=31536000)
    solarSystem.show()
