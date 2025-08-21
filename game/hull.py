from engine.dynamic_object import DynamicObject
from engine.visual_object import VisualObject


class Hull(DynamicObject, VisualObject):
    def __init__(self, sprite="StandardHull.png", max_speed=120, max_rot_speed=60, length=70, width=50, armor=80, lvl=0):
        DynamicObject.__init__(self, "Hull", speed=0, rot_speed=0)
        VisualObject.__init__(self, "Hull", sprite=sprite, render_height=0, length=length, width=width)

        self.armor = armor
        self.max_speed = max_speed
        self.max_rot_speed = max_rot_speed
        self.lvl = lvl
