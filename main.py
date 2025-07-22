from random import randint
import asyncio
import pygame

class Asteroid:
    def __init__(self):
        self.image = pygame.image.load("assets/rock.png")
        self.x = randint(0, 640 - self.image.get_width())
        self.y = randint(-1000, 0)
        self.velocity_x = 0
        self.velocity_y = 2
        self.active = True

    def update(self):
        if not self.active:
            return
        self.y += self.velocity_y
        self.x += self.velocity_x

        if self.x < -self.image.get_width() or self.x > 640:
            self.active = False

    def draw(self, window):
        if self.active:
            window.blit(self.image, (self.x, self.y))

def control_robot(robot, to_left, to_right, x):
    if to_right and x < 640 - robot.get_width():
        x += 2
    if to_left and x > 0:
        x -= 2
    return x

def display_content(window, robot, asteroids, x, y, points):
    background_color = (50, 200, 100)
    window.fill(background_color)
    window.blit(robot, (x, y))
    for asteroid in asteroids:
        asteroid.update()
        asteroid.draw(window)

    pygame.draw.rect(window, (50, 150, 50), (500, 0, 140, 50))
    pygame.draw.rect(window, (50, 100, 50), (500, 0, 140, 50), 4)
    game_font = pygame.font.SysFont("Arial", 24)
    text = game_font.render(f"Points: {points}", True, (250, 250, 250))
    window.blit(text, (520, 10))

    pygame.display.flip()

def show_game_over(window, points, play_again_rect):
    window.fill((0, 0, 0))
    font_big = pygame.font.SysFont("Arial", 48)
    font_small = pygame.font.SysFont("Arial", 30)
    text_game_over = font_big.render("GAME OVER", True, (255, 0, 0))
    text_points = font_small.render(f"Final Points: {points}", True, (255, 255, 255))
    text_restart = font_small.render("Press ESC to Quit", True, (255, 255, 255))
    text_play_again = font_small.render("Play Again", True, (0, 0, 0))

    window.blit(text_game_over, (640//2 - text_game_over.get_width()//2, 150))
    window.blit(text_points, (640//2 - text_points.get_width()//2, 220))
    window.blit(text_restart, (640//2 - text_restart.get_width()//2, 260))

    # Draw play again button
    pygame.draw.rect(window, (100, 200, 100), play_again_rect)
    pygame.draw.rect(window, (0, 100, 0), play_again_rect, 3)
    # Center the text on the button
    text_play_again_pos = text_play_again.get_rect(center=play_again_rect.center)
    window.blit(text_play_again, text_play_again_pos)

    pygame.display.flip()

def handle_events(to_left, to_right):
    quit_game = False
    mouse_clicked = False
    mouse_pos = (0, 0)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_left = True
            if event.key == pygame.K_RIGHT:
                to_right = True
            if event.key == pygame.K_ESCAPE:
                quit_game = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_left = False
            if event.key == pygame.K_RIGHT:
                to_right = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_clicked = True
            mouse_pos = event.pos
        if event.type == pygame.QUIT:
            quit_game = True
    return to_left, to_right, quit_game, mouse_clicked, mouse_pos

def initiate_window():
    window = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Asteroids Game")
    return window

def initiate_robot(window):
    robot = pygame.image.load("assets/robot.png")
    x = window.get_width() / 2 - robot.get_width() / 2
    y = window.get_height() - robot.get_height()
    return robot, x, y, False, False

def initiate_asteroids(num=10):
    return [Asteroid() for _ in range(num)]

async def main():
    pygame.init()
    window = initiate_window()
    robot, x, y, to_right, to_left = initiate_robot(window)
    asteroids = initiate_asteroids()
    clock = pygame.time.Clock()
    points = 0
    game_over = False

    # Define play again button rectangle
    play_again_rect = pygame.Rect(640//2 - 75, 320, 150, 50)

    while True:
        if not game_over:
            to_left, to_right, quit_game, _, _ = handle_events(to_left, to_right)
            if quit_game:
                break
            x = control_robot(robot, to_left, to_right, x)

            robot_rect = robot.get_rect(topleft=(x, y))

            # Check collision & missed asteroids
            for asteroid in asteroids:
                if asteroid.active:
                    asteroid_rect = asteroid.image.get_rect(topleft=(asteroid.x, asteroid.y))
                    if asteroid.y > 480:
                        game_over = True
                    if robot_rect.colliderect(asteroid_rect):
                        asteroid.active = False
                        points += 1

            display_content(window, robot, asteroids, x, y, points)

        else:
            # Game is frozen, show game over screen and wait for ESC to quit or Play Again click
            to_left, to_right, quit_game, mouse_clicked, mouse_pos = handle_events(to_left, to_right)
            show_game_over(window, points, play_again_rect)

            if quit_game:
                break

            # Check if Play Again button clicked
            if mouse_clicked and play_again_rect.collidepoint(mouse_pos):
                # Restart game
                robot, x, y, to_right, to_left = initiate_robot(window)
                asteroids = initiate_asteroids()
                points = 0
                game_over = False

        clock.tick(60)

    pygame.quit()

asyncio.run(main())
