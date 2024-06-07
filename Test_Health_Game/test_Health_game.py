import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import unittest
from Health_Game import (
    static,
    Charactor,
    variable,
    container,
    set_map,
    interface,
    MediaPipe,
    main,
)
import datetime as dt
import json
import pygame


class tests(unittest.TestCase):
    def test_static(self):
        os.remove(sys.path[0] + "\\..\\src\\staticsitc.json")
        body = static.get_statious()
        with open(
            sys.path[0] + "\\..\\src\\staticsitc.json", "w", encoding="utf-8-sig"
        ) as json_file:
            date = dt.datetime(body[0]["year"], body[0]["month"], body[0]["day"])
            date -= dt.timedelta(days=2)
            body[0]["year"] = date.year
            body[0]["month"] = date.month
            body[0]["day"] = date.day
            json.dump(body, json_file, indent=4)
        body = static.get_statious()
        body[0]["Upper_body"] = 30
        static.set_statious(body[0])
        body = static.get_statious()
        static.nomalization_statious()

    def test_character(self):
        pygame.init()
        screen = pygame.display.set_mode((64, 64))
        player = Charactor.Player()
        pygame.display.set_caption("H.G")

        for i in range(1, 30):
            player.move_img()
        player.move(30, 30)
        player.move(1000, 30)
        player.move(-2000, 30)
        player.move(0, -4000)
        player.move(0, 3000)
        enemy = Charactor.Enemy()

        for i in range(1, 300):
            enemy.move_img()
        enemy.move()

    def test_container(self):
        con = container.fight_container()
        container.model_select_container()
        container.static_container()
        container.setting_container()
        con[0].attacked(50)

    def test_set_map(self):
        pygame.init()
        screen = pygame.display.set_mode((64, 64))
        player = Charactor.Player()
        pygame.display.set_caption("H.G")
        set_map.Rock(3, 4)
        set_map.Ground(3, 4)
        background_group = pygame.sprite.Group()
        set_map.set_main_map(background_group)

    def test_interface_main(self):
        pygame.init()
        screen = pygame.display.set_mode(
            (variable.window_height, variable.window_width)
        )
        pygame.display.set_caption("H.G")
        body = static.get_statious()
        Minterface = interface.main_screen(screen, body)
        self.assertEqual(Minterface.return_screen(), "main")
        Minterface.move_interface_flag = True
        Minterface.update()
        self.assertTrue(Minterface.move_interface())
        Minterface.enemy.append(Charactor.Enemy())
        Minterface.draw()
        Minterface.to_x = 1
        Minterface.to_y = 2
        Minterface.draw()
        Minterface.to_x = 0
        Minterface.to_y = 0
        Minterface.draw()
        Minterface.to_x = 0
        Minterface.to_y = 1
        for i in range(1, 70):
            Minterface.update()
        event = pygame.event
        event.type = pygame.KEYDOWN
        event.key = pygame.K_LEFT
        Minterface.handle_event(event)
        event.type = pygame.KEYDOWN
        event.key = pygame.K_RIGHT
        Minterface.handle_event(event)
        event.type = pygame.KEYDOWN
        event.key = pygame.K_DOWN
        Minterface.handle_event(event)
        event.type = pygame.KEYDOWN
        event.key = pygame.K_UP
        Minterface.handle_event(event)
        event.type = pygame.KEYUP
        event.key = pygame.K_UP
        Minterface.handle_event(event)
        event.type = pygame.KEYUP
        event.key = pygame.K_RIGHT
        Minterface.handle_event(event)

    def test_fight_main(self):
        pygame.init()
        screen = pygame.display.set_mode(
            (variable.window_height, variable.window_width)
        )
        pygame.display.set_caption("H.G")
        body = static.get_statious()
        enemy = []
        enemy.append(Charactor.Enemy())
        model = [0]
        Finterface = interface.fight_screen(screen, enemy, model, body, 0)
        Finterface.draw()
        Finterface.fight_container[0].cur_heart = 0
        Finterface.model = MediaPipe.MediaPipe()
        Finterface.select_cout = 2
        Finterface.model.attack_flag = True
        Finterface.update()
        Finterface.select_cout = 3
        Finterface.model.attack_flag = True
        Finterface.update()
        self.assertEqual(Finterface.return_screen(), "fight")
        self.assertTrue(Finterface.move_interface())
        event = pygame.event
        event.type = pygame.KEYDOWN
        event.key = pygame.K_LEFT
        Finterface.handle_event(event)
        event.type = pygame.KEYDOWN
        event.key = pygame.K_RIGHT
        Finterface.handle_event(event)
        event.type = pygame.KEYUP
        event.key = pygame.K_RETURN
        Finterface.model_count[0] = 0
        Finterface.handle_event(event)
        Finterface.model_count[0] = 1
        Finterface.handle_event(event)

    def test_setting_main(self):
        pygame.init()
        screen = pygame.display.set_mode(
            (variable.window_height, variable.window_width)
        )
        pygame.display.set_caption("H.G")
        body = static.get_statious()
        Sinterface = interface.setting_screen(screen, body[len(body) - 1])
        self.assertEqual(Sinterface.return_screen(), "setting")
        Sinterface.move_interface_flag = True
        self.assertTrue(Sinterface.move_interface())
        Sinterface.select_cout = -1
        Sinterface.update()
        Sinterface.select_cout = 4
        Sinterface.update()
        Sinterface.draw()
        event = pygame.event
        event.type = pygame.KEYDOWN
        event.key = pygame.K_DOWN
        Sinterface.handle_event(event)
        event.type = pygame.KEYDOWN
        event.key = pygame.K_UP
        Sinterface.handle_event(event)
        event.type = pygame.KEYUP
        event.key = pygame.K_RETURN
        Sinterface.select_cout = 0
        with self.assertRaises(SystemExit) as cm:
            Sinterface.handle_event(event)
        self.assertEqual(cm.exception.code, 1)
        Sinterface.select_cout = 1
        Sinterface.handle_event(event)
        Sinterface.select_cout = 2
        Sinterface.handle_event(event)
        Sinterface.select_cout = 3
        Sinterface.handle_event(event)

    def test_model_main(self):
        pygame.init()
        screen = pygame.display.set_mode(
            (variable.window_height, variable.window_width)
        )
        pygame.display.set_caption("H.G")
        model = [0]
        Minterface = interface.model_select_screen(screen, model)
        Minterface.select_cout = -1
        Minterface.update()
        Minterface.select_cout = 4
        Minterface.update()
        self.assertEqual(Minterface.return_screen(), "model_select")
        Minterface.move_interface_flag = True
        self.assertTrue(Minterface.move_interface())
        Minterface.draw()
        event = pygame.event
        event.type = pygame.KEYDOWN
        event.key = pygame.K_DOWN
        Minterface.handle_event(event)
        event.type = pygame.KEYDOWN
        event.key = pygame.K_UP
        Minterface.handle_event(event)
        event.type = pygame.KEYUP
        event.key = pygame.K_RETURN
        Minterface.select_cout = 0
        Minterface.handle_event(event)
        Minterface.select_cout = 1
        Minterface.handle_event(event)

    def test_statistics_screen(self):
        pygame.init()
        screen = pygame.display.set_mode(
            (variable.window_height, variable.window_width)
        )
        pygame.display.set_caption("H.G")
        body = static.get_statious()
        Sinterface = interface.statistics_screen(screen, body)
        self.assertEqual(Sinterface.return_screen(), "Static")
        Sinterface.move_interface_flag = True
        self.assertTrue(Sinterface.move_interface())
        Sinterface.select_cout = -1
        Sinterface.update()
        Sinterface.select_cout = 4
        Sinterface.update()
        Sinterface.draw()
        event = pygame.event
        event.type = pygame.KEYDOWN
        event.key = pygame.K_LEFT
        Sinterface.handle_event(event)
        event.type = pygame.KEYDOWN
        event.key = pygame.K_RIGHT
        Sinterface.handle_event(event)
        event.type = pygame.KEYUP
        event.key = pygame.K_RETURN
        Sinterface.handle_event(event)
        Sinterface.select_cout = 0
        Sinterface.screen_count = 2
        Sinterface.handle_event(event)

    # def test_main(self):
    #     with self.assertRaises(SystemExit) as cm:
    #         main.main()
    #     self.assertEqual(cm.exception.code, 1)
