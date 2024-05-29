import pygame
from variable import window_height, window_width
from pygame.locals import KEYUP
import Charactor
import set_map
import container
import sys
import threading
import MediaPipe
import MoveNet
import static
import datetime as dt
import random


# The class for main interface
# It contains Enemys and players
# Also, It has parameters screen, bodys
# Screen is a pygame object, and it is a object to display game
# body is a dictionary it contains date, month, year and record
class main_screen:
    def __init__(self, screen, bodys):
        self.screen = screen
        # variables to make movments
        self.to_x = 0
        self.to_y = 0
        # variable that contains Player's movement
        self.player = Charactor.Player()
        self.background_group = pygame.sprite.Group()
        # variable to move interface
        self.move_interface_flag = False
        # variable that contains exercise recodes
        self.bodys = bodys
        # Setting players inital position
        self.player.rect.x = (window_width / 2) - (self.player.rect.size[0] / 2)
        self.player.rect.y = window_height - self.player.rect.size[1]
        # variable to count the numbers of enemys
        self.enemy_index = 0
        self.enemy = []
        # variable that contains map_data
        self.map_data = set_map.set_main_map(self.background_group)

    # This is a method to handle events
    # In this method, Catch direction key to implement player's movments
    # It has parameters event
    # Event is a pygame object, too. It contains events while game runs.
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.to_x -= 2
            if event.key == pygame.K_RIGHT:
                self.to_x += 2
            if event.key == pygame.K_UP:
                self.to_y -= 2
            if event.key == pygame.K_DOWN:
                self.to_y += 2
        if event.type == KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.to_x = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.to_y = 0

    # This method handles variables by many situations

    def update(self):
        # This is the part of movement for changing player's images while player are moving
        if self.to_x != 0 or self.to_y != 0:
            self.player.move_img()
            self.player.move(self.to_x, self.to_y)
        # This is the part of checking crash between player and enemy
        for i in range(0, len(self.enemy)):
            self.enemy[i].move_img()
            if self.player.rect.colliderect(self.enemy[i].rect):
                self.move_interface_flag = True
                self.enemy_index = i
        # This is the part of adding enemys if all enemys are eliminated
        if len(self.enemy) == 0:
            num = random.randint(4, 21)
            for i in range(0, num):
                enemy = Charactor.Enemy()
                enemy.rect.x = random.randint(0, 988)
                enemy.rect.y = random.randint(0, 988)
                self.enemy.append(enemy)

    # This is method to draw background and other characters
    def draw(self):
        self.background_group.add(self.player)
        for i in range(0, len(self.enemy)):
            self.background_group.add(self.enemy[i])
        self.background_group.draw(self.screen)

    # This is method to return move_interface_flag variable
    def move_interface(self):
        return self.move_interface_flag

    # This is method to find what current screen is in
    def return_screen(self):
        return "main"


# The class for fight interface
# It contains Enemys and players
# Also, It has parameters screen, bodys, enemy, model_count, bodys, enemy_index
# Screen is a pygame object, and it is a object to display game
# body is a dictionary it contains date, month, year and record
# model_count is a important variable to find what model have chosen
class fight_screen:
    def __init__(self, screen, enemy, model_count, bodys, enemy_index):
        self.screen = screen
        # variable that contains ground image
        self.fight_ground_image = pygame.image.load("grass_fight_ground.png")
        # variable that contains selection image while fight
        self.fight_interface = pygame.image.load("fight_selection.png")
        # variable that contains what enemy the player was crashed
        self.enemy_index = enemy_index
        # variable that contains all enemys
        self.enemys = enemy
        self.enemy = enemy[enemy_index]

        self.move_interface_flag = False
        # variable for check what button have chosen
        self.select_cout = 2
        # variable that contains fight blocks
        # 0 : enemy heart bar, 1 : player heart bar
        # 2, 3 : check buttons
        self.fight_container = container.fight_container()
        # self.fight_container[0].attacked(90)
        # This contains font style
        self.font = pygame.font.SysFont(None, 40)
        self.model_count = model_count
        # Thread variable
        self.Thread1 = None
        # model class variable
        self.model = None
        self.bodys = bodys

    # This is a method to handle events
    # In this method, Catch direction key to implement pose detection models
    def handle_event(self, event):
        # if statement to detect model changes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.select_cout -= 1
            if event.key == pygame.K_RIGHT:
                self.select_cout += 1
        # if statement to run pose detection models
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                if self.Thread1 != None and self.Thread1.is_alive():
                    pass
                else:
                    if self.model_count[0] == 0:
                        self.model = MediaPipe.MediaPipe()
                        self.Thread1 = threading.Thread(
                            target=self.model.run,
                            args=[self.select_cout - 2],
                            daemon=True,
                        )
                        self.Thread1.start()
                    else:
                        self.model = MoveNet.Movenet()
                        self.Thread1 = threading.Thread(
                            target=self.model.run,
                            args=[self.select_cout - 2],
                            daemon=True,
                        )
                        self.Thread1.start()

    # This method handles variables by many situations
    def update(self):
        # In this statement, Catch player's attacks. and add into bodys variable
        try:
            if self.model.attack_flag:
                self.model.attack_flag = False
                self.fight_container[0].attacked(5)
                if self.select_cout == 2:
                    self.bodys["Upper_body"] += 3
                elif self.select_cout == 3:
                    self.bodys["Lower_body"] += 3
        except:
            pass
        # In this if statement, find enemy is dead and return to main interface
        if self.fight_container[0].cur_heart <= 0:
            self.move_interface_flag = True
            self.model.kill_thread = True
        # In this if statement, adjust the wrong values
        if self.select_cout <= 2:
            self.select_cout = 2
        elif self.select_cout >= 3:
            self.select_cout = 3
        self.enemy.move_img()
        pass

    # This is method to draw interface objects and strings
    def draw(self):
        # Draw fight_ground_image
        self.screen.blit(self.fight_ground_image, [0, 0])
        # Draw fight_interface
        self.screen.blit(self.fight_interface, [0, 0])
        # Draw enemy image
        self.screen.blit(
            self.enemy.image,
            [
                (window_width / 2) - (self.enemy.rect.size[0] / 2),
                (window_height / 2) - (self.enemy.rect.size[1] / 2) - 45,
            ],
        )
        # Draw heart blocks
        for i in range(0, 2):
            pygame.draw.rect(
                self.screen, (255, 0, 0), self.fight_container[i].left_heart
            )
            pygame.draw.rect(
                self.screen, (0, 0, 0), self.fight_container[i].attacked_heart
            )
        # Draw selection blocks
        for i in range(2, 4):
            if self.select_cout == i:
                pygame.draw.rect(self.screen, (255, 0, 0), self.fight_container[i])
            else:
                pygame.draw.rect(self.screen, (0, 0, 0), self.fight_container[i])
        # Draw heart status
        self.screen.blit(
            self.font.render(
                str(self.fight_container[1].cur_heart)
                + "/"
                + str(self.fight_container[1].max_heart),
                False,
                (0, 0, 0),
            ),
            [
                self.fight_container[1].left + self.fight_container[1].width + 5,
                self.fight_container[1].top + 2,
            ],
        )
        self.screen.blit(
            self.font.render(
                str(self.fight_container[0].cur_heart)
                + "/"
                + str(self.fight_container[0].max_heart),
                False,
                (0, 0, 0),
            ),
            [
                self.fight_container[0].left + self.fight_container[0].width + 5,
                self.fight_container[0].top - 1,
            ],
        )

    # This is method to draw background and other characters
    def move_interface(self):
        return self.move_interface_flag

    # This is method to find what current screen is in
    def return_screen(self):
        return "fight"


# The class for setting interface
# It contains setting blocks
# Also, It has parameters screen, bodys
class setting_screen:
    def __init__(self, screen, bodys):
        self.screen = screen
        # variable that contains setting image
        self.image = pygame.image.load("Setting.png")
        # variable for check what button have chosen
        self.select_cout = 0
        # variable that contains selection blocks
        self.select_button = container.setting_container()
        self.move_interface_flag = False
        # variable that contains what screen to move
        self.move_screen = ""
        self.bodys = bodys

    # This is a method to handle events
    # In this method, Catch direction key to change buttons
    def handle_event(self, event):
        # if statement to detect change buttons
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.select_cout -= 1
            if event.key == pygame.K_DOWN:
                self.select_cout += 1
        # if statement to detect Enter key to move other interface
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                match (self.select_cout):
                    case 0:
                        static.set_statious(self.bodys)
                        pygame.quit()
                        sys.exit()
                    case 1:
                        self.move_screen = "Static"
                        self.move_interface_flag = True
                    case 2:
                        self.move_screen = "Model"
                        self.move_interface_flag = True
                    case 3:
                        self.move_screen = "Return"
                        self.move_interface_flag = True

    # This method handles variables by many situations
    def update(self):
        # In this if statement, adjust the wrong values
        if self.select_cout <= 0:
            self.select_cout = 0
        elif self.select_cout >= 3:
            self.select_cout = 3
        pass

    # This is method to draw interface objects
    def draw(self):
        self.screen.blit(self.image, [0, 0])
        for i in range(0, 4):
            if i == self.select_cout:
                pygame.draw.rect(self.screen, (255, 0, 0), self.select_button[i])
            else:
                pygame.draw.rect(self.screen, (0, 0, 0), self.select_button[i])
        self.font = pygame.font.SysFont(None, 20)

    # This is method to draw background and other characters
    def move_interface(self):
        return self.move_interface_flag

    # This is method to find what current screen is in
    def return_screen(self):
        return "setting"


# The class for model select interface
# It contains setting blocks
# Also, It has parameters screen, bodys, model_count
class model_select_screen:
    def __init__(self, screen, model_count):
        self.screen = screen
        # variable that contains model select image
        self.image = pygame.image.load("change_model.png")
        # variable that contains what model have chosen before
        self.select_cout = model_count[0]
        self.model_count = model_count
        # variable that contains selection blocks
        self.select_button = container.model_select_container()
        self.move_interface_flag = False
        # variable that contains model's name
        self.model = ["Mediapipe", "Movenet"]
        # This contains font style
        self.font = pygame.font.SysFont(None, 75)

    # This is a method to handle events
    # In this method, Catch direction key to change buttons
    def handle_event(self, event):
        # if statement to detect change selections
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.select_cout -= 1
            if event.key == pygame.K_DOWN:
                self.select_cout += 1
        # if statement to detect Enter key to change model variable
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                match (self.select_cout):
                    case 0:
                        self.model_count[0] = 0
                        self.move_interface_flag = True
                    case 1:
                        self.model_count[0] = 1
                        self.move_interface_flag = True

    # This method handles variables by many situations
    def update(self):
        # In this if statement, adjust the wrong values
        if self.select_cout <= 0:
            self.select_cout = 0
        elif self.select_cout >= 1:
            self.select_cout = 1

    # This is method to draw interface objects and strings
    def draw(self):
        self.screen.blit(self.image, [0, 0])
        for i in range(0, 2):
            if i == self.select_cout:
                pygame.draw.rect(self.screen, (255, 0, 0), self.select_button[i])
            else:
                pygame.draw.rect(self.screen, (0, 0, 0), self.select_button[i])
        self.screen.blit(
            self.font.render(
                "Curent Model : " + str(self.model[self.select_cout]), False, (0, 0, 0)
            ),
            [202, 880],
        )

    # This is method to draw background and other characters
    def move_interface(self):
        return self.move_interface_flag

    # This is method to find what current screen is in
    def return_screen(self):
        return "model_select"


# The class for statistics interface
# It contains setting blocks
# Also, It has parameters screen, bodys
class statistics_screen:
    def __init__(self, screen, body):
        # variable that contains exercise recode
        self.bodys = body
        self.screen = screen
        # variable that contains statistics image
        self.img = pygame.image.load("statistics.png")
        self.move_interface_flag = False
        # statement to add updated exercise recode
        static.set_statious(body[len(body) - 1])
        # This contains font style
        self.font = pygame.font.SysFont(None, 60)
        # variable that contains what screen have chosen
        self.screen_count = 0
        # variable that contains what index to start in each screen
        self.max_index = [0]
        # variable that contains blocks to move other screen
        self.select_cout = 0
        # variable that contains selection blocks
        self.container = container.static_container()

    # This is a method to handle events
    # In this method, Catch direction key to change buttons
    def handle_event(self, event):
        # if statement to detect change selections
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.select_cout -= 1
            if event.key == pygame.K_RIGHT:
                self.select_cout += 1
        # if statement to detect Enter key to change screen
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                match (self.select_cout):
                    case 0:
                        if self.screen_count != 0:
                            self.screen_count -= 1
                    case 1:
                        if self.screen_count + 1 < len(self.max_index):
                            self.screen_count += 1

    # This method handles variables by many situations
    def update(self):
        # In this if statement, adjust the wrong values
        if self.select_cout < 0:
            self.select_cout = 0
        elif self.select_cout > 1:
            self.select_cout = 1

    # This is method to draw interface objects and strings
    def draw(self):
        self.screen.blit(self.img, (0, 0))
        for i in range(0, 2):
            if i == self.select_cout:
                pygame.draw.rect(self.screen, (255, 0, 0), self.container[i])
            else:
                pygame.draw.rect(self.screen, (0, 0, 0), self.container[i])
        i = self.max_index[self.screen_count]
        line = 0
        while i < len(self.bodys) and line <= 5:
            k = dt.datetime(
                self.bodys[i]["year"], self.bodys[i]["month"], self.bodys[i]["day"]
            )
            rect = pygame.Rect(200 + line * 130, 180 + 82 * k.weekday(), 24, 24)
            pygame.draw.rect(
                self.screen,
                (
                    (
                        self.bodys[i]["Upper_body"]
                        if self.bodys[i]["Upper_body"] <= 255
                        else 255
                    ),
                    (
                        self.bodys[i]["Lower_body"]
                        if self.bodys[i]["Lower_body"] <= 255
                        else 255
                    ),
                    0,
                ),
                rect,
            )
            i += 1
            if k.weekday() == 6:
                line += 1
            k += dt.timedelta(days=1)
        if i < len(self.bodys):
            if self.screen_count + 1 == len(self.max_index):
                self.max_index.append(i)
        mx, my = pygame.mouse.get_pos()
        i = self.max_index[self.screen_count]
        index = None
        line = 0
        while i < len(self.bodys) and line <= 7:
            k = dt.datetime(
                self.bodys[i]["year"], self.bodys[i]["month"], self.bodys[i]["day"]
            )
            if (
                mx >= 200 + line * 130
                and mx <= 224 + line * 130
                and my >= 180 + 82 * k.weekday()
                and my <= 204 + 82 * k.weekday()
            ):
                index = self.bodys[i]
                break
            i += 1
            if k.weekday() == 6:
                line += 1
            k += dt.timedelta(days=1)
        if index != None:
            self.screen.blit(
                self.font.render(
                    str(index["year"])
                    + "/"
                    + str(index["month"])
                    + "/"
                    + str(index["day"])
                    + " : "
                    + "Upper body = "
                    + str(index["Upper_body"])
                    + ", Lower body = "
                    + str(index["Lower_body"]),
                    False,
                    (0, 0, 0),
                ),
                (60, 30),
            )
        else:
            self.screen.blit(
                self.font.render("", True, (0, 0, 0)),
                (30, 30),
            )
