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
    def enter(Boss1,event):
        pass

    @staticmethod
    def exit(Boss1,event):
        pass

    @staticmethod
    def do(Boss1):
        STAGE0.timer += get_time() - Boss1.cur_time
        STAGE0.cur_time = get_time()


        if STAGE0.timer >=5:
            STAGE0.create_item()
            STAGE0.create_enemy()
            STAGE0.timer = 0


    @staticmethod
    def draw(Boss1):
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
        pass

    #적
    def create_enemy(self):
        pass

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