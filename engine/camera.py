# camera.py

from engine.game_object import GameObject


class Camera(GameObject):
    def __init__(self, x=0, y=0, dir=0, zoom=1.0, parent=None):
        super().__init__("Camera", x, y, dir, parent)
        if parent:
            self.set_position(0, 0, False)
            self.set_dir(0, False)
        self.zoom = zoom
