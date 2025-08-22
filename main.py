# main.py
import pygame
import settings
from engine.physics_service import PhysicsService
from engine.render_service import RenderService
from engine.map_service import MapService
from engine.camera import Camera
from game.tank import Tank
from game.hull import StandardHull
from game.gun import StandardGun


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    physics = PhysicsService()
    render = RenderService()
    map_service = MapService(2000, 2000)

    # карта
    game_objects = map_service.generate()

    # создаём игрока
    player = Tank(StandardHull, StandardGun, 400, 300)
    game_objects.append(player)

    # камеры
    # main.py (фрагмент)
    global_camera = Camera(zoom=0.8)
    global_camera.set_position(1000, 1000)

    zoom_speed = 0.1
    move_speed = 300

    pov_camera = Camera(zoom=1.0, parent=player)
    pov_camera.set_dir(90, False)

    pov_mode = False
    running = True

    dragging = False
    last_mouse_pos = None

    while running:
        dt = clock.tick(settings.FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                pov_mode = not pov_mode

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                dragging = True
                last_mouse_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging and not pov_mode:
                mx, my = pygame.mouse.get_pos()
                dx, dy = mx - last_mouse_pos[0], my - last_mouse_pos[1]
                global_camera._x -= dx / global_camera.zoom
                global_camera._y -= dy / global_camera.zoom
                last_mouse_pos = (mx, my)
            elif event.type == pygame.MOUSEWHEEL:
                if pov_mode:
                    pov_camera.zoom *= 1 + event.y * 0.1
                else:
                    global_camera.zoom *= 1 + event.y * 0.1
                # Ограничим зум
                global_camera.zoom = max(0.2, min(3.0, global_camera.zoom))
                pov_camera.zoom = max(0.5, min(2.0, pov_camera.zoom))

        keys = pygame.key.get_pressed()

        # движение танка
        if keys[pygame.K_UP]:
            player.hull.speed = player.hull.max_speed
        elif keys[pygame.K_DOWN]:
            player.hull.speed = -player.hull.max_speed
        else:
            player.hull.speed = 0

        if keys[pygame.K_LEFT]:
            player.hull.rot_speed = -player.hull.max_rot_speed
        elif keys[pygame.K_RIGHT]:
            player.hull.rot_speed = player.hull.max_rot_speed
        else:
            player.hull.rot_speed = 0

        if keys[pygame.K_z]:
            player.gun.rot_speed = -60
        elif keys[pygame.K_x]:
            player.gun.rot_speed = 60
        else:
            player.gun.rot_speed = 0

        if keys[pygame.K_SPACE]:
            player.gun.shoot(pygame.time.get_ticks() / 1000, player.ammo)

        # обновление
        physics.update_all(dt)
        physics.check_collisions()

        # рендер
        screen.fill((80, 80, 80))
        if pov_mode:
            render.render_all(screen, pov_camera)
        else:
            render.render_all(screen, global_camera)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
