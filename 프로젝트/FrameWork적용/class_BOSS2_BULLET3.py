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
RUN_SPEED_KMPH = 0.05
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

DEGREE_PER_TIME = 32*PI

class BOSS2_BULLET3:
    image = None

    def __init__(self,x = WINX//2,y=WINY//2,degree = 0):
        if BOSS2_BULLET3.image == None:
            BOSS2_BULLET3.image = load_image('Enemy.png')
        self.x,self.y = x,y
        self.dir = 1
        self.degree = degree
        self.timer = 0
        self.cur_time = 0


    def draw(self):
        BOSS2_BULLET3.image.rotate_draw(math.radians(self.degree), self.x, self.y, SIZE, SIZE)


    def update(self):
        self.timer += get_time() - self.cur_time
        self.cur_time = get_time()

        if self.timer >= 5:
            self.dir *=-1
            self.timer = 0

        self.degree += self.dir*DEGREE_PER_TIME*game_framework.frame_time

        self.x = main_state2.Boss2.x + SIZE*2*math.cos(math.radians(self.degree))
        self.y = main_state2.Boss2.y + SIZE*2*math.sin(math.radians(self.degree))


