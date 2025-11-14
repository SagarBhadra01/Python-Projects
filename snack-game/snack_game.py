import random
import sys
import os
import time

try:
    import pygame
    from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_r, K_p
except Exception:
    print("pygame is required. Install with: python -m pip install -r requirements.txt")
    raise


# Game configuration
TILE = 20
GRID_WIDTH = 32
GRID_HEIGHT = 24
WIDTH = TILE * GRID_WIDTH
HEIGHT = TILE * GRID_HEIGHT
FPS = 10
HIGH_SCORE_FILE = "snack_game.highscore"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 170, 0)
DARK_GREEN = (0, 140, 0)
RED = (200, 0, 0)
BLUE = (0, 120, 255)
GRAY = (40, 40, 40)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
BG_GREEN_1 = (20, 80, 20)
BG_GREEN_2 = (15, 70, 15)


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        mid_x = GRID_WIDTH // 2
        mid_y = GRID_HEIGHT // 2
        self.body = [(mid_x, mid_y), (mid_x - 1, mid_y), (mid_x - 2, mid_y)]
        self.direction = (1, 0)  # moving right
        self.grow_pending = 0

    def head(self):
        return self.body[0]

    def set_direction(self, d):
        if (d[0] * -1, d[1] * -1) == self.direction:
            return
        self.direction = d

    def move(self):
        hx, hy = self.head()
        dx, dy = self.direction
        new_head = ((hx + dx) % GRID_WIDTH, (hy + dy) % GRID_HEIGHT) # Wrap around screen
        self.body.insert(0, new_head)
        if self.grow_pending:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        self.grow_pending += amount

    def collides_with_self(self):
        return self.head() in self.body[1:]

    def draw(self, surface):
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * TILE, y * TILE, TILE, TILE)
            if i == 0:
                pygame.draw.rect(surface, BLUE, rect)
                # Eye
                eye_rect = pygame.Rect(x * TILE + TILE // 2, y * TILE + TILE // 4, TILE // 4, TILE // 4)
                pygame.draw.rect(surface, WHITE, eye_rect)
            else:
                pygame.draw.rect(surface, GREEN, rect)
                pygame.draw.rect(surface, DARK_GREEN, rect, 1)


class PowerUp:
    def __init__(self, pos):
        self.pos = pos
        self.type = 'bonus_points'
        self.color = GOLD
        self.spawn_time = time.time()
        self.duration = 5 # seconds

    def draw(self, surface):
        rect = pygame.Rect(self.pos[0] * TILE, self.pos[1] * TILE, TILE, TILE)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, YELLOW, rect, 2)

    def is_expired(self):
        return time.time() - self.spawn_time > self.duration


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snack Game")
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.SysFont(None, 24)
        self.font_medium = pygame.font.SysFont(None, 36)
        self.font_large = pygame.font.SysFont(None, 64)
        self.state = "START"
        self.snake = Snake()
        self.food = None
        self.powerups = []
        self.powerup_spawn_timer = 0
        self.score = 0
        self.high_score = self.load_high_score()
        self.paused = False
        self.speed = FPS
        self.background = self.create_background()

    def create_background(self):
        bg = pygame.Surface((WIDTH, HEIGHT))
        bg.fill(BG_GREEN_1)
        for i in range(100):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.randint(2, 5)
            pygame.draw.circle(bg, BG_GREEN_2, (x, y), size)
        return bg

    def load_high_score(self):
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, "r") as f:
                    return int(f.read())
            except (IOError, ValueError):
                return 0
        return 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                with open(HIGH_SCORE_FILE, "w") as f:
                    f.write(str(self.high_score))
            except IOError:
                print("Warning: Could not save high score.")

    def spawn_food(self):
        occupied = set(self.snake.body) | set(p.pos for p in self.powerups)
        free = set((x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)) - occupied
        if not free:
            return None
        return random.choice(list(free))

    def spawn_powerup(self):
        occupied = set(self.snake.body) | set(p.pos for p in self.powerups)
        if self.food:
            occupied.add(self.food)
        free = set((x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)) - occupied
        if not free:
            return
        pos = random.choice(list(free))
        self.powerups.append(PowerUp(pos))
        self.powerup_spawn_timer = random.randint(5, 15) # Reset timer

    def reset_game(self):
        self.snake.reset()
        self.food = self.spawn_food()
        self.powerups = []
        self.powerup_spawn_timer = random.randint(5, 10)
        self.score = 0
        self.speed = FPS
        self.state = "PLAYING"

    def run(self):
        while True:
            if self.state == "START":
                self.run_start_screen()
            elif self.state == "PLAYING":
                self.run_game()
            elif self.state == "GAME_OVER":
                self.run_game_over_screen()

    def run_start_screen(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_text_center("Snack Game", self.font_large, WHITE, y_offset=-60)
        self.draw_text_center("Use Arrow Keys to Move", self.font_medium, WHITE, y_offset=20)
        self.draw_text_center("Press any key to start", self.font_small, YELLOW, y_offset=70)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                self.reset_game()

    def run_game_over_screen(self):
        self.save_high_score()
        self.screen.blit(self.background, (0, 0))
        self.draw_text_center("Game Over", self.font_large, RED, y_offset=-60)
        self.draw_text_center(f"Score: {self.score}", self.font_medium, WHITE, y_offset=10)
        self.draw_text_center(f"High Score: {self.high_score}", self.font_medium, YELLOW, y_offset=50)
        self.draw_text_center("Press R to restart or Esc to quit", self.font_small, WHITE, y_offset=100)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN and event.key == K_r:
                self.state = "START"

    def run_game(self):
        self.handle_input()
        if not self.paused:
            self.update()
        self.draw()
        self.clock.tick(self.speed)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.state = "START"
                elif event.key == K_p:
                    self.paused = not self.paused
                elif not self.paused:
                    if event.key == K_UP:
                        self.snake.set_direction((0, -1))
                    elif event.key == K_DOWN:
                        self.snake.set_direction((0, 1))
                    elif event.key == K_LEFT:
                        self.snake.set_direction((-1, 0))
                    elif event.key == K_RIGHT:
                        self.snake.set_direction((1, 0))

    def update(self):
        self.snake.move()
        # Check self collision
        if self.snake.collides_with_self():
            self.state = "GAME_OVER"
        # Check food
        if self.food and self.snake.head() == self.food:
            self.score += 1
            self.snake.grow()
            self.food = self.spawn_food()
            # Increase speed
            if self.score % 5 == 0:
                self.speed += 1
        
        # Power-ups
        self.powerup_spawn_timer -= 1 / self.speed
        if self.powerup_spawn_timer <= 0:
            self.spawn_powerup()

        head = self.snake.head()
        for powerup in self.powerups[:]:
            if powerup.is_expired():
                self.powerups.remove(powerup)
                continue
            if head == powerup.pos:
                if powerup.type == 'bonus_points':
                    self.score += 5
                self.powerups.remove(powerup)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_grid()
        self.snake.draw(self.screen)
        
        for powerup in self.powerups:
            powerup.draw(self.screen)

        if self.food:
            rect = pygame.Rect(self.food[0] * TILE, self.food[1] * TILE, TILE, TILE)
            pygame.draw.rect(self.screen, RED, rect)

        # HUD
        score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (8, 8))
        highscore_text = self.font_small.render(f"High Score: {self.high_score}", True, YELLOW)
        self.screen.blit(highscore_text, (WIDTH - highscore_text.get_width() - 8, 8))

        if self.paused:
            self.draw_text_center("Paused", self.font_large, YELLOW)

        pygame.display.flip()

    def draw_grid(self):
        for x in range(0, WIDTH, TILE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WIDTH, y))

    def draw_text_center(self, text, font, color, y_offset=0):
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
        self.screen.blit(surf, rect)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
