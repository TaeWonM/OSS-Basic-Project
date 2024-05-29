import pygame
from pygame.locals import QUIT, KEYUP, K_ESCAPE
import sys
from variable import window_height, window_width
import interface
import static


def main():
    # 통계에 필요한 값들을 bodys 변수에 저장
    bodys = static.get_statious()
    static.nomalization_statious()
    bodys = static.get_statious()
    body = bodys[len(bodys) - 1]
    static.nomalization_statious()
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("H.G")
    screen_stack = []
    # to select models // 0 = Mediapipe // 1 = movenet
    model_count = [0]
    clock = pygame.time.Clock()
    curent_screen = interface.main_screen(screen, body)
    screen_stack.append(curent_screen)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                static.set_statious(body)
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(60)
        if event.type == KEYUP:
            if (
                event.key == K_ESCAPE
                and curent_screen.return_screen() != "setting"
                and curent_screen.return_screen() != "model_select"
            ):
                if curent_screen.return_screen() == "Static":
                    curent_screen = screen_stack.pop()
                    curent_screen.move_interface_flag = False
                else:
                    screen_stack.append(curent_screen)
                    curent_screen = interface.setting_screen(screen, body)
                curent_screen.handle_event(event)
        curent_screen.update()
        curent_screen.draw()


if __name__ == "__main__":
    main()
