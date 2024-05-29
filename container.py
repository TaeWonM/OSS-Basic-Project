import pygame


# method that make setting blocks list
def setting_container():
    container = []
    container.append(pygame.Rect(280, 340, 32, 32))
    container.append(pygame.Rect(280, 510, 32, 32))
    container.append(pygame.Rect(280, 686, 32, 32))
    container.append(pygame.Rect(280, 858, 32, 32))
    return container


# The class for heart
# It contains Enemy's and player's heart
# Also, It has parameters left, top, width, height, max_
class heart:
    def __init__(self, left, top, width, height, max_):
        # variable to make left margin
        self.left = left
        # variable that contains how big heart bar is
        self.width = width
        # variable to make top margin
        self.top = top
        # variable to make left heart block
        self.left_heart = pygame.Rect(left, top, width, height)
        # variable to make attacked heart block
        self.attacked_heart = pygame.Rect(left + width, top, 0, height)
        # variable that contains how much heart they have
        self.max_heart = max_
        self.cur_heart = max_

    # method that adjusts heart block when attacked
    def attacked(self, damage):
        self.cur_heart -= damage
        self.left_heart.width = (self.cur_heart / self.max_heart) * self.width
        self.attacked_heart.width = (1 - self.cur_heart / self.max_heart) * self.width
        self.attacked_heart.left = (
            self.left + (self.cur_heart / self.max_heart) * self.width
        )


# method that make fight blocks list
def fight_container():
    container = []
    # 0,1:enemy_heart_bar 2,3: player_heart_bar 4,5:sports select
    enemy_heart_bar = heart(412, 360, 200, 16, 100)
    player_heart_bar = heart(200, 700, 540, 26, 100)
    container.append(enemy_heart_bar)
    container.append(player_heart_bar)

    container.append(pygame.Rect(120, 830, 32, 32))
    container.append(pygame.Rect(580, 830, 32, 32))
    return container


# method that make model select blocks list
def model_select_container():
    container = []
    container.append(pygame.Rect(270, 422, 32, 32))
    container.append(pygame.Rect(270, 724, 32, 32))
    return container


# method that make screen select blocks list
def static_container():
    container = []
    container.append(pygame.Rect(432, 104, 32, 32))
    container.append(pygame.Rect(584, 104, 32, 32))
    return container
