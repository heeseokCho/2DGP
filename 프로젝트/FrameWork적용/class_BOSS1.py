import game_framework
from pico2d import*
import game_world

import math
import random
WINX,WINY = 1600, 1000
PI = 3.141592

# Boss1 Run Speed
PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

DEGREE_PER_TIME = PI

# Boss1 Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0/TIME_PER_ACTION
FRAMES_PER_ACTION = 8



next_state_table ={}

class RunState:
    @staticmethod
    def enter(Boss1,event):
        Boss1.frame= 0
    
    @staticmethod
    def exit(Boss1,event):
        pass

    @staticmethod
    def do(Boss1):
        pass

    @staticmethod
    def draw(Boss1):
        pass


class BOSS1:

    def __init__(self):
        self.x, self.y = WINX//2, WINY//2
        self.image = load_image('Boss1.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = RunState
        self.cur_state.enter(self, None)
        self.cur_time = 0
        self.degree = 0
        self.timer = 0

    #지뢰
    def shoot_bullet1(self):
        pass

    #8방
    def shoot_bullet2(self):
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