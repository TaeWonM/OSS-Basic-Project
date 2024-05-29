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
