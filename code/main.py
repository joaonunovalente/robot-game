#!/usr/bin/env python3
import pygame

from coin import Coin
from door import Door
from monster import Monster
from robot import Robot

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

        # Initialize objects and pass the loaded images
        self.robot = Robot(self.width // 2, self.height - self.images["robot"].get_height(), self.images["robot"])
        self.coin = Coin(300, 300, self.images["coin"])
        self.monster = Monster(400, 400, self.images["monster"])
        self.door = Door(500, 500, self.images["door"])
        self.main_loop()

    def load_images(self):
        self.images = {}
        for name in ["door", "coin", "robot", "monster"]:
            try:
                self.images[name] = pygame.image.load("assets/" + name + ".png")
            except FileNotFoundError:
                print(f"Error: Could not load image {name}.png")
                pygame.quit()
                exit()

    def main_loop(self):
        while True:
            self.check_events()
            self.update()
            self.draw_window()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            # Keyboard controls
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.robot.set_movement("left", True)
                if event.key == pygame.K_RIGHT:
                    self.robot.set_movement("right", True)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.robot.set_movement("left", False)
                if event.key == pygame.K_RIGHT:
                    self.robot.set_movement("right", False)
            # Touch/mobile controls
            elif event.type == pygame.FINGERDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the touch/click
                if event.type == pygame.FINGERDOWN:
                    x, y = event.x * self.width, event.y * self.height
                else:
                    x, y = pygame.mouse.get_pos()

                # Split the screen into three vertical columns
                column_width = self.width // 3
                if x < column_width:  # Left column
                    self.robot.set_movement("left", True)
                elif x > 2 * column_width:  # Right column
                    self.robot.set_movement("right", True)
            elif event.type == pygame.FINGERUP or event.type == pygame.MOUSEBUTTONUP:
                # Stop movement when finger/mouse is released
                self.robot.set_movement("left", False)
                self.robot.set_movement("right", False)

    def update(self):
        self.robot.update(self.width)

    def draw_window(self):
        self.window.fill((230, 230, 230))
        self.draw_objects()
        pygame.display.flip()

    def draw_objects(self):
        self.robot.draw(self.window)
        self.coin.draw(self.window)
        self.monster.draw(self.window)
        self.door.draw(self.window)

if __name__ == "__main__":
    RobotGame()
