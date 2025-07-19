import asyncio
import pygame

pygame.init()
window_width = 640
window_height = 480
window = pygame.display.set_mode((window_width, window_height))
window.fill((0, 0, 0))

robot = pygame.image.load("assets/robot.png")
robot_width = robot.get_width()
robot_height = robot.get_height()

window.blit(robot, (window_width / 2 - robot_width, window_height / 2 - robot_height))

pygame.display.flip()

async def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

asyncio.run(main())