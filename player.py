# player.py

class Player:
    def __init__(self, x=1.5, z=1.5, angle=0):
        self.x = x
        self.z = z
        self.angle = angle

    def can_move(self, x, z, maze):
        r, c = int(z), int(x)
        return 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c] == 0

    def move(self, dx, dz, maze):
        if self.can_move(self.x + dx, self.z, maze):
            self.x += dx
        if self.can_move(self.x, self.z + dz, maze):
            self.z += dz
