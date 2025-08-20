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
    hull = GameObject(sprite="StandardHull.png", width=80, length=80, render_height=0)
    hull.set_position(400, 300, global_=True)

    # башня
    gun = GameObject(sprite="StandardGun.png", width=60, length=20, render_height=1, parent=hull)
    gun.set_position(0, 0, global_=False)

    # камера (POV на танк)
    camera = Camera(zoom=1.0, parent=hull)
    camera.set_position(0, -150, global_=False)  # сзади танка
    camera.set_dir(0, global_=False)

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
                    if pov_mode:
                        camera.pin_to(hull)
                        camera.set_position(0, -150, global_=False)
                        camera.set_dir(0, global_=False)
                    else:
                        camera.unpin()
                        camera.set_position(400, 300, global_=True)

        # тестовое вращение
        hull.rot_speed = 40
        gun.rot_speed = 80

        physics.update_all(dt)

        screen.fill((100, 100, 100))
        physics.render_all(screen, camera)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
