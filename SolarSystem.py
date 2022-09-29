import matplotlib.pyplot as plt
from matplotlib import animation
from Utils import *


class SolarSystem:
    def __init__(self, planets=None, timeLimit=1E20, dt=3600, scheme=SCHEMES.EULER):
        AU = 1.5e11
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
                    acceleration += Acceleration.calculateAcceleration(secondPlanet, planet)
                planet.point.updatePointRelativeToVelocityAndAcceleration(planet.velocity, self.dt, acceleration)
                planet.velocity.updateVelocityRelativeToAcceleration(acceleration, self.dt)

    def updateCanvas(self, i):
        self.calculateStep()
        for planet in self.planets:
            planet.update()

    def show(self):
        for planet in self.planets:
            planet.plotPoint = self.ax.plot([planet.point.x], [planet.point.y], [planet.point.z], marker='o', markersize=7,
                         markeredgecolor="black", markerfacecolor="black")
        ani = animation.FuncAnimation(self.fig, self.updateCanvas, frames=int(self.timeLimit/self.dt))
        plt.show()
