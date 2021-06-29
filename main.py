import pygame, sys
from players import *
from maps import *
from tools import Tools
import time

# General Setup
pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)
dis = pygame.display.set_mode(WINDOW_SIZE)
screen = pygame.Surface((2400, 1800)) # 400, 300
pygame.display.set_caption('Pygame Prototype')
SCREEN_MULTI = 3

map = Map(screen, 'map_files\level_1_1')
player = Player(map.spawn_locations[0])

tools = Tools()

# GAME LOOP
running = True

while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.keys['mouse_left'] = True
            elif event.button == 3:
                player.keys['mouse_right'] = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                player.keys['mouse_left'] = False
            elif event.button == 3:
                player.keys['mouse_right'] = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.keys['left'] = True
            if event.key == pygame.K_d:
                player.keys['right'] = True
            if event.key == pygame.K_w:
                player.keys['up'] = True
            if event.key == pygame.K_s:
                player.keys['down'] = True
            if event.key == pygame.K_SPACE:
                map.shake = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.keys['left'] = False
            if event.key == pygame.K_d:
                player.keys['right'] = False
            if event.key == pygame.K_w:
                player.keys['up'] = False
            if event.key == pygame.K_s:
                player.keys['down'] = False
            if event.key == pygame.K_SPACE:
                map.shake = False

    # Frame Rate Check
    tools.frame_rate_check()

    # Update Game Screen
    map.update(screen, player)

    # Updates player
    #player.update(level_map.tiles)

    # Draws everything
    #level_map.draw(screen, load_map('map_files\level_1_1'), (180, 180, 200), player)
    


    # Shows display and Updates
    surf = pygame.transform.scale(screen, WINDOW_SIZE)
    dis.blit(surf, (0, 0))
    pygame.display.flip()
    clock.tick(60)
