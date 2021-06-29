import pygame
import time
import IPython as ip

class Tools():
    def __init__(self):
        self.before = int(time.time())
        self.counter = 1
        self.stand_counter = 0
        self.stand = 1

    def frame_rate_check(self):
        # Frame Rate Check
        if int(time.time()) == self.before:
            self.counter += 1
        else:
            self.before = int(time.time())
            #print(f"FPS : {self.counter}")
            self.counter = 1

    def stand_func(self):
        self.stand_counter += 1
        if self.stand_counter == 20:
            self.stand += 1
            if self.stand == 4:
                self.stand = 1
            self.stand_counter = 0

    def smooth_change(self, current, last, max_change):
        """
        Limits the changes of a variable to "max_change" per frame
        """
        if abs(current - last) > max_change:
            if current > last:
                current = last + max_change
            else: 
                current = last - max_change
        #print(f"Before: {last}, Current {current} ")
        ip.display.clear_output()
        return current
    
    def mouse_tracking(self):
        mouse_pos = pygame.mouse.get_pos()
        return mouse_pos
        
            