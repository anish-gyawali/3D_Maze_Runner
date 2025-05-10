# player.py

import settings

class Player:
    def __init__(self, x=1.5, y=1.5, z=0, angle=0):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle

    def check_collision(self, new_x, new_y, maze):
        tile_x = int(new_x)
        tile_y = int(new_y)
        if 0 <= tile_x < settings.MAP_COLS and 0 <= tile_y < settings.MAP_ROWS:
            return maze[tile_y][tile_x] == 1  # True if wall
        return True  # out of bounds treated as wall
