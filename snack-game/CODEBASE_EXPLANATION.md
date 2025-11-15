# 🐍 Snack Game - Complete Code Walkthrough (Line by Line A-Z)

This document explains every line of code in `snack_game.py` in detail, from start to finish.

---

## 📌 Section 1: Imports (Lines 1-11)

### Lines 1-4: Standard Library Imports
```python
import random
import sys
import os
import time
```

| Import | Purpose | Usage |
|--------|---------|-------|
| `random` | Generate random numbers | Random food spawning on the game grid |
| `sys` | System-specific functions | Exit the game cleanly with `sys.exit()` |
| `os` | Operating system interface | Check if high score file exists, build file paths |
| `time` | Time-related functions | Track game duration, measure elapsed time |

---

### Lines 6-11: Pygame Import with Error Handling
```python
try:
    import pygame
    from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_p
except Exception:
    print("pygame is required. Install with: python -m pip install -r requirements.txt")
    raise
```

**What this does:**
- **Line 7**: Imports the main pygame library for game graphics and events
- **Line 8**: Imports specific constants from pygame.locals:
  - `QUIT` - Window close event
  - `KEYDOWN` - Keyboard press event
  - `K_UP`, `K_DOWN`, `K_LEFT`, `K_RIGHT` - Arrow key constants
  - `K_ESCAPE` - Escape key constant
  - `K_p` - P key for pause/unpause
- **Lines 9-11**: If pygame is not installed, display helpful message and exit
- **Why try/except?** Catches missing pygame before the game tries to use it

---

## 📌 Section 2: Game Configuration (Lines 14-22)

### Lines 14-19: Screen and Grid Dimensions
```python
TILE = 20
GRID_WIDTH = 32
GRID_HEIGHT = 24
WIDTH = TILE * GRID_WIDTH
HEIGHT = TILE * GRID_HEIGHT
```

**What this does:**
- `TILE = 20` → Each grid square is 20×20 pixels
- `GRID_WIDTH = 32` → 32 tiles horizontally
- `GRID_HEIGHT = 24` → 24 tiles vertically
- `WIDTH = 20 × 32 = 640` pixels (total window width)
- `HEIGHT = 20 × 24 = 480` pixels (total window height)

**Result:** 640×480 window with 32×24 game grid

---

### Line 21: High Score File Path
```python
HIGH_SCORE_FILE = os.path.join(os.path.dirname(__file__), "snack_game.highscore")
```

**Breakdown:**
- `__file__` = Path to current Python script
- `os.path.dirname(__file__)` = Directory containing the script
- `os.path.join(...)` = Combine path with filename
- **Result:** High score file saved in same folder as snack_game.py (not outside)
- **Example:** `C:\...\snack-game\snack_game.highscore`

---

## 📌 Section 3: Color Constants (Lines 24-32)

```python
BG_DARK = (20, 20, 30)          # Very dark background
WHITE = (255, 255, 255)
GREEN = (100, 255, 100)         # Bright lime green
DARK_GREEN = (70, 180, 70)      # Dark green
RED = (255, 100, 100)           # Bright red
BLUE = (120, 200, 255)          # Bright cyan
GRAY = (100, 110, 130)          # Neutral gray
YELLOW = (255, 240, 80)         # Warm yellow
ORANGE = (255, 140, 80)         # Warm orange
```

**What this is:**
- RGB tuples (Red, Green, Blue) where each value is 0-255
- **BG_DARK**: Almost black - used as game background
- **WHITE**: Pure white - used for text and borders
- **GREEN**: Bright green - snake body color
- **DARK_GREEN**: Darker green - snake body border
- **RED**: Bright red - food color
- **BLUE**: Cyan blue - snake head color
- **GRAY**: Neutral gray - grid lines
- **YELLOW**: Warm yellow - highlights and high score
- **ORANGE**: Warm orange - difficulty/speed indicators

---

## 📌 Section 4: Difficulty Dictionary (Lines 35-38)

```python
DIFFICULTY = {
    "EASY": 8,
    "NORMAL": 10,
    "HARD": 14
}
```

**What this does:**
- Maps difficulty names to base game speed (frames per second)
- `EASY`: 8 FPS (slowest, easiest to control)
- `NORMAL`: 10 FPS (moderate speed)
- `HARD`: 14 FPS (fastest, hardest to control)
- Speed increases further as player eats more food

---

## 📌 Section 5: Snake Class (Lines 41-89)

### Lines 41-42: Snake Class Constructor
```python
class Snake:
    def __init__(self):
        self.reset()
```

**What this does:**
- `class Snake:` Creates a new class for snake entity
- `__init__` is the constructor (runs when Snake object is created)
- `self.reset()` Initializes snake by calling reset method

---

### Lines 44-50: Reset Method
```python
def reset(self):
    mid_x = GRID_WIDTH // 2
    mid_y = GRID_HEIGHT // 2
    self.body = [(mid_x, mid_y), (mid_x - 1, mid_y), (mid_x - 2, mid_y)]
    self.direction = (1, 0)  # moving right
    self.next_direction = (1, 0)  # Queue next direction to prevent input lag
    self.grow_pending = 0
```

**Line by line:**
- `mid_x = 32 // 2 = 16` and `mid_y = 24 // 2 = 12` (center of grid)
- `self.body = [(16,12), (15,12), (13,12)]` - Snake starts as 3 segments
  - Head at center: (16, 12)
  - Body segments moving left: (15, 12), (14, 12)
- `self.direction = (1, 0)` - Currently moving right (dx=1, dy=0)
- `self.next_direction = (1, 0)` - Next direction queued (allows smooth input)
- `self.grow_pending = 0` - No pending growth

---

### Lines 52-53: Head Method
```python
def head(self):
    return self.body[0]
```

**What this does:**
- Returns the first segment of snake body (the head)
- `self.body[0]` is always the head position
- Example: If body is [(16,12), (15,12), (14,12)], returns (16,12)

---

### Lines 55-59: Set Direction Method
```python
def set_direction(self, d):
    """Queue direction change to prevent reversals"""
    if (d[0] * -1, d[1] * -1) != self.direction:
        self.next_direction = d
```

**What this does:**
- Takes new direction `d` as parameter (tuple like (1,0))
- `(d[0] * -1, d[1] * -1)` calculates opposite direction
  - If d = (1, 0) → opposite = (-1, 0)
- **Check:** Only allow direction if it's NOT exactly opposite
  - Prevents snake from reversing into itself
- If valid, queue direction in `self.next_direction`
- **Why queue?** Smooth input handling - capture multiple key presses per frame

---

### Lines 61-70: Move Method
```python
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
```

**Line by line:**
- `self.direction = self.next_direction` - Apply queued direction change
- `hx, hy = self.head()` - Get current head position
- `dx, dy = self.direction` - Get direction components
- `new_head = (hx + dx, hy + dy)` - Calculate new head position
  - Example: Head (16,12) moving right (1,0) → new (17,12)
- `self.body.insert(0, new_head)` - Add new head to front of body
- **Growth logic:**
  - If `self.grow_pending > 0`: Decrement (don't remove tail, snake grows)
  - Else: Remove last segment (snake moves, no growth)

---

### Lines 72-73: Grow Method
```python
def grow(self, amount=1):
    self.grow_pending += amount
```

**What this does:**
- Called when snake eats food
- Increases `grow_pending` counter
- Next `amount` moves will not remove tail (snake grows)

---

### Lines 75-76: Self Collision Check
```python
def collides_with_self(self):
    return self.head() in self.body[1:]
```

**What this does:**
- Checks if snake head collides with its own body
- `self.body[1:]` is all body segments except the head
- Returns `True` if head position is in body (collision detected)
- Returns `False` if head is safe

---

### Lines 78-89: Draw Method
```python
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
```

**Line by line:**
- `for i, (x, y) in enumerate(self.body):` Loop through each segment with index
- `rect = pygame.Rect(x * TILE, y * TILE, TILE, TILE)` Create rectangle
  - Grid position (x, y) converted to pixels (* TILE)
  - Size is TILE×TILE
- **If i == 0 (Head):**
  - `pygame.draw.rect(surface, BLUE, rect)` Fill with cyan blue
  - `pygame.draw.rect(surface, WHITE, rect, 2)` Draw white border (thickness 2)
- **Else (Body segments):**
  - `pygame.draw.rect(surface, GREEN, rect)` Fill with bright green
  - `pygame.draw.rect(surface, DARK_GREEN, rect, 1)` Draw dark green border

---

## 📌 Section 6: Game Class (Lines 92+)

### Lines 92-119: Game Constructor
```python
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snack Game")
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
```

**Line by line:**
- `pygame.init()` - Initialize pygame module
- `self.screen = pygame.display.set_mode((WIDTH, HEIGHT))` - Create 640×480 window
- `pygame.display.set_caption("Snack Game")` - Set window title
- `self.clock = pygame.time.Clock()` - Create clock for FPS control
- **Font initialization:**
  - `self.font_small = pygame.font.SysFont(None, 24)` - Small 24pt font
  - `self.font_medium = pygame.font.SysFont(None, 36)` - Medium 36pt font
  - `self.font_large = pygame.font.SysFont(None, 64)` - Large 64pt font

**Game state initialization:**
- `self.state = "MENU"` - Start at menu screen
- `self.difficulty = "NORMAL"` - Default difficulty
- `self.snake = Snake()` - Create snake object
- `self.food = None` - No food initially

**Game statistics:**
- `self.score = 0` - Current game score
- `self.high_score = self.load_high_score()` - Load best score from file
- `self.foods_eaten = 0` - Count foods eaten this game
- `self.start_time = None` - Set when game starts

**Game flags:**
- `self.paused = False` - Game not paused
- `self.base_speed = DIFFICULTY["NORMAL"]` - 10 FPS for normal mode
- `self.background = self.create_background()` - Create background surface

---

### Lines 121-127: Create Background Method
```python
def create_background(self):
    """Create a simple, clean, and minimalist gaming background"""
    bg = pygame.Surface((WIDTH, HEIGHT))
    
    # Solid dark background - clean and simple
    bg.fill(BG_DARK)
    
    return bg
```

**Line by line:**
- `bg = pygame.Surface((WIDTH, HEIGHT))` - Create blank 640×480 surface
- `bg.fill(BG_DARK)` - Fill entire surface with dark color (20,20,30)
- `return bg` - Return the background surface
- **Result:** Reusable dark background used throughout game

---

### Lines 129-136: Load High Score Method
```python
def load_high_score(self):
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as f:
                return int(f.read())
        except (IOError, ValueError):
            return 0
    return 0
```

**Line by line:**
- `if os.path.exists(HIGH_SCORE_FILE):` - Check if file exists
- `with open(HIGH_SCORE_FILE, "r") as f:` - Open file for reading
  - `with` ensures file is closed automatically
- `return int(f.read())` - Read content and convert to integer
- **Error handling:**
  - `except (IOError, ValueError):` Catches file read errors or invalid numbers
  - `return 0` - Return 0 if file corrupted or unreadable
- Final `return 0` - Return 0 if file doesn't exist
- **Result:** Always returns a valid integer (either saved high score or 0)

---

### Lines 138-146: Save High Score Method
```python
def save_high_score(self):
    if self.score > self.high_score:
        self.high_score = self.score
        try:
            with open(HIGH_SCORE_FILE, "w") as f:
                f.write(str(self.high_score))
        except IOError:
            print("Warning: Could not save high score.")
```

**Line by line:**
- `if self.score > self.high_score:` - Only save if current score is better
- `self.high_score = self.score` - Update high score variable
- `with open(HIGH_SCORE_FILE, "w") as f:` - Open file for writing (overwrites)
- `f.write(str(self.high_score))` - Convert score to string and write
- **Error handling:**
  - `except IOError:` Catches file write errors (permission denied, etc.)
  - Print warning message but don't crash
- **Result:** High score persisted to file

---

### Lines 148-154: Spawn Food Method
```python
def spawn_food(self):
    occupied = set(self.snake.body)
    free = set((x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)) - occupied
    if not free:
        return None
    return random.choice(list(free))
```

**Line by line:**
- `occupied = set(self.snake.body)` - Create set of all snake positions
- Second line creates free positions:
  - `set((x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT))` - All grid positions
  - `- occupied` - Remove snake positions (set subtraction)
  - Result: All empty grid squares
- `if not free: return None` - If no space left (shouldn't happen), return None
- `return random.choice(list(free))` - Pick random empty position
- **Result:** Food spawned at random unoccupied location

---

### Lines 156-163: Main Run Method (State Machine)
```python
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
```

**What this does:**
- `while True:` - Infinite loop (runs until game exits)
- Dispatcher based on `self.state`:
  - **"MENU"** → Show main menu screen
  - **"DIFFICULTY"** → Show difficulty selection
  - **"PLAYING"** → Run main game loop
  - **"GAME_OVER"** → Show game over screen
- State machine pattern: Only one state active at a time

---

### Lines 165-182: Run Menu Screen Method
```python
def run_menu_screen(self):
    """Main menu with game title and options"""
    self.screen.blit(self.background, (0, 0))
    self.draw_text_center("Snack Game", self.font_large, WHITE, y_offset=-80)
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
```

**Line by line:**
- `self.screen.blit(self.background, (0, 0))` - Draw dark background
- Next 5 lines: Draw text at different positions (y_offset values)
  - Title (large, -80)
  - Controls (small, +10, +40, +60)
  - Start prompt (medium, +100)
- `pygame.display.flip()` - Update display
- **Event handling:**
  - `QUIT` or `Esc` key → Exit game
  - `S` key → Move to difficulty selection

---

### Lines 184-206: Run Difficulty Screen Method
```python
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
```

**Line by line:**
- `difficulties = ["EASY", "NORMAL", "HARD"]` - List of options
- `idx = difficulties.index(self.difficulty)` - Find current selection index
- Draw background and title
- **Display loop:**
  - For each difficulty, if selected (i == idx):
    - Color: YELLOW (highlighted)
    - Text: ">>> EASY <<<" (with arrows)
  - Else:
    - Color: WHITE
    - Text: Just the name
  - Position: -20 + (50 each) = -20, 30, 80
- **Event handling:**
  - `K_UP`: Move selection up (with wrapping using %)
  - `K_DOWN`: Move selection down (with wrapping)
  - `RETURN`: Start game with selected difficulty
  - `ESCAPE`: Back to menu

---

### Lines 208-217: Reset Game Method
```python
def reset_game(self):
    """Initialize new game with selected difficulty"""
    self.base_speed = DIFFICULTY[self.difficulty]
    self.snake.reset()
    self.food = self.spawn_food()
    self.score = 0
    self.foods_eaten = 0
    self.start_time = time.time()
    self.state = "PLAYING"
```

**Line by line:**
- `self.base_speed = DIFFICULTY[self.difficulty]` - Set FPS based on difficulty
- `self.snake.reset()` - Reset snake to starting position
- `self.food = self.spawn_food()` - Place first food
- `self.score = 0` - Reset score to 0
- `self.foods_eaten = 0` - Reset food counter
- `self.start_time = time.time()` - Record current time (for duration tracking)
- `self.state = "PLAYING"` - Start game

---

### Lines 219-236: Run Game Over Screen Method
```python
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
```

**Line by line:**
- `self.save_high_score()` - Persist high score if beaten
- `elapsed_time = int(time.time() - self.start_time) if self.start_time else 0`
  - Calculate seconds played
  - `time.time()` is current time
  - Subtract `start_time` to get duration
  - Convert to int (remove decimals)
  - If no start_time, use 0
- Draw background, title, stats (Score, High Score, Foods, Time)
- **Event handling:**
  - `QUIT` → Exit
  - `ESCAPE` → Back to menu
  - `R` → Restart game

---

### Lines 238-242: Run Game (Main Loop)
```python
def run_game(self):
    """Main game loop"""
    self.handle_input()
    if not self.paused:
        self.update()
    self.draw()
    self.clock.tick(self.get_current_speed())
```

**Line by line:**
- `self.handle_input()` - Process keyboard events
- `if not self.paused: self.update()` - Only update game logic if not paused
- `self.draw()` - Render screen
- `self.clock.tick(self.get_current_speed())` - Limit FPS
  - Calls `get_current_speed()` each frame for dynamic speed

**Game loop order:** Input → Update → Draw → Cap FPS

---

### Lines 244-262: Handle Input Method
```python
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
```

**Line by line:**
- `for event in pygame.event.get():` - Get all pending events
- **Event types:**
  - `QUIT` → Close window, exit game
  - `KEYDOWN` (key pressed):
    - `ESCAPE` → Go to menu
    - `P` → Toggle pause
    - **Movement (only if not paused):**
      - `UP` → Direction (0, -1) move up
      - `DOWN` → Direction (0, 1) move down
      - `LEFT` → Direction (-1, 0) move left
      - `RIGHT` → Direction (1, 0) move right

---

### Lines 264-278: Update Game Logic Method
```python
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
```

**Line by line:**
- `self.snake.move()` - Execute snake movement
- **Wall collision check:**
  - Get head position (hx, hy)
  - Check if outside bounds:
    - hx must be 0 to 31 (GRID_WIDTH-1)
    - hy must be 0 to 23 (GRID_HEIGHT-1)
  - If outside: Game Over
- **Self collision check:**
  - If snake head in body: Game Over
- **Food collision check:**
  - If food exists AND head is at food position:
    - `self.score += 1` - Increase score
    - `self.foods_eaten += 1` - Increase counter
    - `self.snake.grow()` - Add growth pending
    - `self.food = self.spawn_food()` - Spawn new food

---

### Lines 280-283: Get Current Speed Method
```python
def get_current_speed(self):
    """Calculate current game speed based on difficulty and foods eaten"""
    speed = self.base_speed + (self.foods_eaten // 5)
    return min(speed, 20)  # Cap at 20 FPS
```

**Line by line:**
- `speed = self.base_speed + (self.foods_eaten // 5)`
  - Start with base speed (8, 10, or 14 FPS)
  - Add 1 FPS for every 5 foods eaten
  - Example: NORMAL (10) + 2 foods = 10 + 0 = 10 FPS
  - Example: NORMAL (10) + 12 foods = 10 + 2 = 12 FPS
- `return min(speed, 20)` - Cap at 20 FPS maximum
  - Prevents game from becoming unplayable

---

### Lines 285-315: Draw Method (Rendering)
```python
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
```

**Line by line:**
- `self.screen.blit(self.background, (0, 0))` - Draw dark background
- `self.draw_grid()` - Draw grid lines
- `self.snake.draw(self.screen)` - Draw snake
- **Food rendering:**
  - If food exists: Draw red square at food position
- **HUD rendering:**
  - Score (top-left, WHITE)
  - High score (top-right, YELLOW)
  - Difficulty (bottom-left, ORANGE)
  - Speed (bottom-right, ORANGE)
- **Pause indicator:**
  - If paused: Draw "PAUSED" in center
- `pygame.display.flip()` - Update entire display

---

### Lines 317-320: Draw Grid Method
```python
def draw_grid(self):
    for x in range(0, WIDTH, TILE):
        pygame.draw.line(self.screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILE):
        pygame.draw.line(self.screen, GRAY, (0, y), (WIDTH, y))
```

**Line by line:**
- **Vertical lines:**
  - `for x in range(0, WIDTH, TILE):` Loop every 20 pixels horizontally
  - Draw line from (x, 0) to (x, HEIGHT) in GRAY
  - Result: 32 vertical lines
- **Horizontal lines:**
  - `for y in range(0, HEIGHT, TILE):` Loop every 20 pixels vertically
  - Draw line from (0, y) to (WIDTH, y) in GRAY
  - Result: 24 horizontal lines
- **Total:** 32×24 grid pattern

---

### Lines 322-325: Draw Text Center Method
```python
def draw_text_center(self, text, font, color, y_offset=0):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    self.screen.blit(surf, rect)
```

**Line by line:**
- `surf = font.render(text, True, color)` - Create text surface
  - `True` means anti-aliased (smooth edges)
- `rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))`
  - Create rectangle centered at screen center + y_offset
- `self.screen.blit(surf, rect)` - Draw text at centered position

---

## 📌 Section 7: Main Entry Point (Lines 328-332)

### Lines 328-329: Main Function
```python
def main():
    game = Game()
    game.run()
```

**What this does:**
- `game = Game()` - Create game object (runs __init__)
- `game.run()` - Start the game loop

---

### Lines 332: Main Guard
```python
if __name__ == "__main__":
    main()
```

**What this does:**
- `__name__` is a special variable
- When script runs directly: `__name__ == "__main__"` is True
- When script imported: `__name__` is the module name (not "__main__")
- Only executes main() when script is run directly, not when imported
- **Best practice:** Prevents accidental execution if file is imported

---

## 📊 Code Summary Statistics

| Metric | Value |
|--------|-------|
| Total Lines | 353 |
| Classes | 2 (Snake, Game) |
| Methods | 16 (Snake: 7, Game: 16) |
| Game States | 4 (MENU, DIFFICULTY, PLAYING, GAME_OVER) |
| Difficulty Levels | 3 (EASY, NORMAL, HARD) |
| Colors Used | 9 |
| Grid Size | 32×24 tiles (640×480 pixels) |
| Max FPS | 20 |

---

## 🎮 Game Flow Diagram

```
START
  ↓
pygame.init()
  ↓
Run Game Loop:
  │
  ├─→ State = MENU
  │    ├─→ Show title and instructions
  │    └─→ Wait for S key
  │
  ├─→ State = DIFFICULTY
  │    ├─→ Show difficulty options
  │    ├─→ Allow UP/DOWN selection
  │    └─→ Wait for ENTER
  │
  ├─→ State = PLAYING
  │    ├─→ Handle Input (arrow keys, P for pause)
  │    ├─→ Update (move snake, check collisions, spawn food)
  │    ├─→ Draw (render grid, snake, food, HUD)
  │    ├─→ Cap FPS (speed increases with foods)
  │    └─→ Check game over conditions
  │
  ├─→ State = GAME_OVER
  │    ├─→ Save high score if beaten
  │    ├─→ Show final stats
  │    └─→ Wait for R (restart) or ESC (menu)
  │
  └─→ Repeat until QUIT

EXIT
```

---

## 🔑 Key Programming Concepts Used

1. **Classes** - Snake and Game encapsulate data and behavior
2. **State Machine** - Four distinct game states with transitions
3. **Event Loop** - Continuous polling for user input
4. **Collision Detection** - Head-wall, head-self, head-food
5. **Game Loop Pattern** - Input → Update → Draw (standard in all games)
6. **File I/O** - High score persistence
7. **Error Handling** - try/except for pygame and file operations
8. **Vector Math** - Direction as (dx, dy) tuples
9. **Modulo Operator** - Wrap-around for difficulty selection
10. **Set Operations** - Efficient food spawning

---
