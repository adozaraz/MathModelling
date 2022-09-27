import Utils


class Planet:
    def __init__(self, **kwargs):
        self.__mass = kwargs['mass']
        self.__point = kwargs['point']
        self.__velocity = kwargs['velocity']
        self.__acceleration = kwargs['acceleration']
        self.__line = kwargs['line']

    def __eq__(self, other):
        if not isinstance(other, Planet):
            return NotImplemented

        return self.mass == other.mass and self.point == other.point \
               and self.velocity == other.velocity and self.acceleration == other.acceleration

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
    def acceleration(self):
        return self.__acceleration

    @mass.setter
    def mass(self, mass) -> None:
        self.__mass = mass

    @point.setter
    def point(self, point) -> None:
        self.__point = point

    @velocity.setter
    def velocity(self, velocity) -> None:
        self.__velocity = velocity

    @acceleration.setter
    def acceleration(self, acceleration) -> None:
        self.__acceleration = acceleration

    def calculateStep(self, time: float, dt: float, planets, scheme: int = 0) -> None:
        """
        :param dt: Шаг по времени
        :param planets: Все планеты
        :param time: Текущее время шага
        :param scheme: По какому методу будет вычисляться
        :return: None
        """
        if scheme == Utils.SCHEMES.EULER:
            self.acceleration = Utils.Acceleration(0, 0, 0)
            for planet in planets:
                if self == planet:
                    continue
                self.acceleration += Utils.Acceleration.calculateAcceleration(self.point, planet.point)
            self.point.updatePointRelativeToVelocityAndAcceleration(self.velocity, dt, self.acceleration)
            self.velocity.updateVelocityRelativeToAcceleration(self.acceleration, dt)
