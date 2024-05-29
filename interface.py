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
# body is a dictionary it contains date, month, year and record
class main_screen:
    def __init__(self, screen, bodys):
        self.screen = screen
        # variables to make movments
        self.to_x = 0
        self.to_y = 0
        # variable to Contains Player's movement
        self.player = Charactor.Player()
        self.background_group = pygame.sprite.Group()
        # variable to move interface
        self.move_interface_flag = False
        # variable that contains exercise recodes
        self.bodys = bodys
        # Setting players inital position
        self.player.rect.x = (window_width / 2) - (self.player.rect.size[0] / 2)
        self.player.rect.y = window_height - self.player.rect.size[1]
        # variable to count the numbers of enemys
        self.enemy_index = 0
        self.enemy = []
        # variable that contains map_data
        self.map_data = set_map.set_main_map(self.background_group)

    # This is a method to handle events
    # In this method, Catch direction key to implement player's movments
    # It has parameters event
    # Event is a pygame object, too. It contains events while game runs.
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.to_x -= 2
            if event.key == pygame.K_RIGHT:
                self.to_x += 2
            if event.key == pygame.K_UP:
                self.to_y -= 2
            if event.key == pygame.K_DOWN:
                self.to_y += 2
        if event.type == KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.to_x = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.to_y = 0
