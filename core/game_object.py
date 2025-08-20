import pygame
import os
import math
from core.utils import rotate_point, get_local_position, get_global_position


class GameCoreException(Exception):
    pass


class GameObject:
    registry = []

    def __init__(self, name=None, sprite=None, width=40, length=40, render_height=0,
                 visible=True, collision=False, parent=None):
        # локальные координаты
        self._x = 0
        self._y = 0
        self._dir = 0

        self.speed = 0
        self.rot_speed = 0

        self.visible = visible
        self.collision = collision
        self.width = width
        self.length = length
        self.render_height = render_height
        self.pinned = False

        self.parent = None
        self.children = []

        # имя и спрайт
        self.name = name if name else self.__class__.__name__
        self.sprite = None
        if sprite:
            self.load_sprite(sprite, (width, length))

        if parent:
            self.pin_to(parent)

        GameObject.registry.append(self)

    # ================= Sprite =================
    def load_sprite(self, filename, size):
        path = os.path.join("src", filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Sprite {path} not found")
        self.sprite = pygame.image.load(path).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, size)

    # ================= Parent/Child =================
    def pin_to(self, obj):
        if self.parent:
            self.unpin()
        self.parent = obj
        obj.children.append(self)
        self.pinned = True

    def unpin(self):
        if self.parent:
            self.parent.children.remove(self)
        self.parent = None
        self.pinned = False

    # ================= Position =================
    def set_position(self, x, y, global_=True):
        if self.pinned and global_:
            parent_pos = self.parent.get_position(global_=True)
            parent_dir = self.parent.get_dir(global_=True)
            local_x, local_y = get_local_position(parent_pos, parent_dir, (x, y))
            self.set_position(local_x, local_y, global_=False)
        elif not self.pinned and not global_:
            raise GameCoreException("Unpinned objects have only global position")
        else:
            self._x, self._y = x, y

    def get_position(self, global_=True):
        if self.pinned and global_:
            parent_pos = self.parent.get_position(global_=True)
            parent_dir = self.parent.get_dir(global_=True)
            return get_global_position(parent_pos, parent_dir, self.get_position(global_=False))
        elif not self.pinned and not global_:
            raise GameCoreException("Unpinned objects have only global position")
        else:
            return self._x, self._y

    # ================= Direction =================
    def set_dir(self, angle, global_=True):
        if self.pinned and global_:
            parent_dir = self.parent.get_dir(global_=True)
            self.set_dir(angle - parent_dir, global_=False)
        elif not self.pinned and not global_:
            raise GameCoreException("Unpinned objects have only global dir")
        else:
            self._dir = angle

    def get_dir(self, global_=True):
        if self.pinned and global_:
            return self.parent.get_dir(global_=True) + self._dir
        elif not self.pinned and not global_:
            raise GameCoreException("Unpinned objects have only global dir")
        else:
            return self._dir

    # ================= Lifecycle =================
    def update(self, dt):
        if self.speed != 0:
            dir_global = self.get_dir(global_=True)
            dx = math.cos(math.radians(dir_global)) * self.speed * dt
            dy = math.sin(math.radians(dir_global)) * self.speed * dt

            if self.pinned:
                # переводим глобальное смещение в локальное
                parent_dir = self.parent.get_dir(global_=True)
                lx, ly = rotate_point((dx, dy), -parent_dir, base=(0, 0))
                self._x += lx
                self._y += ly
            else:
                self._x += dx
                self._y += dy

        if self.rot_speed != 0:
            self._dir += self.rot_speed * dt

        for child in self.children:
            child.update(dt)

    def render(self, surface, camera):
        if not self.visible or not self.sprite:
            return

        cam_dir = camera.get_dir()
        if camera.pinned and getattr(__import__("settings"), "DIR_POV", False):
            cam_dir = 0

        wx, wy = get_local_position(camera.get_position(), cam_dir, self.get_position())
        wdir = self.get_dir() - cam_dir

        surf = pygame.transform.rotozoom(self.sprite, wdir, camera.zoom)
        rect = surf.get_rect()
        rect.center = (wx, wy)
        surface.blit(surf, rect)



