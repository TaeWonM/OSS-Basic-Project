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
