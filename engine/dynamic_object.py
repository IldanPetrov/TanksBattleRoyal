# dynamic_object.py

import math
from engine.game_object import GameObject


class DynamicObject(GameObject):
    def __init__(self, name, **kwargs):
        GameObject.__init__(self, name, kwargs.get("x", 0), kwargs.get("y", 0), kwargs.get("dir", 0), kwargs.get("parent"))
        self.speed = 0
        self.rot_speed = 0
        self.accel = 0
        self.rot_accel = 0

    def update(self, dt):
        if self.speed != 0:
            rad = math.radians(self._dir)
            self._x += math.cos(rad) * self.speed * dt
            self._y += math.sin(rad) * self.speed * dt
        if self.rot_speed != 0:
            self._dir += self.rot_speed * dt
