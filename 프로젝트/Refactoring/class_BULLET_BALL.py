from pico2d import*
import game_world
import game_framework
import main_state2_sunset

import class_BOSS2_DEVIL
import random
import math

WINX,WINY = 1600,1000
SIZE  = 64
PI = 3.141592

PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 8.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

DEGREE_PER_TIME = PI/36

class BULLET_BALL:
    image = None

    def __init__(self,x=0,y=0):
        if BULLET_BALL.image == None:
            BULLET_BALL.image = load_image('Bullet_Ball.png')

        self.startX,self.startY = x,y
        self.endX,self.endY=main_state2_sunset.LINK.x,main_state2_sunset.LINK.y
        self.x,self.y =x,y
        self.velocity = RUN_SPEED_PPS
        self.bullet_rotate_degree = 0
        self.t = 0

        if random.randint(0,1) == 0:
            self.bullet_rotate_dir = -1
        else:
            self.bullet_rotate_dir = 1



    def draw(self):
        if main_state2_sunset.Boss2_Devil.life > 0:
            BULLET_BALL.image.rotate_draw(math.radians(self.bullet_rotate_degree), self.x, self.y, SIZE / 2, SIZE / 2)
            #draw_rectangle(*self.get_bb())

    def update(self):
        self.bullet_rotate_degree += self.bullet_rotate_dir*DEGREE_PER_TIME*game_framework.frame_time

        self.t += RUN_SPEED_PPS*game_framework.frame_time/100
        self.x = (1 - self.t) * self.startX + self.t * self.endX
        self.y = (1 - self.t) * self.startY + self.t * self.endY

        if self.x < SIZE or self.x > WINX-SIZE or self.y < SIZE or self.y > WINY-250:
            class_BOSS2_DEVIL.BOSS2_DEVIL.bullet_ball.remove(self)
            game_world.remove_object(self)

    def get_bb(self):
        return self.x-4,self.y-4,self.x+4,self.y+4


