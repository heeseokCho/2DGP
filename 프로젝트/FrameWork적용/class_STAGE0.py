import game_framework
from pico2d import*
import game_world

from class_BOSS1_BULLET1 import BOSS1_BULLET1
from class_BOSS1_BULLET2 import BOSS1_BULLET2

import math
import random
WINX,WINY = 1600, 1000
PI = 3.141592
SIZE = 64

LEFT_TOP,LEFT,LEFT_BOTTOM,BOTTOM,\
RIGHT_BOTTOM,RIGHT,RIGHT_TOP,TOP = range(8)

# Boss1 Run Speed
PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

DEGREE_PER_TIME = PI

# Boss1 Action Speed
TIME_PER_ACTION = 3
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
        Boss1.frame = (Boss1.frame +FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time)%5

        Boss1.timer += get_time() - Boss1.cur_time
        Boss1.cur_time = get_time()

        if Boss1.timer >=5:
            Boss1.shoot_bullet2()
            Boss1.shoot_bullet1()
            Boss1.timer = 0

    @staticmethod
    def draw(Boss1):
        Boss1.image.clip_draw(int(Boss1.frame)*SIZE*3,0,SIZE*3,SIZE*3,Boss1.x,Boss1.y)


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
        bullet1 = BOSS1_BULLET1()
        game_world.add_object(bullet1,1)

    #8방
    def shoot_bullet2(self):
        bullet2 = [BOSS1_BULLET2(self.x,self.y,i) for i in range(8)]

        for o in bullet2:
            game_world.add_object(o,1)

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