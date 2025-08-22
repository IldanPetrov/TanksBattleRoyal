# engine/map_service.py
import pygame

from engine.destructible_object import DestructibleObject
from engine.game_object import GameObject
from engine.visual_object import VisualObject
from engine.material_object import MaterialObject
from game.bullet import Bullet


class Wall(MaterialObject, VisualObject):
    def __init__(self, x, y, dir=0):
        name = "Wall"
        sprite = "WallTexture.png"
        VisualObject.__init__(self, name, sprite=sprite, render_height=2, length=80, width=20)
        MaterialObject.__init__(self, name, x=x, y=y, dir=dir, length=80, width=20, collision=True)


class Box(MaterialObject, VisualObject, DestructibleObject):
    def __init__(self, x, y, dir=0, hp=40):
        name = "Box"
        sprite = "BoxTexture.jpg"
        VisualObject.__init__(self, name, sprite=sprite, render_height=2, length=200, width=200)
        MaterialObject.__init__(self, name, x=x, y=y, dir=dir, length=200, width=200, collision=True)
        DestructibleObject.__init__(self, hp)


class Field(VisualObject):
    def __init__(self, width, height):
        VisualObject.__init__(self, "Field", sprite="FieldTexture.png", render_height=-1,
                              length=height, width=width, x=width // 2, y=height // 2)


class MapService:
    def __init__(self, width=2000, height=2000, wall_step=80):
        self.width = width
        self.height = height
        self.wall_step = wall_step

    def generate(self):
        # поле
        Field(self.width, self.height)

        # стены по периметру
        for x in range(self.wall_step // 2, self.width, self.wall_step):
            Wall(x, 0)
            Wall(x, self.height)
        for y in range(self.wall_step // 2, self.height, self.wall_step):
            Wall(0, y, dir=90)
            Wall(self.width, y, dir=90)

        # несколько случайных препятствий
        Box(600, 600)
        Box(1000, 1000)
        Box(1400, 1400)

        return []
