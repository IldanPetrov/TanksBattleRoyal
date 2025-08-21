import pygame
import math
import os
from game.utils import scale_value


def load_sprite(name, size):
    path = os.path.join("sprites", f"{name}.png")
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)


class Bullet:
    def __init__(self, x, y, angle, dmg, speed, range_, lvl=0):
        self.base_dmg = dmg
        self.base_speed = speed
        self.base_range = range_
        self.lvl = lvl

        self.dmg = scale_value(dmg, lvl)
        self.speed = scale_value(speed, lvl)
        self.range = scale_value(range_, lvl)

        self.x = x
        self.y = y
        self.angle = angle
        self.distance_traveled = 0
        self.alive = True
        self.sprite = None  # загружаем в наследнике

    def update(self):
        if not self.alive:
            return
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed
        self.distance_traveled += self.speed
        if self.distance_traveled > self.range:
            self.alive = False

    def draw(self, screen, camera):
        if not self.alive:
            return
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=camera.world_to_screen(self.x, self.y))
        screen.blit(rotated, rect)


class StandardBullet(Bullet):
    def __init__(self, x, y, angle, lvl=0):
        super().__init__(x, y, angle, dmg=10, speed=10, range_=500, lvl=lvl)
        self.sprite = load_sprite(self.__class__.__name__, (10, 5))
