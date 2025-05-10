# 3D Maze Runner

A first-person 3D maze game built with **PyOpenGL** and **Pygame**.

Explore a 3D maze, collect coins, and reach the goal as fast as you can!


## Features

- First-person 3D movement using OpenGL
- Collectible coins (shown on the minimap)
- Timer + coin counter (HUD)
- Win condition with final score display
- Custom textures for walls and floors
- Minimap showing maze, coins, and player direction

## 📁 Folder Structure

```bash

3D\_Maze\_Runner/
├── main.py             # Main game loop
├── player.py           # Player class
├── settings.py         # Game constants
├── requirements.txt    # Python dependencies
├── textures/
│   ├── brick.png       # Wall texture
│   └── stone.png       # Floor texture

````

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/anish-gyawali/3D_Maze_Runner.git
cd 3D_Maze_Runner
````

### 2. Set up a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the game

```bash
python main.py
```

---

## Controls

| Key     | Action                |
| ------- | --------------------- |
| `W`/`S` | Move forward/backward |
| `A`/`D` | Rotate left/right     |
| `Q`/`E` | Strafe left/right     |
| `ESC`   | Quit game             |

---

## License

MIT License. Feel free to modify or expand for learning or your own projects.
