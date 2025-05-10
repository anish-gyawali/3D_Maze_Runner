# maze_generator.py

import random

def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    for y in range(1, rows-1):
        for x in range(1, cols-1):
            maze[y][x] = random.choice([0, 1])

    maze[1][1] = 0  # start point open
    return maze
