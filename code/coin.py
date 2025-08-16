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
        if self.y < self.window.get_height() - self.image.get_height():
            self.y += self.velocity