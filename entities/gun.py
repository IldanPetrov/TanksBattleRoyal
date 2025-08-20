from abc import ABC, abstractmethod
from entities.utils import scale_value
from entities.bullet import StandardBullet


class Gun(ABC):
    def __init__(self, hp, rot_speed, cooldown, shoot_cost, bullet_type, lvl=0):
        self.base_hp = hp
        self.base_rot_speed = rot_speed
        self.base_cooldown = cooldown
        self.base_shoot_cost = shoot_cost
        self.bullet_type = bullet_type
        self.lvl = lvl

        self.hp = scale_value(hp, lvl)
        self.rot_speed = scale_value(rot_speed, lvl)
        self.cooldown = scale_value(cooldown, lvl, val_k=0.9)  # скорость ↑, значит время ↓
        self.shoot_cost = scale_value(shoot_cost, lvl, val_k=1.1)

        self.dir = 0  # относительный угол башни
        self.timer = 0

    @abstractmethod
    def get_type(self):
        pass

    def can_shoot(self, ammo):
        return ammo >= self.shoot_cost and self.timer == 0

    def update(self):
        if self.timer > 0:
            self.timer -= 1


class StandardGun(Gun):
    def __init__(self, lvl=0):
        super().__init__(hp=20, rot_speed=3, cooldown=30, shoot_cost=1, bullet_type=StandardBullet, lvl=lvl)

    def get_type(self):
        return "Standard Gun"
