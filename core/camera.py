import math
import settings
from core.game_object import GameObject
from core.utils import rotate_point


class Camera(GameObject):
    def __init__(self, zoom=1.0, parent=None):
        super().__init__(name="Camera", visible=False, collision=False, parent=parent)
        self.zoom = zoom

    def world_to_screen(self, wx, wy, surface):
        cx, cy = self.get_position(global_=True)
        cd = self.get_dir(global_=True)

        dx, dy = wx - cx, wy - cy

        if settings.DIR_POV:
            dx, dy = rotate_point((dx, dy), -cd)

        dx *= self.zoom
        dy *= self.zoom

        screen_w, screen_h = surface.get_size()
        sx = dx + screen_w // 2
        sy = dy + screen_h // 2
        return sx, sy

    def screen_to_world(self, sx, sy, surface):
        """Перевод экранных координат в глобальные"""
        cx, cy = self.get_position(global_=True)
        cd = self.get_dir(global_=True)

        screen_w, screen_h = surface.get_size()
        dx = (sx - screen_w // 2) / self.zoom
        dy = (sy - screen_h // 2) / self.zoom

        # если POV, то возвращаем обратно поворот
        if settings.DIR_POV:
            dx, dy = rotate_point((dx, dy), cd)

        wx, wy = cx + dx, cy + dy
        return wx, wy
