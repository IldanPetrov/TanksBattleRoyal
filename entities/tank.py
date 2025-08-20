import pygame
import math
import os
from entities.hull import StandardHull
from entities.gun import StandardGun


def load_sprite(name, size):
    path = os.path.join("src", f"{name}.png")
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)


class Tank:
    def __init__(self, x, y, hull=None, gun=None):
        self.x = x
        self.y = y
        self.hull = hull if hull else StandardHull()
        self.gun = gun if gun else StandardGun()

        self.max_hp = self.hull.hp + self.gun.hp
        self.hp = self.max_hp
        self.patrons = 30
        self.gears = 0
        self.blueprints = 0
        self.bullets = []

        # загружаем картинки
        self.hull_img = load_sprite(self.hull.__class__.__name__, (40, 40))
        self.gun_img = load_sprite(self.gun.__class__.__name__, (40, 20))

    def handle_input(self, keys):
        if keys[pygame.K_UP]:
            self.move(1)
        if keys[pygame.K_DOWN]:
            self.move(-1)
        if keys[pygame.K_LEFT]:
            self.hull.dir -= self.hull.rot_speed
        if keys[pygame.K_RIGHT]:
            self.hull.dir += self.hull.rot_speed

        if keys[pygame.K_z]:
            self.gun.dir -= self.gun.rot_speed
        if keys[pygame.K_x]:
            self.gun.dir += self.gun.rot_speed

    def move(self, forward):
        rad = math.radians(self.hull.dir)
        self.x += math.cos(rad) * self.hull.speed * forward
        self.y += math.sin(rad) * self.hull.speed * forward

    def shoot(self):
        if self.gun.can_shoot(self.patrons):
            from entities.bullet import StandardBullet
            abs_angle = self.hull.dir + self.gun.dir
            bullet = StandardBullet(self.x, self.y, abs_angle, lvl=self.gun.lvl)
            self.bullets.append(bullet)
            self.patrons -= self.gun.shoot_cost
            self.gun.timer = self.gun.cooldown

    def update(self):
        self.gun.update()
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.alive]

    def draw(self, screen, camera):
        # корпус
        rotated_hull = pygame.transform.rotate(self.hull_img, -self.hull.dir)
        rect = rotated_hull.get_rect(center=camera.world_to_screen(self.x, self.y))
        screen.blit(rotated_hull, rect)

        # башня
        abs_angle = self.hull.dir + self.gun.dir
        rotated_gun = pygame.transform.rotate(self.gun_img, -abs_angle)
        gun_rect = rotated_gun.get_rect(center=camera.world_to_screen(self.x, self.y))
        screen.blit(rotated_gun, gun_rect)

        # пули
        for bullet in self.bullets:
            bullet.draw(screen, camera)
