import pygame
from variable import window_height, window_width


# The class for Player
# It contains setting blocks and player's movements
# Also, It has no parameters
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # variable that contains player image
        self.image = pygame.image.load("charactor1.png").convert_alpha()
        # variable that contains player's size
        self.rect = self.image.get_rect()
        # variable that contains player's movement while player moves
        self.movement = 0
        # variable to check player's movements
        self.movement_flag = True
        # variable to check frames how much they move
        self.movement_count = 0

    # This is a method to make player's movements
    def move_img(self):
        if self.movement_count >= 5:
            self.movement_count -= 5
            if self.movement_flag:
                self.movement += 1
            else:
                self.movement -= 1
            if self.movement >= 2:
                self.movement_flag = False
            elif self.movement <= 0:
                self.movement_flag = True
            match (self.movement):
                case 0:
                    self.image = pygame.image.load("charactor1.png").convert_alpha()
                case 1:
                    self.image = pygame.image.load("charactor2.png").convert_alpha()
                case 2:
                    self.image = pygame.image.load("charactor3.png").convert_alpha()
        else:
            self.movement_count += 1
