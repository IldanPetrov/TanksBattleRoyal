# visual_object

import pygame, os

from engine.game_object import GameObject
from engine.utils import rotate_point


class VisualObject(GameObject):
    registry = []

    def __init__(self, name, sprite=None, render_height=0, visible=True, length=40, width=40, **kwargs):
        # print((name, kwargs.get("x", 0), kwargs.get("y", 0), kwargs.get("dir", 0), kwargs.get("parent")))
        GameObject.__init__(self, name, kwargs.get("x", 0), kwargs.get("y", 0), kwargs.get("dir", 0), kwargs.get("parent"))
        self.visible = visible
        self.render_height = render_height
        self.sprites = {}
        self.active_sprite = None
        if sprite:
            self.add_sprite("default", sprite, (length, width))
            self.active_sprite = "default"

        VisualObject.registry.append(self)

    def add_sprite(self, key, filename, size=None):
        path = os.path.join("assets/sprites", filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Sprite not found: {path}")
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        self.sprites[key] = img