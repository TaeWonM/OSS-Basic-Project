import pygame
from variable import window_height, window_width
from pygame.locals import KEYUP
import Charactor
import set_map
import container
import sys
import threading
import MediaPipe
import MoveNet
import static
import datetime as dt
import random


# The class for main interface
# It contains Enemys and players
# Also, It has parameters screen, bodys
# Screen is a pygame object, and it is a object to display game
# body is a dictionary it contains today's date, month, year and record
class main_screen:
    def __init__(self, screen, bodys):
        self.screen = screen
        self.to_x = 0
        self.to_y = 0
        self.player = Charactor.Player()
        self.background_group = pygame.sprite.Group()
        self.move_interface_flag = False
        self.bodys = bodys
        self.player.rect.x = (window_width / 2) - (self.player.rect.size[0] / 2)
        self.player.rect.y = window_height - self.player.rect.size[1]
        self.enemy_index = 0
        self.enemy = []
        self.map_data = set_map.set_main_map(self.background_group)
