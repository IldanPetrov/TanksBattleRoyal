import pygame
import sys
import settings
from game.world import World
from entities.tank import Tank


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Tank Battle Royale - Tank with Sprites")
    clock = pygame.time.Clock()

    world = World()
    tank = Tank(500, 500)

    running = True
    mouse_wheel = 0
    while running:
        mouse_wheel = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                mouse_wheel = event.y
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    tank.shoot()
            world.handle_mouse(event)

        keys = pygame.key.get_pressed()
        world.handle_input(keys, mouse_wheel)
        tank.handle_input(keys)
        tank.update()

        screen.fill((100, 100, 100))
        world.draw(screen)
        tank.draw(screen, world.camera)

        pygame.display.flip()
        clock.tick(settings.FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
