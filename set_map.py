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

        self.image = pygame.image.load("tile_rock.png").convert_alpha()
        # create block for tile position
        self.rect = self.image.get_rect()
        # Add rock tile position
        self.rect.x = self.grid_x
        self.rect.y = self.grid_y


# This is class for background tiles
# This tile looks like grass
class Ground(pygame.sprite.Sprite):
    def __init__(self, col, row):
        pygame.sprite.Sprite.__init__(self)
        # TILESIZE is 64px*64px
        self.grid_x = row * TILESIZE
        self.grid_y = col * TILESIZE
        # variable for load image
        self.image = pygame.image.load("tile_ground.png").convert_alpha()
        self.rect = self.image.get_rect()
        # Add rock tile position
        self.rect.x = self.grid_x
        self.rect.y = self.grid_y


# This mothod is for setting map
# Game reads map.txt and add tiles into background
def set_main_map(background_group):
    map_file = "map.txt"
    map_data = []

    with open(map_file, "r") as file:
        for line in file:
            map_data.append(line.strip("\n").split(" "))
    for col in range(0, len(map_data)):
        for row in range(0, len(map_data[col])):
            if map_data[col][row] == "r":
                rock = Rock(col, row)
                background_group.add(rock)
            elif map_data[col][row] == "g":
                ground = Ground(col, row)
                background_group.add(ground)
    return map_data
