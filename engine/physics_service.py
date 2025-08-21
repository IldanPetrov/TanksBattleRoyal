import pygame
from engine.game_object import GameObject
from engine.material_object import MaterialObject
from engine.dynamic_object import DynamicObject
from engine.visual_object import VisualObject


class PhysicsService:
    def __init__(self):
        pass

    def update_all(self, dt):
        for obj in GameObject.registry:
            if isinstance(obj, DynamicObject):
                obj.update(dt)

    def render_all(self, surface, camera):
        for obj in sorted([obj for obj in GameObject.registry if isinstance(obj, VisualObject)],
                          key=lambda o: o.render_height):
            obj.render(surface, camera)

    def check_collisions(self):
        for i, a in enumerate([obj for obj in GameObject.registry if isinstance(obj, MaterialObject)]):
            if not a.collision:
                continue
            rect_a = pygame.Rect(*a.get_position(), a.width, a.length)
            for b in GameObject.registry[i + 1:]:
                if not b.collision:
                    continue
                rect_b = pygame.Rect(*b.get_position(), b.width, b.length)
                if rect_a.colliderect(rect_b):
                    print(f"Collision: {a.name} with {b.name}")
