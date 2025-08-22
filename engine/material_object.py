# material_object.py
import math

import pygame

from engine.destructible_object import DestructibleObject
from engine.dynamic_object import DynamicObject
from engine.game_object import GameObject


class MaterialObject(GameObject):
    registry = []

    def __init__(self, name, length=40, width=40, collision=True, **kwargs):
        GameObject.__init__(self, name, kwargs.get("x", 0), kwargs.get("y", 0), kwargs.get("dir", 0),
                            kwargs.get("parent", None))
        self.length = length
        self.width = width
        self.collision = collision

        MaterialObject.registry.append(self)

    def get_hitbox(self):
        x, y = self.get_position(global_=True)
        return pygame.Rect(x - self.width // 2, y - self.length // 2, self.width, self.length)

    def collided_to(self, other: "MaterialObject"):
        """Поведение по умолчанию: динамика останавливается"""
        if isinstance(self, DynamicObject):
            self.speed = 0
            self.rot_speed = 0
            self._x -= math.cos(math.radians(self._dir)) * 2
            self._y -= math.sin(math.radians(self._dir)) * 2
