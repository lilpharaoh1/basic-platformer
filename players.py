import pygame
import time
import numpy as np

class Player:
    def __init__(self, spawn):
        x, y = spawn
        self.dim_multi = 1 
        self.player_dim = [64*self.dim_multi, 128*self.dim_multi]
        self.rect = pygame.Rect(x, y, self.player_dim[0], self.player_dim[1])
        self.cam_center = [300, 200]
        self.rect.x = x
        self.rect.y = y
        # self.colors = {'stand1': (180, 100, 100), 'stand2': (200, 100, 100), 'stand3': (220, 100, 100),
        #              'jump': (100, 200, 100), 'drift': (100, 100, 200)}
        self.image = [('stand1', (180, 100, 100)), ('stand2', (200, 100, 100)), ('stand3', (220, 100, 100)),
                      ('jumping', (100, 200, 100)), ('falling', (100, 250, 100)), ('runleft', (100, 150, 180)),
                      ('driftleft', (100, 100, 180)),
                      ('runright', (100, 150, 220)), ('dirftright', (100, 100, 220))]
        self.momentum = [0, 0]
        self.momentum[0] = 0
        self.momentum[1] = 0
        self.keys = {'right': False, 'left': False, 'up': False, 'down': False, 'mouse_right': False, 'mouse_left': False}
        self.collisions = {'top': False, 'bottom': False, "right": False, 'left': False}
        self.mouse_direction = {'right': False, 'left': False, 'up': False, 'down': False}
        self.attack = {'up': False, 'down': False, "right": False, 'left': False}
        self.movement_info = {
            'accel' : 0.3,
            'move_speed' : 12,
            'friction_coeff' : 0.2
        }
        self.jump_info = {
            'jump_count': 2,
            'jump_count_max': 2,
            'max_jump_speed': 24,
            'jump_timer': 0.5,
            'time_before': time.time()
        }
        self.last_time = time.time()

    def draw(self, screen, order, x, y):
        colour = 0
        # Stand Animation
        if order == 1: colour = self.image[0][1]
        if order == 2: colour = self.image[1][1]
        if order == 3: colour = self.image[2][1]

        # Lateral Movement Animation
        if self.momentum[0] < 0 and not self.collisions['left']:
            if self.keys['left']: colour = self.image[5][1]
            else: colour = self.image[6][1]
        if self.momentum[0] > 0 and not self.collisions['right']:
            if self.keys['right']: colour = self.image[7][1]
            else: colour = self.image[8][1]

        # Jumping Animation
        if self.momentum[1] < 0: colour = self.image[3][1]
        if self.momentum[1] >= 0 and not self.collisions['bottom']: colour = self.image[4][1]

        pygame.draw.rect(screen, colour, pygame.Rect(x, y, self.player_dim[0], self.player_dim[1]))
        # screen.blit(player_image, (self.rect.x, self.rect.y))


    def find_hit_zones(self):
        attack_angle = 0.611 # 35 degrees
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0] * 3
        mouse_y = mouse_pos[1] * 3
        y_sign = mouse_y - (self.rect.y + (self.player_dim[1] / 2)) # neg is up, pos is down
        y_amp = abs(y_sign)
        x_sign = mouse_x - (self.rect.x + (self.player_dim[0] / 2)) # neg is left, pos is right
        x_amp = abs(x_sign)
        thres_x = np.tan(attack_angle) * y_amp

        self.mouse_direction = {'right': False, 'left': False, 'up': False, 'down': False}
        if x_amp > thres_x: # attacking to the side
            if x_sign > 0:
                if not self.collisions['right']:
                    self.mouse_direction['right'] = True
            else:
                if not self.collisions['left']:
                    self.mouse_direction['left'] = True
        else: # attacking vertically
            if y_sign > 0:
                if not self.collisions['bottom']:
                    self.mouse_direction['down'] = True
            else:
                if not self.collisions['top']:
                    self.mouse_direction['up'] = True


    def axis_collision_test(self, block_list, axis):
        if axis == 'x':
            hit_list = self.collision_test(block_list)
            for hit in hit_list:
                if self.momentum[0] > 0:
                    self.collisions['right'] = True
                    self.rect.right = hit.left
                    if self.momentum[0] > 0: self.momentum[0] = 0
                elif self.momentum[0] < 0:
                    self.collisions['left'] = True
                    self.rect.left = hit.right
                    if self.momentum[0] < 0: self.momentum[0] = 0
        elif axis == 'y':
            hit_list = self.collision_test(block_list)
            for hit in hit_list:
                if self.momentum[1] > 0:
                    self.collisions['bottom'] = True
                    self.rect.bottom = hit.top
                    self.momentum[1] = 1
                    self.jump_info['jump_count'] = self.jump_info['jump_count_max']
                elif self.momentum[1] < 0:
                    self.collisions['top'] = True
                    self.rect.top = hit.bottom



    def collision_test(self, tiles):
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def update_movement(self):
        # Momentum Control-> needs to be updated for y
        # Momentum Regulation
        if self.momentum[0] > self.movement_info['move_speed']:
            self.momentum[0] = self.movement_info['move_speed']
        if self.momentum[0] < -self.movement_info['move_speed']:
            self.momentum[0] = -self.movement_info['move_speed']

        # Speed Down
        if not self.keys['right'] and not self.keys['left']:
            if self.momentum[0] > 0:
                self.momentum[0] -= self.movement_info['friction_coeff']
            if self.momentum[0] < 0:
                self.momentum[0] += self.movement_info['friction_coeff']
        if not self.keys['right'] and not self.keys['left'] and (
                0.10 > self.momentum[0] > -0.10):
            self.momentum[0] = 0

        # Player Movement Control
        if self.keys['right'] and not self.keys['left']:
            self.momentum[0] += self.movement_info['accel']
        if self.keys['left'] and not self.keys['right']:
            self.momentum[0] -= self.movement_info['accel']
        if self.keys['up'] and not self.keys['down']:
            if time.time() > self.jump_info['time_before'] + self.jump_info['jump_timer']:
                if self.jump_info['jump_count'] > 0:
                    self.rect.y -= 1
                    self.jump_info['jump_count'] -= 1
                    if self.jump_info['jump_count'] > 0:
                        #First Jump
                        self.momentum[1] = -self.jump_info['max_jump_speed']
                    else:
                        #Second Jump
                        self.momentum[1] = -self.jump_info['max_jump_speed']
                    self.jump_info['time_before'] = time.time()
                    #print('Jumped', self.jump_count, time.time())
        self.momentum[1] += 0.75  # Gravity
        self.find_hit_zones()
        #print(f"Movement Speed: {self.momentum[0]}")
        #print("----------------")

    def update_collisions(self, block_list):
        # Momentum effect and Collision testing
        self.collisions = {'top': False, 'bottom': False, "right": False, 'left': False}
        dt = time.time() - self.last_time
        dt *= 60
        self.last_time = time.time()

        self.rect.x += self.momentum[0]* dt
        self.axis_collision_test(block_list, 'x')

        self.rect.y += self.momentum[1] * dt
        self.axis_collision_test(block_list, 'y')

        # Set Final Rect
        #print(f"x:{self.rect.x}, y:{self.rect.y}")
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.player_dim[0], self.player_dim[1])
