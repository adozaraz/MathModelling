import Utils


class Planet:
    def __init__(self, **kwargs):
        self.__name = kwargs['name']
        self.__mass = kwargs['mass']
        self.__point = kwargs['point']
        self.__velocity = kwargs['velocity']

    def __eq__(self, other):
        if not isinstance(other, Planet):
            return NotImplemented

        return self.name == other.name

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