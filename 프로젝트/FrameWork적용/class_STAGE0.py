import game_framework
from pico2d import*
import game_world

from class_ENEMY import ENEMY
from class_ITEM import ITEM

import math
import random
WINX,WINY = 1600, 1000
PI = 3.141592
SIZE = 64

LEFT_TOP,LEFT,LEFT_BOTTOM,BOTTOM,\
RIGHT_BOTTOM,RIGHT,RIGHT_TOP,TOP = range(8)

next_state_table ={}

class RunState:
    @staticmethod
    def enter(STAGE0,event):
        pass

    @staticmethod
    def exit(STAGE0,event):
        pass

    @staticmethod
    def do(STAGE0):
        STAGE0.timer += get_time() - STAGE0.cur_time
        STAGE0.cur_time = get_time()

        if 0< STAGE0.timer % 1<0.1:
            STAGE0.create_enemy(random.randint(0,1))

        if STAGE0.timer >=3:
            STAGE0.create_item()
            STAGE0.timer = 0


    @staticmethod
    def draw(STAGE0):
        pass


class STAGE0:

    def __init__(self):
        self.image = load_image('Boss1.png')
        self.event_que = []
        self.cur_state = RunState
        self.cur_state.enter(self, None)
        self.cur_time = 0
        self.timer = 0

    #아이템
    def create_item(self):
        Item = ITEM()
        game_world.add_object(Item,1)

    #적
    def create_enemy(self,pattern =0):
        Enemy = None
        if pattern == 0:
            for i in range(8):
                Enemy = ENEMY(i)
        elif pattern == 1:
            for i in range(8):
                direction = random.randint(0,7)
                Enemy = ENEMY(direction)

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