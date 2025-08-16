#!/usr/bin/env python3
import pygame

class RobotGame:
    def __init__(self):
        pygame.init()
        
        self.load_images()
        
        self.height = 1080
        self.width = 1920
        self.scale = 1

        window_height = self.scale * self.height
        window_width = self.scale * self.width
        self.window = pygame.display.set_mode((window_width, window_height))

        pygame.display.set_caption("Robot Game")

        self.main_loop()

    def load_images(self):
        self.images = []
        for name in ["door", "coin", "robot", "monster"]:
            self.images.append(pygame.image.load("assets/" + name + ".png"))

    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def draw_window(self):
        self.window.fill((230, 230, 230))
        self.draw_objects()
        pygame.display.flip()

    def draw_objects(self):
        self.robot = Robot(200, 200)
        self.robot.draw(self.window)

        self.coin = Coin(300, 300)
        self.coin.draw(self.window)

        self.monster = Monster(400, 400)
        self.monster.draw(self.window)

        self.door = Door(500, 500)
        self.door.draw(self.window)

class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/robot.png")

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/coin.png")

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/monster.png")

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

class Door:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/door.png")

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

if __name__ == "__main__":
    RobotGame()