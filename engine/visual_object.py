import pygame, os

from engine.game_object import GameObject
from engine.utils import rotate_point


class VisualObject(GameObject):
    def __init__(self, name, sprite=None, render_height=0, visible=True, length=40, width=40, **kwargs):
        super().__init__(name, kwargs.get("x", 0), kwargs.get("y", 0), kwargs.get("dir", 0), kwargs.get("parent"))
        self.visible = visible
        self.render_height = render_height
        self.sprites = {}
        self.active_sprite = None
        if sprite:
            self.add_sprite("default", sprite, (length, width))
            self.active_sprite = "default"

    def add_sprite(self, key, filename, size=None):
        path = os.path.join("assets/sprites", filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Sprite not found: {path}")
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        self.sprites[key] = img

    def render(self, surface, camera):
        if not self.visible or not self.active_sprite:
            return

        sprite = self.sprites[self.active_sprite]

        screen_w, screen_h = surface.get_size()

        # глобальные координаты и угол объекта
        obj_x, obj_y = self.get_position(global_=True)
        obj_dir = self.get_dir(global_=True)

        # глобальные координаты и угол камеры
        cam_x, cam_y = camera.get_position(global_=True)
        cam_dir = camera.get_dir(global_=True)

        if camera.parent and not getattr(__import__('settings'), 'DIR_POV', False):
            cam_dir = 0

        # перенос в систему камеры
        dx, dy = obj_x - cam_x, obj_y - cam_y
        dx, dy = rotate_point((dx, dy), -cam_dir, base=(0, 0))

        # применяем зум
        dx, dy = dx * camera.zoom, dy * camera.zoom

        # экранные координаты
        screen_x = dx + screen_w // 2
        screen_y = dy + screen_h // 2

        # угол объекта в экранной системе
        wdir = obj_dir - cam_dir

        # рендер спрайта
        surf = pygame.transform.rotozoom(sprite, -wdir, camera.zoom)
        rect = surf.get_rect(center=(screen_x, screen_y))
        surface.blit(surf, rect)