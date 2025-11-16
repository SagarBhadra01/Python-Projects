import random
import sys
import os
import time

try:
    import pygame
    from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_p
except Exception:
    print("pygame is required. Install with: python -m pip install -r requirements.txt")
    raise

# Game configuration
TILE = 20
GRID_WIDTH = 32
GRID_HEIGHT = 24
WIDTH = TILE * GRID_WIDTH
HEIGHT = TILE * GRID_HEIGHT
# High score file saved in the game's directory, not outside
HIGH_SCORE_FILE = os.path.join(os.path.dirname(__file__), "snake_game.highscore")

# Colors - Clean Minimalist Theme
BG_DARK = (20, 20, 30)          # Very dark background
WHITE = (255, 255, 255)
GREEN = (100, 255, 100)         # Bright lime green
DARK_GREEN = (70, 180, 70)      # Dark green
RED = (255, 100, 100)           # Bright red
BLUE = (120, 200, 255)          # Bright cyan
GRAY = (100, 110, 130)          # Neutral gray
YELLOW = (255, 240, 80)         # Warm yellow
ORANGE = (255, 140, 80)         # Warm orange

# Difficulty levels
DIFFICULTY = {
    "EASY": 8,
    "NORMAL": 10,
    "HARD": 14
}


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        mid_x = GRID_WIDTH // 2
        mid_y = GRID_HEIGHT // 2
        self.body = [(mid_x, mid_y), (mid_x - 1, mid_y), (mid_x - 2, mid_y)]
        self.direction = (1, 0)  # moving right
        self.next_direction = (1, 0)  # Queue next direction to prevent input lag
        self.grow_pending = 0

    def head(self):
        return self.body[0]

    def set_direction(self, d):
        """Queue direction change to prevent reversals"""
        if (d[0] * -1, d[1] * -1) != self.direction:
            self.next_direction = d

    def move(self):
        """Move snake and apply queued direction"""
        self.direction = self.next_direction
        hx, hy = self.head()
        dx, dy = self.direction
        new_head = (hx + dx, hy + dy)
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
                # Head
                pygame.draw.rect(surface, BLUE, rect)
                pygame.draw.rect(surface, WHITE, rect, 2)
            else:
                # Body
                pygame.draw.rect(surface, GREEN, rect)
                pygame.draw.rect(surface, DARK_GREEN, rect, 1)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.SysFont(None, 24)
        self.font_medium = pygame.font.SysFont(None, 36)
        self.font_large = pygame.font.SysFont(None, 64)
        
        # Game state
        self.state = "MENU"
        self.difficulty = "NORMAL"
        self.snake = Snake()
        self.food = None
        
        # Game stats
        self.score = 0
        self.high_score = self.load_high_score()
        self.foods_eaten = 0
        self.start_time = None
        
        # Game flags
        self.paused = False
        self.base_speed = DIFFICULTY["NORMAL"]
        self.background = self.create_background()

    def create_background(self):
        """Create a simple, clean, and minimalist gaming background"""
        bg = pygame.Surface((WIDTH, HEIGHT))
        
        # Solid dark background - clean and simple
        bg.fill(BG_DARK)
        
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
        occupied = set(self.snake.body)
        free = set((x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)) - occupied
        if not free:
            return None
        return random.choice(list(free))

    def run(self):
        while True:
            if self.state == "MENU":
                self.run_menu_screen()
            elif self.state == "DIFFICULTY":
                self.run_difficulty_screen()
            elif self.state == "PLAYING":
                self.run_game()
            elif self.state == "GAME_OVER":
                self.run_game_over_screen()

    def run_menu_screen(self):
        """Main menu with game title and options"""
        self.screen.blit(self.background, (0, 0))
        self.draw_text_center("Snake Game", self.font_large, WHITE, y_offset=-80)
        self.draw_text_center("Use Arrow Keys to Move", self.font_small, WHITE, y_offset=10)
        self.draw_text_center("Eat food to grow and score points", self.font_small, WHITE, y_offset=40)
        self.draw_text_center("Avoid walls and yourself to survive", self.font_small, WHITE, y_offset=60)
        self.draw_text_center("Press S for START or Esc to quit", self.font_medium, YELLOW, y_offset=100)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN and event.key == pygame.K_s:
                self.state = "DIFFICULTY"

    def run_difficulty_screen(self):
        """Difficulty selection screen"""
        difficulties = ["EASY", "NORMAL", "HARD"]
        idx = difficulties.index(self.difficulty)
        
        self.screen.blit(self.background, (0, 0))
        self.draw_text_center("Select Difficulty", self.font_large, WHITE, y_offset=-80)
        
        for i, diff in enumerate(difficulties):
            color = YELLOW if i == idx else WHITE
            text = f">>> {diff} <<<" if i == idx else diff
            y = -20 + (i * 50)
            self.draw_text_center(text, self.font_medium, color, y_offset=y)
        
        self.draw_text_center("Use UP/DOWN arrows, Press Enter to select", self.font_small, WHITE, y_offset=100)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    idx = (idx - 1) % len(difficulties)
                    self.difficulty = difficulties[idx]
                elif event.key == K_DOWN:
                    idx = (idx + 1) % len(difficulties)
                    self.difficulty = difficulties[idx]
                elif event.key == pygame.K_RETURN:
                    self.reset_game()
                elif event.key == K_ESCAPE:
                    self.state = "MENU"

    def reset_game(self):
        """Initialize new game with selected difficulty"""
        self.base_speed = DIFFICULTY[self.difficulty]
        self.snake.reset()
        self.food = self.spawn_food()
        self.score = 0
        self.foods_eaten = 0
        self.start_time = time.time()
        self.state = "PLAYING"

    def run_game_over_screen(self):
        """Game over screen with stats"""
        self.save_high_score()
        elapsed_time = int(time.time() - self.start_time) if self.start_time else 0
        
        self.screen.blit(self.background, (0, 0))
        self.draw_text_center("Game Over", self.font_large, RED, y_offset=-100)
        self.draw_text_center(f"Score: {self.score}", self.font_medium, WHITE, y_offset=-20)
        self.draw_text_center(f"High Score: {self.high_score}", self.font_medium, YELLOW, y_offset=20)
        self.draw_text_center(f"Foods Eaten: {self.foods_eaten} | Time: {elapsed_time}s", self.font_small, WHITE, y_offset=70)
        self.draw_text_center("Press R to restart or Esc to menu", self.font_small, WHITE, y_offset=110)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.state = "MENU"
                elif event.key == pygame.K_r:
                    self.reset_game()

    def run_game(self):
        """Main game loop"""
        self.handle_input()
        if not self.paused:
            self.update()
        self.draw()
        self.clock.tick(self.get_current_speed())

    def handle_input(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.state = "MENU"
                elif event.key == K_p:
                    self.paused = not self.paused
                elif not self.paused:
                    # Handle snake movement
                    if event.key == K_UP:
                        self.snake.set_direction((0, -1))
                    elif event.key == K_DOWN:
                        self.snake.set_direction((0, 1))
                    elif event.key == K_LEFT:
                        self.snake.set_direction((-1, 0))
                    elif event.key == K_RIGHT:
                        self.snake.set_direction((1, 0))

    def update(self):
        """Update game logic"""
        self.snake.move()

        # Check wall collision
        hx, hy = self.snake.head()
        if not (0 <= hx < GRID_WIDTH and 0 <= hy < GRID_HEIGHT):
            self.state = "GAME_OVER"
            return

        # Check self collision
        if self.snake.collides_with_self():
            self.state = "GAME_OVER"
            return

        # Check food collision
        if self.food and self.snake.head() == self.food:
            self.score += 1
            self.foods_eaten += 1
            self.snake.grow()
            self.food = self.spawn_food()

    def get_current_speed(self):
        """Calculate current game speed based on difficulty and foods eaten"""
        speed = self.base_speed + (self.foods_eaten // 5)
        return min(speed, 20)  # Cap at 20 FPS

    def draw(self):
        """Render game screen"""
        self.screen.blit(self.background, (0, 0))
        self.draw_grid()
        self.snake.draw(self.screen)

        # Draw food
        if self.food:
            rect = pygame.Rect(self.food[0] * TILE, self.food[1] * TILE, TILE, TILE)
            pygame.draw.rect(self.screen, RED, rect)

        # Draw HUD
        score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (8, 8))
        
        highscore_text = self.font_small.render(f"High: {self.high_score}", True, YELLOW)
        self.screen.blit(highscore_text, (WIDTH - highscore_text.get_width() - 8, 8))
        
        diff_text = self.font_small.render(f"Difficulty: {self.difficulty}", True, ORANGE)
        self.screen.blit(diff_text, (8, HEIGHT - 30))
        
        speed_text = self.font_small.render(f"Speed: {self.get_current_speed()}", True, ORANGE)
        self.screen.blit(speed_text, (WIDTH - speed_text.get_width() - 8, HEIGHT - 30))

        # Pause indicator
        if self.paused:
            self.draw_text_center("PAUSED", self.font_large, YELLOW)

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
