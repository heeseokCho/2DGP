from pico2d import*
import game_world
import game_framework
import main_state2

import random
import math

WINX,WINY = 1600,1000
SIZE  = 64
PI = 3.141592

PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

DEGREE_PER_TIME = PI/36

class BOSS2_BULLET1:
    image = None

    def __init__(self,x=0,y=0):
        if BOSS2_BULLET1.image == None:
            BOSS2_BULLET1.image = load_image('Boss2_Bullet.png')

        self.startX,self.startY = x,y
        self.endX,self.endY=main_state2.Link.x,main_state2.Link.y
        self.x,self.y =x,y
        self.velocity = RUN_SPEED_PPS
        self.bullet_rotate_degree = 0
        self.t = 0

        if random.randint(0,1) == 0:
            self.bullet_rotate_dir = -1
        else:
            self.bullet_rotate_dir = 1



    def draw(self):
        BOSS2_BULLET1.image.rotate_draw(math.radians(self.bullet_rotate_degree), self.x, self.y, SIZE / 2, SIZE / 2)

    def update(self):
        self.bullet_rotate_degree += self.bullet_rotate_dir*DEGREE_PER_TIME*game_framework.frame_time

        self.t += RUN_SPEED_PPS*game_framework.frame_time/100
        self.x = (1 - self.t) * self.startX + self.t * self.endX
        self.y = (1 - self.t) * self.startY + self.t * self.endY


