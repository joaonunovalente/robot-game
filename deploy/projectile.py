class Projectile:
    def __init__(self, x, y, image, speed=500):
        self.image = image
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, dt):
        self.y -= self.speed * dt
        self.rect.y = int(self.y)

    def draw(self, window):
        window.blit(self.image, self.rect)

    def get_rect(self):
        return self.rect