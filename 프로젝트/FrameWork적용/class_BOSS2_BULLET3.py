from pico2d import*
import game_framework
import game_world
import main_state2

import random
import math

WINX,WINY = 1600,1000
SIZE  = 64
PI =3.141592

LEFT_TOP,LEFT,LEFT_BOTTOM,BOTTOM,\
RIGHT_BOTTOM,RIGHT,RIGHT_TOP,TOP = range(8)

PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 5
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

DEGREE_PER_TIME = 24*PI

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0/TIME_PER_ACTION
FRAMES_PER_ACTION = 1

class BOSS2_BULLET3:
    image = None
    frame = 0

    def __init__(self,x = WINX//2,y=WINY//2,degree = 0):
        if BOSS2_BULLET3.image == None:
            BOSS2_BULLET3.image = load_image('Boss2Bullet3.png')

        self.x,self.y = x,y
        self.r = 50
        self.dir_revolution = 1
        self.degree = degree
        self.timer = 0
        self.cur_time = 0
        self.dir = 1
        self.velocity = RUN_SPEED_PPS


    def draw(self):
        BOSS2_BULLET3.image.clip_composite_draw(int(BOSS2_BULLET3.frame) * SIZE//2, 0, SIZE//2, SIZE//2, math.radians(self.dir*self.degree),
                                       'v', self.x, self.y, SIZE, SIZE)

    def update(self):
        BOSS2_BULLET3.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7

        self.timer += get_time() - self.cur_time
        self.cur_time = get_time()

        if self.timer >= 5:
            self.dir_revolution *=-1
            self.dir *= -1
            self.timer = 0

        self.degree += self.dir_revolution*DEGREE_PER_TIME*game_framework.frame_time

        self.x = main_state2.Boss2.x + self.r*math.cos(math.radians(self.degree))
        self.y = main_state2.Boss2.y + self.r*math.sin(math.radians(self.degree))
        self.r = self.r + self.dir*self.velocity*game_framework.frame_time


