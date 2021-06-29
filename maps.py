import pygame
import time
from tools import Tools
import random


def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

tools = Tools()

class Map:
    def __init__(self, screen, level_map):
        self.map = load_map(level_map)
        self.tiles = []
        self.dirt_color = (205, 133, 63)
        self.grass_color = (60, 179, 113)
        self.center = [screen.get_width() / 2, screen.get_height() / 2]
        self.build_point = [0, 0]
        self.cam_tolerance = [80, 100]
        self.screen = screen
        self.block_size = screen.get_width() / 20
        self.shake = False
        self.shake_degree = 10
        self.shake_out_timer = 15
        self.after_shake = self.shake_out_timer + 1
        self.shake_out = 0
        self.shake_correction = {
            'build_point': [0, 0],
            'player_coords': [0, 0],
            'center': [0, 0],
            'cam_tolerance': [0, 0],
            'map_bounds': [0, 0, 0, 0]
        }
        self.map_bounds_tolerance = [100, 100, 300, 100]
        self.map_bounds = self.find_cam_bounds()
        self.spawn_locations = self.find_initial_spawns()


    def find_initial_spawns(self):
        spawn_locs = []
        for num_y, layer in enumerate(self.map):
            for num_x, tile in enumerate(layer):
                if tile == "P": 
                    spawn_locs.append((num_x*self.block_size + self.build_point[0], num_y*self.block_size + self.build_point[1]))
        return spawn_locs


    def draw(self, screen, game_map, background_color):
        self.tiles = []
        self.spawn_locations =[]
        screen.fill(background_color)
        for num_y, layer in enumerate(game_map):
            for num_x, tile in enumerate(layer):
                if tile == "2":
                    pygame.draw.rect(screen, self.dirt_color, pygame.Rect((num_x*self.block_size) + self.build_point[0], (num_y*self.block_size) + self.build_point[1], self.block_size, self.block_size))
                    self.tiles.append(pygame.Rect((num_x*self.block_size) + self.build_point[0], (num_y*self.block_size) + self.build_point[1], self.block_size, self.block_size))
                if tile == "1":
                    pygame.draw.rect(screen, self.grass_color, pygame.Rect((num_x*self.block_size) + self.build_point[0], (num_y*self.block_size) + self.build_point[1], self.block_size, self.block_size))
                    self.tiles.append(pygame.Rect((num_x*self.block_size) + self.build_point[0], (num_y*self.block_size) + self.build_point[1], self.block_size, self.block_size))
                if tile == "P":
                    self.spawn_locations.append((num_x*self.block_size + self.build_point[0], num_y*self.block_size + self.build_point[1]))


    def find_cam_bounds(self):
        max_left, max_right, max_top, max_bottom = self.center[0]*2, 0, self.center[1]*2, 0
        
        for num_y, layer in enumerate(self.map):
            for num_x, tile in enumerate(layer):
                if tile == "2":
                    self.tiles.append(("2", pygame.Rect((num_x*self.block_size) + self.build_point[0], (num_y*self.block_size) + self.build_point[1], self.block_size, self.block_size)))
                if tile == "1":
                    self.tiles.append(("1", pygame.Rect((num_x*self.block_size) + self.build_point[0], (num_y*self.block_size) + self.build_point[1], self.block_size, self.block_size)))
                
        for tile in self.tiles:
            tile = tile[1]
            tile_left, tile_right = tile[0], tile[0] + self.block_size
            tile_top, tile_bottom = tile[1], tile[1] + self.block_size
            
            # Find x-axis
            if tile_left < max_left: max_left = tile_left
            if tile_right > max_right: max_right = tile_right
            if tile_top < max_top: max_top = tile_top
            if tile_bottom > max_bottom: max_bottom = tile_bottom
        
        #max_left -= self.map_bounds_tolerance[0]
        #max_right += self.map_bounds_tolerance[1]
        #max_top -= self.map_bounds_tolerance[2]
        #max_bottom += self.map_bounds_tolerance[3]

        return [max_left, max_right, max_top, max_bottom]


    def correct_shake(self, player):
        # Shake x
        player.rect.x -= self.shake_correction['player_coords'][0]
        self.build_point[0] -= self.shake_correction['build_point'][0]
        self.center[0] -= self.shake_correction['center'][0]
        self.cam_tolerance[0] -= self.shake_correction['cam_tolerance'][0]
        self.map_bounds[0] -= self.shake_correction['map_bounds'][0]
        self.map_bounds[1] -= self.shake_correction['map_bounds'][1]
        self.shake_correction['build_point'][0] = 0
        self.shake_correction['player_coords'][0] = 0
        self.shake_correction['center'][0] = 0
        self.shake_correction['cam_tolerance'][0] = 0
        self.shake_correction['map_bounds'][0] = 0
        self.shake_correction['map_bounds'][1] = 0
        # Shake y 
        player.rect.y -= self.shake_correction['player_coords'][1]
        self.build_point[1] -= self.shake_correction['build_point'][1]
        self.center[1] -= self.shake_correction['center'][1]
        self.cam_tolerance[1] -= self.shake_correction['cam_tolerance'][1]
        self.map_bounds[2] -= self.shake_correction['map_bounds'][2]
        self.map_bounds[3] -= self.shake_correction['map_bounds'][3]
        self.shake_correction['build_point'][1] = 0
        self.shake_correction['player_coords'][1] = 0
        self.shake_correction['center'][1] = 0
        self.shake_correction['cam_tolerance'][1] = 0
        self.shake_correction['map_bounds'][2] = 0
        self.shake_correction['map_bounds'][3] = 0


    def do_shake_inner(self, player, shake_degree):
        num_x = random.randint(-shake_degree, shake_degree)
        num_y = random.randint(-shake_degree , shake_degree)
        # Shake x
        player.rect.x += num_x
        self.build_point[0] += num_x
        self.center[0] += num_x
        self.cam_tolerance[0] += num_x
        self.map_bounds[0] += num_x
        self.map_bounds[1] += num_x
        self.shake_correction['build_point'][0] += num_x
        self.shake_correction['player_coords'][0] += num_x
        self.shake_correction['center'][0] += num_x
        self.shake_correction['cam_tolerance'][0] += num_x
        self.shake_correction['map_bounds'][0] += num_x
        self.shake_correction['map_bounds'][1] += num_x
        # Shake y 
        player.rect.y += num_y
        self.build_point[1] += num_y
        self.center[1] += num_y
        self.cam_tolerance[1] += num_y
        self.map_bounds[2] += num_y
        self.map_bounds[3] += num_y
        self.shake_correction['build_point'][1] += num_y
        self.shake_correction['player_coords'][1] += num_y
        self.shake_correction['center'][1] += num_y
        self.shake_correction['cam_tolerance'][1] += num_y
        self.shake_correction['map_bounds'][2] += num_y
        self.shake_correction['map_bounds'][3] += num_y


    def do_shake(self, player, shake_degree):
        if self.shake_out < self.shake_out_timer:
            self.do_shake_inner(player, shake_degree)
            #Iterate self.shake_out
            self.shake_out += 1
        else:
            self.correct_shake(player)
            self.shake_out = 0


    def shake_screen(self, player):
        # Potential Fault, doesn't fully correct shake immediately after shaking has stopped
        # Eventually corrects it's self after enough iterations
        # Incorrect coords by a max of self.shake_degree in either axis
        if self.shake:
            self.after_shake = 0
            self.do_shake(player, self.shake_degree)
        elif self.after_shake < self.shake_out_timer + 1:
            if self.after_shake < self.shake_out_timer:
                self.do_shake(player, self.shake_degree)
            elif self.after_shake == self.shake_out_timer:
                self.correct_shake(player)
            self.after_shake += 1


    def camera_tracking(self, player):
        player_right = player.rect.x > self.center[0] + self.cam_tolerance[0] + player.player_dim[0]
        player_left = player.rect.x < self.center[0] - self.cam_tolerance[0]
        player_top = player.rect.y < self.center[1] - self.cam_tolerance[1]
        player_bottom = player.rect.y > self.center[1] + self.cam_tolerance[1] + player.player_dim[1]
        player_exceed_left = player.rect.x < self.map_bounds[0]
        player_exceed_right = player.rect.x > self.map_bounds[1]
        player_exceed_top = player.rect.y < self.map_bounds[2]
        player_exceed_bottom = player.rect.y > self.map_bounds[3]

        # Cam Tracking x-axis
        if player_exceed_left or player_exceed_right:
            print("exceed right") if player_exceed_right else print("exceed left")
        elif player_right or player_left:
            if player_right:
                diff = player.rect.x - self.center[0] - self.cam_tolerance[0] - player.player_dim[0]
                self.build_point[0] -= diff
                self.map_bounds[0] -= diff
                self.map_bounds[1] -= diff
                player.rect.x = self.center[0] + self.cam_tolerance[0] + player.player_dim[0]
            elif player_left:
                diff = self.center[0] - self.cam_tolerance[0] - player.rect.x
                self.build_point[0] += diff
                self.map_bounds[0] += diff
                self.map_bounds[1] += diff
                player.rect.x = self.center[0] - self.cam_tolerance[0]

        # Cam Tracking y-axis
        if player_exceed_top or player_exceed_bottom:
            print("exceed top") if player_exceed_top else print("exceed bot")
        elif player_top or player_bottom:
            if player_top:
                diff = self.center[1] - self.cam_tolerance[1] - player.rect.y
                self.build_point[1] += diff
                self.map_bounds[2] += diff
                self.map_bounds[3] += diff
                player.rect.y = self.center[1] - self.cam_tolerance[1]
            elif player_bottom:
                diff = player.rect.y - self.center[1] - self.cam_tolerance[1] - player.player_dim[1]
                self.build_point[1] -= diff
                self.map_bounds[2] -= diff
                self.map_bounds[3] -= diff
                player.rect.y = self.center[1] + self.cam_tolerance[1] + player.player_dim[1]


    def update(self, screen, player):
        player.update_movement()
        
        # Check Camera Sway X
        self.camera_tracking(player)
        self.shake_screen(player)

        # Load and  Draw Map
        self.draw(screen, self.map, (180, 180, 200))
        tools.stand_func()

        player.update_collisions(self.tiles)
        player.draw(screen, tools.stand, player.rect.x, player.rect.y)
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0] * 3
        mouse_y = mouse_pos[1] * 3
        pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(mouse_x, mouse_y, 10, 25))
        if player.keys['mouse_right']:
            pygame.draw.line(screen, (0, 0, 0), (player.rect.x + (player.player_dim[0]/2), player.rect.y + (player.player_dim[1]/2)), (mouse_x, mouse_y), 5)
        if player.keys['mouse_left']:
            pygame.draw.line(screen, (255, 255, 255), (player.rect.x + (player.player_dim[0]/2), player.rect.y + (player.player_dim[1]/2)), (mouse_x, mouse_y), 5)



level_1_1 = [
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "1", "1", "1", "1", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["1", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["2", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2", "2", "2", "2", "2"],
    ["2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2"],
    ["2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2"],
    ["2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2"],
    ["2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2"]]
