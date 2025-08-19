import asyncio
import pygame

class RobotGame:
    def __init__(self):
        pygame.init()

        screen_height = 1080
        screen_width = 1920
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        pygame.display.set_caption("Robot Game")

    def draw_screen(self):
        self.screen.fill((230, 230,  230))

        pygame.display.flip()

async def main():
    game = RobotGame()
    clock = pygame.time.Clock()

    while True:
        game.draw_screen()
        clock.tick(30)
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
