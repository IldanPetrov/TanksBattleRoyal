# engine/render_service.py

import pygame

from engine.utils import rotate_point
from engine.visual_object import VisualObject



class RenderService:
    def __init__(self):
        pass

    def render_all(self, surface, camera):
        screen_w, screen_h = surface.get_size()
        # сортировка по render_height
        objects_to_render = [o for o in VisualObject.registry if o.visible]
        objects_to_render.sort(key=lambda o: o.render_height)

        for obj in objects_to_render:
            if not obj.active_sprite:
                continue

            sprite = obj.sprites[obj.active_sprite]


            # глобальные координаты и угол объекта
            obj_x, obj_y = obj.get_position(global_=True)
            obj_dir = obj.get_dir(global_=True)

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