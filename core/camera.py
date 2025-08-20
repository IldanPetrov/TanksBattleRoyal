import math
import settings
from core.game_object import GameObject
from core.utils import rotate_point


class Camera(GameObject):
    def __init__(self, zoom=1.0, parent=None):
        super().__init__(name="Camera", visible=False, collision=False, parent=parent)
        self.zoom = zoom
