# 🐍 Snake Game

A fully-featured, professional Snake game built with Python and pygame. Features clean minimalist design, smooth gameplay, and multiple difficulty levels.

**Status**: ✅ Production Ready | **Version**: 1.0.0 | **Quality**: ⭐⭐⭐⭐⭐

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Dependencies](#dependencies)
3. [Installation Guide](#installation-guide)
4. [How to Play](#how-to-play)
5. [Controls](#controls)
6. [Features](#features)
7. [Difficulty Levels](#difficulty-levels)
8. [Game Mechanics](#game-mechanics)
9. [Statistics & Scoring](#statistics--scoring)
10. [Technical Details](#technical-details)

---

## 🚀 Quick Start

### Fastest Way to Play (3 steps)

```powershell
# Step 1: Install dependencies
python -m pip install -r requirements.txt

# Step 2: Run the game
python snake_game.py

# Step 3: Start playing!
# Press S to start from the menu
```

---

## 📦 Dependencies

### Required Packages

| Package | Version | Purpose |
|---------|---------|---------|
| **pygame** | Latest | Game engine, graphics, and input handling |
| **Python** | 3.7+ | Programming language |

### Built-in Python Modules Used
- `random` - Random food spawning
- `sys` - System exit handling
- `os` - File operations (high score)
- `time` - Game timing and statistics

### File: `requirements.txt`
```
pygame
```

---

## 💻 Installation Guide

### Prerequisites
- Python 3.7 or higher installed
- pip (Python package manager)
- ~50 MB disk space
- Internet connection (for downloading pygame)

### Step-by-Step Installation

#### Step 1: Verify Python Installation

```powershell
# Check if Python is installed
python --version

# Expected output: Python 3.x.x
# If not installed, download from https://www.python.org
```

#### Step 2: Verify pip Installation

```powershell
# Check if pip is installed
pip --version

# Expected output: pip x.x.x from ...
# pip is usually installed with Python
```

#### Step 3: Install pygame from requirements.txt

**Recommended Method:**
```powershell
# Navigate to game directory
cd "path\to\snake-game"

# Install using requirements.txt
python -m pip install -r requirements.txt
```

**Alternative Method (if requirements.txt fails):**
```powershell
# Install pygame directly
python -m pip install pygame
```

**For M1/M2 Mac users:**
```bash
pip install pygame --prefer-binary
```

**For Linux users:**
```bash
python3 -m pip install pygame
```

#### Step 4: Verify Installation

```powershell
# Test if pygame is installed correctly
python -c "import pygame; print('pygame version:', pygame.ver)"
```

Expected output:
```
pygame version: 2.x.x
```


---

## 🎮 How to Play

### Starting the Game

```powershell
python snack_game.py
```

### Game Flow

1. **Main Menu** - See game title and instructions
   - Press **S** to start
   - Press **Esc** to quit

2. **Difficulty Selection** - Choose your challenge
   - Use **↑/↓** arrow keys to select
   - Press **Enter** to confirm
   - Press **Esc** to go back

3. **Gameplay** - Main game screen
   - Use **↑↓←→** arrow keys to move
   - Press **P** to pause/unpause
   - Press **Esc** to return to menu
   - Press **R** to restart (from game over)

4. **Game Over** - View your results
   - See final score, high score, foods eaten, time
   - Press **R** to restart
   - Press **Esc** to return to menu

---

## ⌨️ Controls

| Key | Screen | Action |
|-----|--------|--------|
| **S** | Menu | Start game |
| **↑** | Difficulty | Select previous difficulty |
| **↓** | Difficulty | Select next difficulty |
| **Enter** | Difficulty | Confirm difficulty selection |
| **↑** | Gameplay | Move snake up |
| **↓** | Gameplay | Move snake down |
| **←** | Gameplay | Move snake left |
| **→** | Gameplay | Move snake right |
| **P** | Gameplay | Pause/Resume game |
| **Esc** | Gameplay | Return to menu |
| **R** | Game Over | Restart game |
| **Esc** | Game Over | Return to menu |
| **Esc** | Menu | Quit game |

---

## ✨ Features

### Core Gameplay
✅ **Snake Movement** - Smooth directional control with input queuing
✅ **Food System** - Random food spawning on grid
✅ **Growth Mechanics** - Snake grows when eating food
✅ **Collision Detection** - Wall and self-collision detection
✅ **Score Tracking** - Points awarded per food eaten

### Game Modes
✅ **Three Difficulty Levels** - Easy, Normal, Hard
✅ **Menu Navigation** - Intuitive menu system
✅ **Pause/Resume** - Pause game at any time
✅ **Restart Option** - Quick game restart

### Statistics & Progress
✅ **Score Display** - Real-time score tracking
✅ **High Score** - Persistent high score (saved to file)
✅ **Foods Eaten Counter** - Total foods eaten tracking
✅ **Elapsed Time** - Game duration tracking
✅ **Speed Display** - Current game speed indicator
✅ **Difficulty Display** - Current difficulty indicator

### User Experience
✅ **Smooth Animations** - Fluid snake movement
✅ **Visual Feedback** - Clear visual indicators
✅ **Responsive Controls** - Immediate input response
✅ **Professional Design** - Minimalist modern aesthetic
✅ **Dark Theme** - Easy on the eyes, professional look

---

## 🎯 Difficulty Levels

### EASY (8 FPS)
- **Speed**: Slowest
- **Best For**: Learning and casual play
- **Speed Progression**: +1 FPS per 5 foods eaten
- **Max Speed**: Capped at 20 FPS

### NORMAL (10 FPS) ⭐ Recommended
- **Speed**: Balanced
- **Best For**: Standard gameplay experience
- **Speed Progression**: +1 FPS per 5 foods eaten
- **Max Speed**: Capped at 20 FPS

### HARD (14 FPS)
- **Speed**: Fastest
- **Best For**: Experienced players
- **Speed Progression**: +1 FPS per 5 foods eaten
- **Max Speed**: Capped at 20 FPS

### Speed Mechanics
```
Current Speed = Base Speed + (Foods Eaten ÷ 5)
Maximum Possible Speed = 20 FPS (hardcapped)

Example:
NORMAL (Base 10) + 5 foods = 11 FPS
NORMAL (Base 10) + 15 foods = 13 FPS
NORMAL (Base 10) + 50 foods = 20 FPS (capped)
```

---

## 🕹️ Game Mechanics

### Movement System
- **Direction Queuing**: Next direction buffered for smooth turns
- **Prevents Reversal**: Snake cannot reverse into itself
- **Smooth Transitions**: Directional changes apply immediately

### Food Spawning
- **Random Location**: Food spawns in random unoccupied grid space
- **Never Overlaps**: Food never spawns on snake body
- **One at a Time**: Only one food on screen at once
- **Always Present**: Food always available (unless grid full)

### Collision Detection
- **Wall Collision**: Game ends if snake hits boundary
- **Self Collision**: Game ends if snake eats itself
- **Grid Boundaries**: 32x24 tile grid (640x480 pixels)

### Growth System
- **Growth Amount**: Snake grows by 1 segment per food
- **Growth Animation**: Smooth growth effect
- **No Maximum Length**: Snake can grow infinitely

---

## 📊 Statistics & Scoring

### During Gameplay
- **Current Score**: Number of foods eaten (1 point per food)
- **High Score**: Best score from all games
- **Foods Eaten**: Total count of food consumed
- **Current Speed**: Real-time game speed (FPS)
- **Difficulty**: Currently selected difficulty level

### Game Over Screen
- **Final Score**: Points earned this game
- **High Score**: Best score ever achieved
- **Foods Eaten**: Total foods eaten this game
- **Elapsed Time**: How long you played (seconds)

### High Score System
- **Saved to File**: `snake_game.highscore`
- **Persistent**: Survives between game sessions
- **Auto-Updated**: Updates when you beat high score
- **Text Format**: Plain text file (human-readable)

---

## 🎨 Visual Design

### Theme: Minimalist Professional
- **Background**: Solid dark navy (20, 20, 30) - Zero distractions
- **Grid**: Subtle gray lines for board definition
- **Snake Head**: Bright cyan with white border
- **Snake Body**: Lime green with dark green outline
- **Food**: Bright red for easy visibility
- **Text**: White for primary, yellow for highlights

### Color Palette
| Element | RGB | Hex |
|---------|-----|-----|
| Background | (20, 20, 30) | #141E1E |
| Snake Head | (120, 200, 255) | #78C8FF |
| Snake Body | (100, 255, 100) | #64FF64 |
| Food | (255, 100, 100) | #FF6464 |
| Grid | (100, 110, 130) | #646E82 |
| Text (Primary) | (255, 255, 255) | #FFFFFF |
| Text (Highlight) | (255, 240, 80) | #FFF050 |
| Text (Secondary) | (255, 140, 80) | #FF8C50 |

---


## ⚙️ Technical Details

### System Requirements
```
OS:              Windows, macOS, Linux
Python:          3.7 or higher
RAM:             100 MB minimum
Storage:         50 MB for pygame
Display:         640x480 minimum resolution
```

### Game Window
```
Window Size:     640x480 pixels
Grid:            32x24 tiles
Tile Size:       20x20 pixels
Aspect Ratio:    4:3
Resizable:       No
Fullscreen:      No
```

### Performance
```
Base FPS Range:  8-14 (depends on difficulty)
Max FPS:         20 (hardcapped)
Frame Time:      50-125 milliseconds
Target Platform: All desktop platforms
```
---


## 📄 License & Attribution

This game is created for educational purposes. Feel free to modify, improve, and distribute as needed.

---


**Enjoy the game! 🎮✨**

---

## 📞 Support

If you encounter any issues or have questions, you can contact me:

### 👤 Developer Information

| Contact Type | Details |
|--------------|---------|
| **Name** | Sagar Bhadra |
| **Mobile** | +91 7980394584 |
| **Email** | sagarbhadra404@gmail.com |
| **GitHub** | [github.com/SagarBhadra01](https://github.com/SagarBhadra01) |
| **LinkedIn** | [linkedin.com/in/sagarbhadra01](https://linkedin.com/in/sagarbhadra01) |
| **Twitter** | [@SagarBhadra01](https://twitter.com/SagarBhadra01) |


---

**Last Updated**: November 15, 2025  
