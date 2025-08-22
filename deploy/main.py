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
        self.score = 0
        self.health = 3
        self.total_coins = 100
        self.total_health = 3
        self.font = pygame.font.SysFont('Arial', 30)

    def load_images(self):
        self.images = {}
        for name in ["door", "coin", "robot", "monster"]:
            try:
                self.images[name] = pygame.image.load(f"assets/{name}.png")
            except FileNotFoundError:
                print(f"Error: Could not load image {name}.png")
                pygame.quit()
                exit()

    def step(self):
        """Run one frame of the game (safe for async loop)."""
        self.check_events()
        self.generate()
        self.update()
        self.draw_window()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
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
            elif event.type in (pygame.FINGERDOWN, pygame.MOUSEBUTTONDOWN):
                if event.type == pygame.FINGERDOWN:
                    x, y = event.x * self.window_width, event.y * self.window_height
                else:
                    x, y = pygame.mouse.get_pos()
                column_width = self.window_width // 3
                if x < column_width:
                    self.robot.set_movement("left", True)
                elif x > 2 * column_width:
                    self.robot.set_movement("right", True)
            elif event.type in (pygame.FINGERUP, pygame.MOUSEBUTTONUP):
                self.robot.set_movement("left", False)
                self.robot.set_movement("right", False)

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

    def update(self):
        self.spawn_coins.update()
        self.spawn_monsters.update()
        self.spawn_doors.update()
        self.robot.update()

        # Coin collisions
        for coin in self.coins[:]:
            coin.update()
            if self.robot.get_rect().colliderect(coin.get_rect()):
                self.coins.remove(coin)
                self.score += 1
                if self.score >= self.total_coins:
                    self.show_popup("You Win!")
            elif coin.y >= self.window_height:
                self.coins.remove(coin)
                self.health -= 1
                if self.health <= 0:
                    self.show_popup("Game Over!")

        # Monster collisions
        for monster in self.monsters[:]:
            monster.update()
            if self.robot.get_rect().colliderect(monster.get_rect()):
                self.monsters.remove(monster)
                self.health -= 1
                if self.health <= 0:
                    self.show_popup("Game Over!")
            elif monster.y > self.window_height:
                self.monsters.remove(monster)

        # Door collisions
        for door in self.doors[:]:
            door.update()
            if self.robot.get_rect().colliderect(door.get_rect()):
                self.doors.remove(door)
                self.health = min(self.total_health, self.health + 1)
            elif door.y > self.window_height:
                self.doors.remove(door)

    def draw_window(self):
        self.window.fill((230, 230, 230))
        self.draw_objects()

        coin_text = self.font.render(f"{self.score} / {self.total_coins}", True, (0, 0, 0))
        self.window.blit(self.images['coin'], (self.window.get_width() - 180, 19))
        self.window.blit(coin_text, (self.window_width - coin_text.get_width() - 20, 20))

        door_text = self.font.render(f"{self.health} / {self.total_health}", True, (0, 0, 0))
        self.window.blit(self.images['door'], (self.window.get_width() - 184, 65))
        self.window.blit(door_text, (self.window_width - door_text.get_width() - 37, 83))

        pygame.display.flip()

    def draw_objects(self):
        self.robot.draw(self.window)
        for coin in self.coins:
            coin.draw(self.window)
        for monster in self.monsters:
            monster.draw()
        for door in self.doors:
            door.draw()

    def show_popup(self, message):
        popup_font = pygame.font.SysFont('Arial', 50)
        button_font = pygame.font.SysFont('Arial', 30)

        popup_surface = pygame.Surface((600, 300))
        popup_surface.fill((200, 200, 200))
        popup_rect = popup_surface.get_rect(center=(self.window_width // 2, self.window_height // 2))

        text = popup_font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(300, 100))
        popup_surface.blit(text, text_rect)

        pygame.draw.rect(popup_surface, (100, 100, 100), (200, 180, 200, 60))
        button_text = button_font.render("Quit", True, (255, 255, 255))
        button_rect = button_text.get_rect(center=(300, 210))
        popup_surface.blit(button_text, button_rect)

        self.window.blit(popup_surface, popup_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if popup_rect.collidepoint(mouse_pos):
                        x, y = mouse_pos[0] - popup_rect.left, mouse_pos[1] - popup_rect.top
                        if 200 <= x <= 400 and 180 <= y <= 240:
                            waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                        waiting = False

        pygame.quit()
        exit()


async def main():
    game = RobotGame()
    clock = pygame.time.Clock()

    while True:
        game.step()
        clock.tick(30)
        await asyncio.sleep(0)  # yield to pygbag


if __name__ == "__main__":
    asyncio.run(main())
