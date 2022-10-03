from Utils import Point, Velocity, Acceleration


class Planet:
    def __init__(self, **kwargs):
        self.__name = kwargs.get('name', '1')
        self.__mass = kwargs.get('mass', 0)
        self.__point = kwargs.get('point', Point())
        self.__velocity = kwargs.get('velocity', Velocity())
        self.__prevPoint = None
        self.plotPoint = None

    def __eq__(self, other):
        if not isinstance(other, Planet):
            return NotImplemented

        return self.name == other.name

    def __str__(self):
        return f'{self.__name}:\nMass: {self.__mass}\nPoint: {self.point}\nVelocity: {self.velocity}'

    @property
    def mass(self):
        return self.__mass

    @property
    def point(self):
        return self.__point

    @property
    def velocity(self):
        return self.__velocity

    @property
    def name(self):
        return self.__name

    @property
    def prevPoint(self):
        return self.__prevPoint

    @mass.setter
    def mass(self, mass) -> None:
        self.__mass = mass

    @point.setter
    def point(self, point) -> None:
        self.__point = point

    @velocity.setter
    def velocity(self, velocity) -> None:
        self.__velocity = velocity

    @prevPoint.setter
    def prevPoint(self, prevPoint) -> None:
        self.__prevPoint = prevPoint

    def update(self):
        self.plotPoint[0].set_data_3d(self.point.x, self.point.y, self.point.z)
