# game_object.py

import math
from idlelib.window import registry

from engine.utils import rotate_point


class GameObject:
    registry = []

    def __init__(self, name, x=0, y=0, dir=0, parent=None):
        self.name = name
        self._x, self._y, self._dir = x, y, dir
        self.parent = None
        self.children = []
        if parent:
            self.pin_to(parent)

        GameObject.registry.append(self)

    # ====== Pinning ======
    def pin_to(self, parent):
        if self.parent:
            self.unpin()

        pos = self.get_position()
        d = self.get_dir()
        self.parent = parent
        parent.children.append(self)
        self.set_position(*pos)
        self.set_dir(d)

    def unpin(self):
        if self.parent:
            pos = self.get_position()
            d = self.get_dir()
            self.parent.children.remove(self)
            self.set_position(*pos)
            self.set_dir(d)
        self.parent = None

    # ====== Position ======
    def set_position(self, x, y, global_=True):
        if self.parent and global_:
            px, py = self.parent.get_position(global_=True)
            pd = self.parent.get_dir(global_=True)
            lx, ly = rotate_point((x, y), -pd, base=(px, py))
            self._x, self._y = lx - px, ly - py
        else:
            self._x, self._y = x, y

    def get_position(self, global_=True):
        if self.parent and global_:
            px, py = self.parent.get_position(global_=True)
            pd = self.parent.get_dir(global_=True)
            gx, gy = rotate_point((self._x, self._y), pd)
            return px + gx, py + gy
        return self._x, self._y

    # ====== Direction ======
    def set_dir(self, angle, global_=True):
        if self.parent and global_:
            pd = self.parent.get_dir(global_=True)
            self._dir = angle - pd
        else:
            self._dir = angle

    def get_dir(self, global_=True):
        if self.parent and global_:
            return self.parent.get_dir(global_=True) + self._dir
        return self._dir
