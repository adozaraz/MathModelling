import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib
from Utils import *
from Planet import Planet
matplotlib.use("TkAgg")
AU = 1.5e11

class SolarSystem:
    def __init__(self, planets=None, timeLimit=1E20, dt=3600, scheme: int = 0):
        if planets is None:
            planets = []
        self.planets = planets
        self.timeLimit = timeLimit
        self.dt = dt
        self.scheme = scheme
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = plt.axes(projection='3d')
        self.ax.axis('auto')
        self.axis_size = 2.5
        self.ax.set_xlim(-self.axis_size * AU, self.axis_size * AU)
        self.ax.set_ylim(-self.axis_size * AU, self.axis_size * AU)
        self.ax.set_zlim(-self.axis_size * AU, self.axis_size * AU)
        self.x = []
        self.y = []
        self.z = []

    def calculateStep(self):
        if self.scheme == SCHEMES.EULER:
            for planet in self.planets:
                acceleration = Acceleration()
                for secondPlanet in self.planets:
                    if secondPlanet == planet:
                        continue
                    acceleration += Acceleration.calculateAcceleration(planet, secondPlanet)
                planet.point.updatePointRelativeToVelocityAndAcceleration(planet.velocity, self.dt, acceleration)
                planet.velocity.updateVelocityRelativeToAcceleration(acceleration, self.dt)

    def updateCanvas(self, i):
        self.calculateStep()
        self.ax.clear()
        for planet in self.planets:
            self.ax.plot([planet.point.x], [planet.point.y], [planet.point.z], marker='o', markersize=7, markeredgecolor="black", markerfacecolor="black")


if __name__ in "__main__":
    solarSystem = SolarSystem([Planet(name="Earth", mass=100, point=Point(), velocity=Velocity()),
                               Planet(name="Mars", mass=1000, point=Point(4*AU, 4*AU, 4*AU), velocity=Velocity(AU, 0, 0))])
    ani = animation.FuncAnimation(solarSystem.fig, solarSystem.updateCanvas, interval=100)
    plt.show()