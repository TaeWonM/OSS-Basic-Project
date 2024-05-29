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
        # variable that contains Player's movement
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

    # This method handles variables by many situations

    def update(self):
        # This is the part of movement for changing player's images while player are moving
        if self.to_x != 0 or self.to_y != 0:
            self.player.move_img()
            self.player.move(self.to_x, self.to_y)
        # This is the part of checking crash between player and enemy
        for i in range(0, len(self.enemy)):
            self.enemy[i].move_img()
            if self.player.rect.colliderect(self.enemy[i].rect):
                self.move_interface_flag = True
                self.enemy_index = i
        # This is the part of adding enemys if all enemys are eliminated
        if len(self.enemy) == 0:
            num = random.randint(4, 21)
            for i in range(0, num):
                enemy = Charactor.Enemy()
                enemy.rect.x = random.randint(0, 988)
                enemy.rect.y = random.randint(0, 988)
                self.enemy.append(enemy)

    # This is method to draw background and other characters
    def draw(self):
        self.background_group.add(self.player)
        for i in range(0, len(self.enemy)):
            self.background_group.add(self.enemy[i])
        self.background_group.draw(self.screen)

    # This is method to return move_interface_flag variable
    def move_interface(self):
        return self.move_interface_flag

    # This is method to find what current screnn is in
    def return_screen(self):
        return "main"


# The class for main interface
# It contains Enemys and players
# Also, It has parameters screen, bodys, enemy, model_count, bodys, enemy_index
# Screen is a pygame object, and it is a object to display game
# body is a dictionary it contains date, month, year and record
# model_count is a important variable to find what model have chosen
class fight_screen:
    def __init__(self, screen, enemy, model_count, bodys, enemy_index):
        self.screen = screen
        # variable that contains ground image
        self.fight_ground_image = pygame.image.load("grass_fight_ground.png")
        # variable that contains selection image while fight
        self.fight_interface = pygame.image.load("fight_selection.png")
        # variable that contains what enemy the player was crashed
        self.enemy_index = enemy_index
        # variable that contains all enemys
        self.enemys = enemy
        self.enemy = enemy[enemy_index]

        self.move_interface_flag = False
        # variable for check what button have chosen
        self.select_cout = 2
        # variable that contains fight blocks
        # 0 : enemy heart bar, 1 : player heart bar
        # 2, 3 : check buttons
        self.fight_container = container.fight_container()
        # self.fight_container[0].attacked(90)
        # This contains font style
        self.font = pygame.font.SysFont(None, 40)
        self.model_count = model_count
        # Thread variable
        self.Thread1 = None
        # model class variable
        self.model = None
        self.bodys = bodys
