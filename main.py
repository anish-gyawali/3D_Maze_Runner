import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GLUT as glut
import settings
from player import Player
from math import cos, sin, pi, hypot
from PIL import Image
import time

fixed_maze = [
    [1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,1,0,0,0,0,1],
    [1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,1],
    [1,0,1,1,1,1,1,0,1,1],
    [1,0,1,0,0,0,0,0,0,1],
    [1,0,1,0,1,1,1,1,0,1],
    [1,0,1,0,1,0,0,1,0,1],
    [1,0,0,0,1,0,1,1,0,0],
    [1,1,1,1,1,1,1,1,1,1],
]

START_POS = (1.5, 1.5)
FINISH_TILE = (8, 8)

COIN_POSITIONS = [
    (1.5, 1.5), (3.5, 1.5), (5.5, 1.5), (7.5, 2.5), (7.5, 4.5),
    (5.5, 5.5), (3.5, 5.5), (1.5, 6.5), (2.5, 8.5), (6.5, 8.5)
]
collected_coins = set()

wall_tex = None
floor_tex = None

def load_texture(path):
    img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
    img_data = img.convert("RGBA").tobytes()
    width, height = img.size
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return tex_id

def draw_floor():
    glBindTexture(GL_TEXTURE_2D, floor_tex)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-50, 0, -50)
    glTexCoord2f(10, 0); glVertex3f(50, 0, -50)
    glTexCoord2f(10, 10); glVertex3f(50, 0, 50)
    glTexCoord2f(0, 10); glVertex3f(-50, 0, 50)
    glEnd()

def draw_coin(x, z):
    glColor3f(1, 1, 0)
    glPushMatrix()
    glTranslatef(x + 0.5, 0.1, z + 0.5)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0)
    for i in range(21):
        angle = 2 * pi * i / 20
        glVertex3f(cos(angle) * 0.2, 0, sin(angle) * 0.2)
    glEnd()
    glPopMatrix()

def draw_cube(x, z):
    glPushMatrix()
    glTranslatef(x, 0, z)
    glBindTexture(GL_TEXTURE_2D, wall_tex)
    glColor3f(1, 1, 1)
    h = 1.5
    glBegin(GL_QUADS)
    for face in [
        [(0,0,0),(1,0,0),(1,h,0),(0,h,0)],
        [(0,0,-1),(1,0,-1),(1,h,-1),(0,h,-1)],
        [(0,0,-1),(0,0,0),(0,h,0),(0,h,-1)],
        [(1,0,0),(1,0,-1),(1,h,-1),(1,h,0)],
        [(0,h,0),(1,h,0),(1,h,-1),(0,h,-1)]
    ]:
        for i, (vx, vy, vz) in enumerate(face):
            glTexCoord2f(i % 2, i // 2)
            glVertex3f(vx, vy, vz)
    glEnd()
    glPopMatrix()

def draw_minimap(maze, player):
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    tile = 8
    off = 10
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            glColor3f(1, 1, 1) if maze[r][c] == 1 else glColor3f(0, 0, 0)
            x = c * tile + off
            y = r * tile + off
            glBegin(GL_QUADS)
            glVertex2f(x, y)
            glVertex2f(x+tile, y)
            glVertex2f(x+tile, y+tile)
            glVertex2f(x, y+tile)
            glEnd()
    for cx, cz in COIN_POSITIONS:
        if (cx, cz) not in collected_coins:
            glColor3f(1, 1, 0)
            x = cx * tile + off
            y = cz * tile + off
            glBegin(GL_QUADS)
            glVertex2f(x-2, y-2)
            glVertex2f(x+2, y-2)
            glVertex2f(x+2, y+2)
            glVertex2f(x-2, y+2)
            glEnd()
    px = player.x * tile + off
    py = player.z * tile + off
    glColor3f(1, 0, 0)
    glBegin(GL_QUADS)
    glVertex2f(px-2, py-2)
    glVertex2f(px+2, py-2)
    glVertex2f(px+2, py+2)
    glVertex2f(px-2, py+2)
    glEnd()
    glColor3f(0, 1, 0)
    dx = cos(player.angle) * 10
    dy = sin(player.angle) * 10
    glBegin(GL_LINES)
    glVertex2f(px, py)
    glVertex2f(px + dx, py + dy)
    glEnd()
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

def draw_hud(elapsed):
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, settings.SCREEN_WIDTH, 0, settings.SCREEN_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(0, 1, 0)  # Green
    glRasterPos2f(settings.SCREEN_WIDTH - 180, settings.SCREEN_HEIGHT - 30)
    for ch in f"Coins: {len(collected_coins)} / {len(COIN_POSITIONS)}":
        glut.glutBitmapCharacter(glut.GLUT_BITMAP_HELVETICA_18, ord(ch))
    glRasterPos2f(settings.SCREEN_WIDTH - 180, settings.SCREEN_HEIGHT - 50)
    for ch in f"Time: {int(elapsed)}s":
        glut.glutBitmapCharacter(glut.GLUT_BITMAP_HELVETICA_18, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

def show_win_overlay(elapsed):
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, settings.SCREEN_WIDTH, 0, settings.SCREEN_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(1, 1, 0)
    glRasterPos2f(settings.SCREEN_WIDTH // 2 - 50, settings.SCREEN_HEIGHT // 2 + 10)
    for ch in b"GAME OVER!":
        glut.glutBitmapCharacter(glut.GLUT_BITMAP_HELVETICA_18, ch)
    glRasterPos2f(settings.SCREEN_WIDTH // 2 - 60, settings.SCREEN_HEIGHT // 2 - 10)
    for ch in f"Time: {elapsed}s  Coins: {len(collected_coins)} / {len(COIN_POSITIONS)}":
        glut.glutBitmapCharacter(glut.GLUT_BITMAP_HELVETICA_18, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

def main():
    global wall_tex, floor_tex
    glut.glutInit()
    pygame.init()

    if settings.FULLSCREEN:
        info = pygame.display.Info()
        settings.SCREEN_WIDTH = info.current_w
        settings.SCREEN_HEIGHT = info.current_h
        pygame.display.set_mode((0, 0), pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN)
    else:
        pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

    # OpenGL setup
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.5, 0.7, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, settings.SCREEN_WIDTH/settings.SCREEN_HEIGHT, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    wall_tex = load_texture('textures/brick.png')
    floor_tex = load_texture('textures/stone.png')

    player = Player(x=START_POS[0], z=START_POS[1])
    clock = pygame.time.Clock()
    won = False
    start_time = time.time()
    elapsed = 0
    running = True
    while running:
        if not won:
            elapsed = time.time() - start_time
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False
        keys = pygame.key.get_pressed()
        if not won:
            if keys[pygame.K_a]: player.angle -= 0.05
            if keys[pygame.K_d]: player.angle += 0.05
            spd = 0.1
            dx, dz = spd * cos(player.angle), spd * sin(player.angle)
            if keys[pygame.K_w]: player.move(dx, dz, fixed_maze)
            if keys[pygame.K_s]: player.move(-dx, -dz, fixed_maze)
            if keys[pygame.K_q]: player.move(cos(player.angle - pi/2)*spd, sin(player.angle - pi/2)*spd, fixed_maze)
            if keys[pygame.K_e]: player.move(cos(player.angle + pi/2)*spd, sin(player.angle + pi/2)*spd, fixed_maze)
            for cx, cz in COIN_POSITIONS:
                if (cx, cz) not in collected_coins and hypot(player.x - cx, player.z - cz) < 0.5:
                    collected_coins.add((cx, cz))
            if int(player.x) == FINISH_TILE[0] and int(player.z) == FINISH_TILE[1]:
                won = True
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(player.x, 0.8, player.z,
                  player.x + cos(player.angle), 0.8, player.z + sin(player.angle),
                  0, 1, 0)
        draw_floor()
        for r in range(len(fixed_maze)):
            for c in range(len(fixed_maze[0])):
                if fixed_maze[r][c] == 1:
                    draw_cube(c, r)
        for cx, cz in COIN_POSITIONS:
            if (cx, cz) not in collected_coins:
                draw_coin(cx, cz)
        draw_minimap(fixed_maze, player)
        draw_hud(elapsed)
        if won:
            show_win_overlay(int(elapsed))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    main()
