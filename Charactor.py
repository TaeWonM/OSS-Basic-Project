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
        # variable that contains player's hit box
        self.rect = self.image.get_rect()
        # variable that contains player's movement while player moves
        self.movement = 0
        # variable to check player's movements
        self.movement_flag = True
        # variable to check frames how much they move
        self.movement_count = 0

    # This is a method to make player's movements dynamically
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

    # This is a method to make player's movements with player's hit box
    def move(self, to_x, to_y):
        self.rect.x += to_x
        self.rect.y += to_y
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > window_width - self.rect.size[0]:
            self.rect.x = window_width - self.rect.size[0]

        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > window_height - self.rect.size[1]:
            self.rect.y = window_height - self.rect.size[1]


# The class for Enemy
# It contains setting blocks and Enemy's movements
# Also, It has no parameters
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # variable that contains enemy image
        self.image = pygame.image.load("Enemy_up-1.png").convert_alpha()
        # variable that contains enemy's hit box
        self.rect = self.image.get_rect()
        # variable that contains enemy's movement while player moves
        self.movement = 0
        # variable to check frames how much they move
        self.movement_count = 0
        # variable to check enemy's movements
        self.movement_flag = True

    # This is a method to make enemy's movements dynamically
    def move_img(self):
        if self.movement_count >= 5:
            self.movement_count -= 5
            if self.movement_flag:
                match (self.movement):
                    case 0:
                        self.image = pygame.image.load("Enemy_up-1.png").convert_alpha()
                    case 1:
                        self.image = pygame.image.load("Enemy_up-2.png").convert_alpha()
                    case 2:
                        self.image = pygame.image.load("Enemy_up-3.png").convert_alpha()
                self.movement += 1
            else:
                match (self.movement):
                    case 0:
                        self.image = pygame.image.load(
                            "Enemy_down-1.png"
                        ).convert_alpha()
                    case 1:
                        self.image = pygame.image.load(
                            "Enemy_down-2.png"
                        ).convert_alpha()
                    case 2:
                        self.image = pygame.image.load(
                            "Enemy_down-3.png"
                        ).convert_alpha()
                self.movement -= 1
            if self.movement >= 2:
                self.movement_flag = False
            elif self.movement <= 0:
                self.movement_flag = True
        else:
            self.movement_count += 1

    # This is a method to make for match player class
    def move(self):
        pass
