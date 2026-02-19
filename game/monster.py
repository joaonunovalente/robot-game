import pygame


class Monster:
    def __init__(self, x, y, image, window):
        self.x = x
        self.y = y
        self.image = image
        self.window = window
        self.speed = 300

    def update(self, dt):
        self.y += self.speed * dt

    # Fix draw to accept window
    def draw(self, window=None):
        # If window is passed, use it; otherwise use self.window
        target_window = window if window else self.window
        target_window.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())