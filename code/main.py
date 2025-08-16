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



        pygame.display.flip()

if __name__ == "__main__":
    RobotGame()