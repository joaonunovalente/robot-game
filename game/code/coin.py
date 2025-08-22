import pygame

class Coin:
    def __init__(self, x, y, image, window):
        self.x = x
        self.y = y
        self.image = image
        self.velocity = 1
        self.window = window

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def update(self):
        self.y += self.velocity

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

