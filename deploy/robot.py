import pygame

class Robot:
    def __init__(self, x, y, image, window):
        self.x = x
        self.y = y
        self.image = image
        self.window = window
        self.speed = 600  # pixels per second
        self.move_left = False
        self.move_right = False

    def set_movement(self, direction, is_moving):
        if direction == "left":
            self.move_left = is_moving
        elif direction == "right":
            self.move_right = is_moving

    def update(self, dt):
        if self.move_left:
            self.x -= self.speed * dt
        if self.move_right:
            self.x += self.speed * dt

        # Keep robot inside window boundaries
        if self.x < 0:
            self.x = 0
        if self.x > self.window.get_width() - self.image.get_width():
            self.x = self.window.get_width() - self.image.get_width()

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def get_position(self):
        return self.x, self.y

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
