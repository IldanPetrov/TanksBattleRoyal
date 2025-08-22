# game/bullet.py
import math

import pygame

from engine.destructible_object import DestructibleObject
from engine.dynamic_object import DynamicObject
from engine.game_object import GameObject
from engine.visual_object import VisualObject
from engine.material_object import MaterialObject


class Bullet(DynamicObject, VisualObject, MaterialObject):
    def __init__(self, sprite="StandardBullet.png", speed=400, dmg=10, range_=500, owner=None,
                 length=10, width=10, **kwargs):

        # Инициализируем каждую часть отдельно
        DynamicObject.__init__(self, "Bullet", **kwargs)
        VisualObject.__init__(self, "Bullet", sprite=sprite, render_height=2,
                              length=length, width=width, **kwargs)
        MaterialObject.__init__(self, "Bullet", length=length, width=width, collision=True, **kwargs)

        self.speed = speed
        self.dmg = dmg
        self.range = range_
        self.owner = owner
        self.distance_traveled = 0

    def update(self, dt):
        # движение
        DynamicObject.update(self, dt)
        self.distance_traveled += self.speed * dt

        # исчезновение после достижения дальности
        if self.distance_traveled > self.range:
            self.destroy()

    def collided_to(self, other):
        if other == self.owner:
            return
        if isinstance(other, DestructibleObject):
            other.get_dmg(self.dmg, pygame.time.get_ticks())
        self.destroy()

    def destroy(self):
        if self in GameObject.registry:
            GameObject.registry.remove(self)
        if self in VisualObject.registry:
            VisualObject.registry.remove(self)
        if self in MaterialObject.registry:
            MaterialObject.registry.remove(self)

        del self

class StandardBullet(Bullet):
    def __init__(self, owner=None, lvl=0):
        super().__init__(sprite="StandardBullet.png", speed=400, dmg=10, range_=500,
                         owner=owner, length=10, width=10)
        self.lvl = lvl
