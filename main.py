import pygame
from pygame.locals import QUIT, KEYUP, K_ESCAPE
import sys
import static


def main():
    # 통계에 필요한 값들을 bodys 변수에 저장
    bodys = static.get_statious()
    static.nomalization_statious()
    bodys = static.get_statious()


if __name__ == "__main__":
    main()
