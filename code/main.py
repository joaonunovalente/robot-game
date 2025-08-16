#!/usr/bin/env python3
import pygame

from coin import Coin
from door import Door
from monster import Monster
from robot import Robot
from spawn import Spawn

class RobotGame:
    def __init__(self):
        pygame.init()
        self.window_height = 1080
        self.window_width = 1920
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Robot Game")

        self.load_images()

        # Initialize objects and pass the loaded images
        self.robot = Robot(self.window_width // 2, self.window_height - self.images["robot"].get_height(), self.images["robot"], self.window)
        self.coins = []

        # Spawn management
        self.spawn_counter = 0
        self.spawn_interval = 500
        self.counter = 0
        self.spawn_position = 0

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
            self.generate_coins()
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
                    x, y = event.x * self.window_width, event.y * self.window_height
                else:
                    x, y = pygame.mouse.get_pos()
                # Split the screen into three vertical columns
                column_width = self.window_width // 3
                if x < column_width:  # Left column
                    self.robot.set_movement("left", True)
                elif x > 2 * column_width:  # Right column
                    self.robot.set_movement("right", True)

            elif event.type == pygame.FINGERUP or event.type == pygame.MOUSEBUTTONUP:
                # Stop movement when finger/mouse is released
                self.robot.set_movement("left", False)
                self.robot.set_movement("right", False)

    def update(self):
        self.robot.update()
        self.coins = [coin for coin in self.coins if coin.y + coin.image.get_height() < self.window_height]
        for coin in self.coins:
            coin.update()

    def draw_window(self):
        self.window.fill((230, 230, 230))
        self.draw_objects()
        pygame.display.flip()

    def draw_objects(self):
        self.robot.draw(self.window)
        for coin in self.coins:
            coin.draw(self.window)

    def generate_coins(self):
        self.spawn_counter += 1

        if self.spawn_counter >= self.spawn_interval:
            # Gradually decrease spawn interval, with a reasonable minimum
            self.spawn_interval = max(30, self.spawn_interval - 5)
            self.spawn_counter = 0

            # Use robot's position to influence spawn, but keep it controlled
            robot_x = self.robot.get_position[0]  # Access as a property (no parentheses)
            # Spawn coins at a fixed offset from the robot's position
            self.spawn_position = (self.spawn_position + robot_x + 250) % self.window.get_width() - self.images["coin"].get_width()

            self.coins.append(Coin(self.spawn_position, 0, self.images["coin"], self.window))

if __name__ == "__main__":
    RobotGame()
