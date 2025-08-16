class Robot:
    def __init__(self, x, y, image, window):
        self.x = x
        self.y = y
        self.image = image
        self.to_left = False
        self.to_right = False
        self.window = window

    def set_movement(self, direction, is_pressed):
        if direction == "left":
            self.to_left = is_pressed
        if direction == "right":
            self.to_right = is_pressed

    def update(self):
        if self.to_left and self.x > 0:
            self.x -= 5
        if self.to_right and self.x < self.window.get_width() - self.image.get_width():
            self.x += 5

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    @property
    def get_position(self):
        return self.x, self.y