import game_framework
from pico2d import*
import game_world

from class_BOSS2_BULLET1 import BOSS2_BULLET1
from class_BOSS2_BULLET2 import BOSS2_BULLET2
from class_CIRCLE import CIRCLE

import math
import random
WINX,WINY = 1600, 1000
PI = 3.141592
SIZE = 64

LEFT_TOP,LEFT,LEFT_BOTTOM,BOTTOM,\
RIGHT_BOTTOM,RIGHT,RIGHT_TOP,TOP = range(8)

# Boss2 Run Speed
PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 1.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

DEGREE_PER_TIME = PI

# Boss2 Action Speed
TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0/TIME_PER_ACTION
FRAMES_PER_ACTION = 8

DEGREE_PER_TIME = PI/12

next_state_table ={}

class RunState:

    @staticmethod
    def enter(Boss2,event):
        Boss2.frame= 0


    @staticmethod
    def exit(Boss2,event):
        pass

    @staticmethod
    def do(Boss2):
        Boss2.frame = (Boss2.frame +FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time)%4

        Boss2.timer += get_time() - Boss2.cur_time
        Boss2.cur_time = get_time()

        if 0 < Boss2.timer % 1 and Boss2.timer % 1 < 0.01:
            Boss2.shoot_bullet1()

        if 0<Boss2.timer %5 and Boss2.timer %5< 0.01:
            Boss2.shoot_bullet1()
            Boss2.shoot_bullet2()

        if Boss2.timer >=20:
            Boss2.dir*=-1
            Boss2.timer = 0

        #Boss2.angle_rotation = math.atan2(Circle.y - Boss2.y, Circle.x - Boss2.x) * Boss2.dir

        #Boss2.angle_revolution += Boss2.dir * 0.02
        #Boss2.x = Circle.x + (Circle.r - SIZE) * math.cos(Boss2.angle_revolution)
        #Boss2.y = Circle.y + (Circle.r - SIZE) * math.sin(Boss2.angle_revolution)

        Boss2.revolution_degree += Boss2.dir * DEGREE_PER_TIME* game_framework.frame_time
        Boss2.rotate_degree = math.atan2(WINY//2 - Boss2.y, WINX//2 - Boss2.x) * Boss2.dir

        Boss2.x = WINX//2 + (380 - SIZE) * math.cos(Boss2.revolution_degree)
        Boss2.y = WINY//2 + (380 - SIZE) * math.sin(Boss2.revolution_degree)


    @staticmethod
    def draw(Boss2):
        Boss2.image.clip_draw(int(Boss2.frame)*SIZE*3,0,SIZE*3,SIZE*3,Boss2.x,Boss2.y)


class BOSS2:

    def __init__(self):
        self.x, self.y = WINX//2, WINY//2
        self.image = load_image('Boss2.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = RunState
        self.cur_state.enter(self, None)
        self.cur_time = 0
        self.rotation_degree = 0
        self.revolution_degree =0
        self.timer = 0

    #Link에게쏘는탄
    def shoot_bullet1(self):
        bullet1 = BOSS2_BULLET1(self.x,self.y)
        game_world.add_object(bullet1,1)

    #8방
    def shoot_bullet2(self):
        bullet2 = [BOSS2_BULLET2(self.x,self.y,i) for i in range(8)]

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