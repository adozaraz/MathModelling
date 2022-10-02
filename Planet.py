import Utils


class Planet:
    def __init__(self, **kwargs):
        self.__name = kwargs['name']
        self.__mass = kwargs['mass']
        self.__point = kwargs['point']
        self.__velocity = kwargs['velocity']
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

    @mass.setter
    def mass(self, mass) -> None:
        self.__mass = mass

    @point.setter
    def point(self, point) -> None:
        self.__point = point

    @velocity.setter
    def velocity(self, velocity) -> None:
        self.__velocity = velocity

    def update(self):
        self.plotPoint[0].set_data_3d(self.point.x, self.point.y, self.point.z)
