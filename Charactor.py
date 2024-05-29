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
