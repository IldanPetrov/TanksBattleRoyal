from abc import ABC, abstractmethod
from entities.utils import scale_value


class Hull(ABC):
    def __init__(self, hp, speed, rot_speed, lvl=0):
        self.base_hp = hp
        self.base_speed = speed
        self.base_rot_speed = rot_speed
        self.lvl = lvl

        self.hp = scale_value(hp, lvl)
        self.speed = scale_value(speed, lvl)
        self.rot_speed = scale_value(rot_speed, lvl)

        self.dir = 0  # направление корпуса

    @abstractmethod
    def get_type(self):
        pass


class StandardHull(Hull):
    def __init__(self, lvl=0):
        super().__init__(hp=100, speed=3, rot_speed=3, lvl=lvl)

    def get_type(self):
        return "Standard Hull"
