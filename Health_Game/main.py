import pygame
from pygame.locals import QUIT, KEYUP, K_ESCAPE
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Health_Game.variable import window_height, window_width
from Health_Game import interface
from Health_Game import static


def main():
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
                sys.exit(1)

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
        if curent_screen.move_interface():
            match (curent_screen.return_screen()):
                case "setting":
                    match (curent_screen.move_screen):
                        case "Static":
                            screen_stack.append(curent_screen)
                            curent_screen = interface.statistics_screen(screen, bodys)
                        case "Return":
                            curent_screen = screen_stack.pop()
                        case "Model":
                            screen_stack.append(curent_screen)
                            curent_screen = interface.model_select_screen(
                                screen, model_count
                            )
                case "main":
                    screen_stack.append(curent_screen)
                    curent_screen = interface.fight_screen(
                        screen,
                        curent_screen.enemy,
                        model_count,
                        body,
                        curent_screen.enemy_index,
                    )
                case "fight":
                    enemy_index = curent_screen.enemy_index
                    curent_screen = screen_stack.pop()
                    curent_screen.move_interface_flag = False
                    curent_screen.enemy[enemy_index].kill()
                    curent_screen.enemy.remove(curent_screen.enemy[enemy_index])
                case "model_select":
                    curent_screen = screen_stack.pop()
                    curent_screen.move_interface_flag = False
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
