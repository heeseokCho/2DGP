from pico2d import*
import game_world
import main_state_bonus

from class_ENEMY import ENEMY
from class_ITEM import ITEM
from class_LINK import LINK

import random
WINX,WINY = 1600, 1000
PI = 3.141592
SIZE = 64

LEFT_TOP,LEFT,LEFT_BOTTOM,BOTTOM,\
RIGHT_BOTTOM,RIGHT,RIGHT_TOP,TOP = range(8)

next_state_table ={}

class RunState:
    @staticmethod
    def enter(Stage0,event):
        Stage0.timer = 0
        Stage0.clear_timer = 0
        Stage0.cur_time = get_time()

    @staticmethod
    def exit(Stage0,event):
        pass

    @staticmethod
    def do(Stage0):
        if main_state_bonus.Link.collide_able:
            Stage0.timer += get_time() - Stage0.cur_time

            Stage0.clear_timer += get_time() - Stage0.cur_time

            Stage0.cur_time = get_time()

        if 0< Stage0.timer % 1<0.1:
            Stage0.create_enemy(random.randint(0,1))

        if Stage0.timer >=2:
            Stage0.create_item()
            Stage0.timer = 0

        if Stage0.clear_timer >= 20:
            if LINK.cur_stage == 0:
                LINK.cur_stage = 1
                Stage0.clear_timer = 0
            elif LINK.cur_stage == 2:
                LINK.cur_stage = 3
                Stage0.clear_timer = 0





    @staticmethod
    def draw(STAGE0):
        pass


class STAGE0:
    enemy = []
    item = []

    def __init__(self):
        self.image = load_image('Boss1_plant.png')
        self.event_que = []
        self.cur_time = 0
        self.timer = 0

        self.clear_timer = 0

        self.cur_state = RunState
        self.cur_state.enter(self, None)

    #아이템
    def create_item(self):
        Item = ITEM()
        STAGE0.item.append(Item)
        game_world.add_object(Item,1)

    #적
    def create_enemy(self,pattern =0):
        Enemy = None
        if pattern == 0:
            for i in range(8):
                Enemy = ENEMY(i)
        elif pattern == 1:
            direction = random.randint(0, 7)
            for i in range(8):
                Enemy = ENEMY(direction)

        STAGE0.enemy.append(Enemy)

        game_world.add_object(Enemy,1)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        pass