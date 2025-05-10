# main.py
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import settings
from maze_generator import generate_maze
from player import Player
import math
from math import cos, sin
from PIL import Image

texture_wall = None

def load_texture(path):
    global texture_wall
    img = Image.open(path)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = img.convert("RGBA").tobytes()
    width, height = img.size

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    return texture_id

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.5, 0.7, 1.0, 1.0)  # sky color

    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, settings.SCREEN_WIDTH / settings.SCREEN_HEIGHT, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def draw_floor():
    glColor3f(0.3, 0.3, 0.3)  # dark gray floor
    glBegin(GL_QUADS)
    glVertex3f(-50, 0, -50)
    glVertex3f(50, 0, -50)
    glVertex3f(50, 0, 50)
    glVertex3f(-50, 0, 50)
    glEnd()

def draw_cube(x, y):
    glPushMatrix()
    glTranslatef(x, 0, y)
    glBindTexture(GL_TEXTURE_2D, texture_wall)

    glBegin(GL_QUADS)

    # Front
    glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
    glTexCoord2f(1, 0); glVertex3f(1, 0, 0)
    glTexCoord2f(1, 1); glVertex3f(1, 1, 0)
    glTexCoord2f(0, 1); glVertex3f(0, 1, 0)

    # Back
    glTexCoord2f(0, 0); glVertex3f(0, 0, -1)
    glTexCoord2f(1, 0); glVertex3f(1, 0, -1)
    glTexCoord2f(1, 1); glVertex3f(1, 1, -1)
    glTexCoord2f(0, 1); glVertex3f(0, 1, -1)

    # Left
    glTexCoord2f(0, 0); glVertex3f(0, 0, -1)
    glTexCoord2f(1, 0); glVertex3f(0, 0, 0)
    glTexCoord2f(1, 1); glVertex3f(0, 1, 0)
    glTexCoord2f(0, 1); glVertex3f(0, 1, -1)

    # Right
    glTexCoord2f(0, 0); glVertex3f(1, 0, 0)
    glTexCoord2f(1, 0); glVertex3f(1, 0, -1)
    glTexCoord2f(1, 1); glVertex3f(1, 1, -1)
    glTexCoord2f(0, 1); glVertex3f(1, 1, 0)

    # Top
    glTexCoord2f(0, 0); glVertex3f(0, 1, 0)
    glTexCoord2f(1, 0); glVertex3f(1, 1, 0)
    glTexCoord2f(1, 1); glVertex3f(1, 1, -1)
    glTexCoord2f(0, 1); glVertex3f(0, 1, -1)

    # Bottom
    glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
    glTexCoord2f(1, 0); glVertex3f(1, 0, 0)
    glTexCoord2f(1, 1); glVertex3f(1, 0, -1)
    glTexCoord2f(0, 1); glVertex3f(0, 0, -1)

    glEnd()
    glPopMatrix()

def main():
    global texture_wall

    pygame.init()
    pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
    init()

    texture_wall = load_texture('textures/brick.png')

    maze = generate_maze(settings.MAP_ROWS, settings.MAP_COLS)
    for row in maze:
        print(row)  # debug print of maze

    player = Player()

    pygame.event.set_grab(True)  # lock mouse in window
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()
    toggle_mouse = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_TAB:
                    toggle_mouse = not toggle_mouse
                    pygame.event.set_grab(not toggle_mouse)
                    pygame.mouse.set_visible(toggle_mouse)

        rel = pygame.mouse.get_rel()
        player.angle += rel[0] * 0.003

        keys = pygame.key.get_pressed()
        speed = 0.1
        rot_speed = 0.05  # rotation speed
        dx = speed * cos(player.angle)
        dy = speed * sin(player.angle)

        # Move forward
        if keys[pygame.K_w]:
            next_x = player.x + dx
            next_y = player.y + dy
            if not player.check_collision(next_x, player.y, maze):
                player.x = next_x
            if not player.check_collision(player.x, next_y, maze):
                player.y = next_y

        # Move backward
        if keys[pygame.K_s]:
            next_x = player.x - dx
            next_y = player.y - dy
            if not player.check_collision(next_x, player.y, maze):
                player.x = next_x
            if not player.check_collision(player.x, next_y, maze):
                player.y = next_y

        # Strafe left
        if keys[pygame.K_a]:
            strafe_x = speed * cos(player.angle - math.pi / 2)
            strafe_y = speed * sin(player.angle - math.pi / 2)
            next_x = player.x + strafe_x
            next_y = player.y + strafe_y
            if not player.check_collision(next_x, player.y, maze):
                player.x = next_x
            if not player.check_collision(player.x, next_y, maze):
                player.y = next_y

        # Strafe right
        if keys[pygame.K_d]:
            strafe_x = speed * cos(player.angle + math.pi / 2)
            strafe_y = speed * sin(player.angle + math.pi / 2)
            next_x = player.x + strafe_x
            next_y = player.y + strafe_y
            if not player.check_collision(next_x, player.y, maze):
                player.x = next_x
            if not player.check_collision(player.x, next_y, maze):
                player.y = next_y

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        gluLookAt(player.x, 0.5, player.y,
                  player.x + cos(player.angle), 0.5, player.y + sin(player.angle),
                  0, 1, 0)

        draw_floor()

        for row in range(settings.MAP_ROWS):
            for col in range(settings.MAP_COLS):
                if maze[row][col] == 1:
                    draw_cube(col, -row)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
