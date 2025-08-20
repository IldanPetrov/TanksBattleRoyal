import pygame
import settings


class Camera:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
        self.dragging = False
        self.drag_start = (0, 0)

    def handle_mouse(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.dragging = True
            self.drag_start = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = pygame.mouse.get_pos()
            dx = (mx - self.drag_start[0]) / self.zoom
            dy = (my - self.drag_start[1]) / self.zoom
            self.offset_x -= dx
            self.offset_y -= dy
            self.drag_start = (mx, my)

    def move(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy

    def apply(self, rect):
        return pygame.Rect(
            (rect.x - self.offset_x) * self.zoom,
            (rect.y - self.offset_y) * self.zoom,
            rect.width * self.zoom,
            rect.height * self.zoom
        )

    def world_to_screen(self, x, y):
        return (x - self.offset_x) * self.zoom, (y - self.offset_y) * self.zoom

    def screen_to_world(self, x, y):
        return x / self.zoom + self.offset_x, y / self.zoom + self.offset_y


class World:
    def __init__(self):
        self.width = settings.MAP_WIDTH
        self.height = settings.MAP_HEIGHT
        self.color = settings.MAP_COLOR
        self.camera = Camera()

    def handle_input(self, keys, mouse_wheel):
        # зум колесиком
        if mouse_wheel > 0:
            self.camera.zoom = min(self.camera.zoom + settings.ZOOM_STEP, settings.MAX_ZOOM)
        elif mouse_wheel < 0:
            self.camera.zoom = max(self.camera.zoom - settings.ZOOM_STEP, settings.MIN_ZOOM)

    def handle_mouse(self, event):
        self.camera.handle_mouse(event)

    def draw(self, screen):
        map_rect = pygame.Rect(0, 0, self.width, self.height)
        screen_rect = self.camera.apply(map_rect)
        pygame.draw.rect(screen, self.color, screen_rect)
        pygame.draw.rect(screen, settings.BORDER_COLOR, screen_rect, settings.BORDER_WIDTH)
