import pygame
from variable import TILESIZE


# This is class for background tiles
# This tile looks like rock
class Rock(pygame.sprite.Sprite):
    def __init__(self, col, row):
        pygame.sprite.Sprite.__init__(self)
        # TILESIZE is 64px*64px
        self.grid_x = row * TILESIZE
        self.grid_y = col * TILESIZE
        # variable for load image
        self.image = pygame.image.load("tile_rock.png").convert_alpha()
        # create block for tile position
        self.rect = self.image.get_rect()
        # Add rock tile position
        self.rect.x = self.grid_x
        self.rect.y = self.grid_y
