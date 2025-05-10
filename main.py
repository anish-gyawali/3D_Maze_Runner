# main.py

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import settings
from maze_generator import generate_maze
from player import Player
from math import cos, sin
from PIL import Image

texture_wall = None  # will hold the texture ID

def load_texture(path):
    global texture_wall
    img = Image.open(path)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)  # OpenGL expects flipped vertically
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
    glEnable(GL_TEXTURE_2D)  # Enable 2D texturing
    glClearColor(0.5, 0.7, 1.0, 1.0)  # sky color

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

    # Load texture (must exist in textures/ folder)
    texture_wall = load_texture('textures/brick.png')

    maze = generate_maze(settings.MAP_ROWS, settings.MAP_COLS)
    player = Player()

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        speed = 0.1
        if keys[pygame.K_w]:
            player.x += speed * cos(player.angle)
            player.y += speed * sin(player.angle)
        if keys[pygame.K_s]:
            player.x -= speed * cos(player.angle)
            player.y -= speed * sin(player.angle)
        if keys[pygame.K_a]:
            player.angle -= 0.05
        if keys[pygame.K_d]:
            player.angle += 0.05

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        gluLookAt(player.x, 0.5, player.y,
                  player.x + cos(player.angle), 0.5, player.y + sin(player.angle),
                  0, 1, 0)

        for row in range(settings.MAP_ROWS):
            for col in range(settings.MAP_COLS):
                if maze[row][col] == 1:
                    draw_cube(col, -row)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
