import pygame
import sys
import settings
from core.physics_service import PhysicsService
from core.game_object import GameObject
from core.camera import Camera


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Tank Battle Royale - Camera Test")
    clock = pygame.time.Clock()

    physics = PhysicsService()

    # корпус
    hull = GameObject(sprite="StandardHull.png", width=70, length=50, render_height=0)
    hull.set_position(400, 300, global_=True)

    # башня
    gun = GameObject(sprite="StandardGun.png", width=80, length=33, render_height=1, parent=hull)
    gun.set_position(0, 0, global_=False)
    gun.set_dir(0, global_=False)

    # камера (POV на танк)
    pov_camera = Camera(zoom=1.0, parent=hull)
    pov_camera.set_position(0, 0, global_=False)  # сзади танка
    pov_camera.set_dir(90, global_=False)

    global_camera = Camera(zoom=0.5)
    global_camera.set_position(0, 0)

    pov_mode = True

    running = True
    while running:
        dt = clock.tick(settings.FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    # переключение режима камеры
                    pov_mode = not pov_mode

        # тестовое вращение
        hull.rot_speed = 40
        gun.rot_speed = 80

        physics.update_all(dt)

        screen.fill((100, 100, 100))
        if pov_mode:
            physics.render_all(screen, pov_camera)
        else:
            physics.render_all(screen, global_camera)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
