import pygame
import settings
from engine.physics_service import PhysicsService
from engine.camera import Camera
from game.gun import Gun
from game.hull import Hull
from game.tank import Tank


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    physics = PhysicsService()

    # создаём игрока
    player = Tank(Hull, Gun, 400, 300)
    player.hull.speed = 20
    player.hull.rot_speed = -20

    # камеры
    global_camera = Camera(zoom=0.5)
    pov_camera = Camera(zoom=1.0, parent=player)
    pov_camera.set_dir(90, False)

    pov_mode = False
    running = True

    while running:
        dt = clock.tick(settings.FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                pov_mode = not pov_mode

        # обновление
        physics.update_all(dt)

        # рендер
        screen.fill((80, 80, 80))
        if pov_mode:
            physics.render_all(screen, pov_camera)
        else:
            physics.render_all(screen, global_camera)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
