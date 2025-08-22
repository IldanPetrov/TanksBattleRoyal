# physics_service.py
import math

import pygame

from engine.destructible_object import DestructibleObject
from engine.game_object import GameObject
from engine.material_object import MaterialObject
from engine.dynamic_object import DynamicObject


class PhysicsService:
    def __init__(self):
        pass

    def update_all(self, dt):
        for obj in GameObject.registry:
            if hasattr(obj, 'update'):
                obj.update(dt)

    # engine/physics_service.py
    def check_collisions(self):
        material_objs = [obj for obj in MaterialObject.registry if obj.collision]

        for i, a in enumerate(material_objs):
            rect_a = a.get_hitbox()
            for b in material_objs[i + 1:]:
                rect_b = b.get_hitbox()
                if rect_a.colliderect(rect_b):
                    # Просто уведомляем объекты
                    a.collided_to(b)
                    b.collided_to(a)
