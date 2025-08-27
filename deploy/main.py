import asyncio
import pygame

from robot import Robot
from spawn import CoinSpawn, MonsterSpawn, DoorSpawn


class RobotGame:
    def __init__(self):
        pygame.init()
        self.window_height = 1080
        self.window_width = 1920
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Robot Game")

        self.load_images()

        # Fonts
        self.font = pygame.font.SysFont('Arial', 30)
        self.big_font = pygame.font.SysFont('Arial', 60)

        # Game state: "menu", "playing", "gameover", "win"
        self.state = "menu"
        self.reset_game()

    def load_images(self):
        self.images = {}
        for name in ["door", "coin", "robot", "monster"]:
            try:
                self.images[name] = pygame.image.load(f"assets/{name}.png")
            except FileNotFoundError:
                print(f"Error: Could not load image {name}.png")
                pygame.quit()
                exit()

    def reset_game(self):
        """Reset everything for a new game."""
        self.robot = Robot(
            self.window_width // 2,
            self.window_height - self.images["robot"].get_height(),
            self.images["robot"],
            self.window
        )
        self.coins = []
        self.monsters = []
        self.doors = []
        self.spawn_coins = CoinSpawn()
        self.spawn_monsters = MonsterSpawn()
        self.spawn_doors = DoorSpawn()
        self.score = 49
        self.health = 3
        self.total_coins = 50
        self.total_health = 3

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if self.state == "playing":
                # normal gameplay events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.robot.set_movement("left", True)
                    if event.key == pygame.K_RIGHT:
                        self.robot.set_movement("right", True)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.robot.set_movement("left", False)
                    if event.key == pygame.K_RIGHT:
                        self.robot.set_movement("right", False)

            elif self.state in ("menu", "gameover", "win"):
                # Menu/GameOver/Win controls
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # start or restart
                        self.reset_game()
                        self.state = "playing"
                    elif event.key == pygame.K_ESCAPE:  # quit
                        pygame.quit()
                        exit()

    def step(self, dt):
        """Run one frame depending on game state."""
        self.check_events()

        if self.state == "playing":
            self.generate()
            self.update(dt)
            self.draw_window()
        elif self.state == "menu":
            self.draw_menu("menu", "Press ENTER to Play")
        elif self.state == "gameover":
            self.draw_menu("gameover", "Game Over - Press ENTER to Restart")
        elif self.state == "win":
            self.draw_menu("win", "You Win! - Press ENTER to Play Again")

    def generate(self):
        coin = self.spawn_coins.generate(self.window, self.images["coin"], robot=self.robot)
        if coin:
            self.coins.append(coin)

        monster = self.spawn_monsters.generate(self.window, self.images["monster"], robot=self.robot)
        if monster:
            self.monsters.append(monster)

        door = self.spawn_doors.generate(self.window, self.images["door"], robot=self.robot)
        if door:
            self.doors.append(door)

    def update(self, dt):
        self.spawn_coins.update()
        self.spawn_monsters.update()
        self.spawn_doors.update()
        self.robot.update(dt)

        # Coin collisions
        for coin in self.coins[:]:
            coin.update(dt)
            if self.robot.get_rect().colliderect(coin.get_rect()):
                self.coins.remove(coin)
                self.score += 1
                if self.score >= self.total_coins:
                    self.state = "win"
            elif coin.y >= self.window_height:
                self.coins.remove(coin)
                self.health -= 1
                if self.health <= 0:
                    self.state = "gameover"

        # Monster collisions
        for monster in self.monsters[:]:
            monster.update(dt)
            if self.robot.get_rect().colliderect(monster.get_rect()):
                self.monsters.remove(monster)
                self.health -= 1
                if self.health <= 0:
                    self.state = "gameover"
            elif monster.y > self.window_height:
                self.monsters.remove(monster)

        # Door collisions
        for door in self.doors[:]:
            door.update(dt)
            if self.robot.get_rect().colliderect(door.get_rect()):
                self.doors.remove(door)
                self.health = min(self.total_health, self.health + 1)
            elif door.y > self.window_height:
                self.doors.remove(door)

    def draw_window(self):
        self.window.fill((150, 150, 230))
        self.robot.draw(self.window)
        for coin in self.coins:
            coin.draw(self.window)
        for monster in self.monsters:
            monster.draw()
        for door in self.doors:
            door.draw()

        # UI
        coin_text = self.font.render(f"{self.score} / {self.total_coins}", True, (0, 0, 0))
        self.window.blit(self.images['coin'], (self.window.get_width() - 180, 19))
        self.window.blit(coin_text, (self.window_width - coin_text.get_width() - 20, 20))

        door_text = self.font.render(f"{self.health} / {self.total_health}", True, (0, 0, 0))
        self.window.blit(self.images['door'], (self.window.get_width() - 177, 75))
        self.window.blit(door_text, (self.window_width - door_text.get_width() - 37, 83))

        pygame.display.flip()

    def draw_menu(self, result, message):
        """Draw menu or gameover/win screen."""
        if result == "win":
            self.window.fill((50, 200, 50))
        elif result == "gameover":
            self.window.fill((200, 50, 50))
        else:
            self.window.fill((50, 50, 200))
        text = self.big_font.render(message, True, (255, 255, 255))
        rect = text.get_rect(center=(self.window_width//2, self.window_height//2))
        self.window.blit(text, rect)
        pygame.display.flip()


async def main():
    game = RobotGame()
    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60) / 1000  # delta time in seconds
        game.step(dt)
        await asyncio.sleep(0)  # yield to pygbag


if __name__ == "__main__":
    asyncio.run(main())
