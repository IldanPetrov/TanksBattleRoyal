from engine.dynamic_object import DynamicObject
from engine.visual_object import VisualObject
import time


class Gun(DynamicObject, VisualObject):
    def __init__(self, sprite="StandardGun.png", max_rot_speed=90, cooldown=0.5, shoot_cost=1,
                 bullet_type=None, length=80, width=33, armor=20, lvl=0):
        DynamicObject.__init__(self, "Gun", max_rot_speed=0)
        VisualObject.__init__(self, "Gun", sprite=sprite, render_height=1, length=length, width=width)

        self.armor = 0
        self.max_rot_speed = max_rot_speed
        self.cooldown = cooldown
        self.shoot_cost = shoot_cost
        self.bullet_type = bullet_type
        self.lvl = lvl
        self.last_shot = 0

    def shoot(self, now, ammo):
        if now - self.last_shot < self.cooldown:
            return None
        if ammo < self.shoot_cost:
            return None
        self.last_shot = now
        ammo -= self.shoot_cost
        return self.bullet_type(self)
