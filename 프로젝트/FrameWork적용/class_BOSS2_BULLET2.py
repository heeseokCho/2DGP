from pico2d import*
import game_framework
import game_world

import random

WINX,WINY = 1600,1000
SIZE  = 64

LEFT_TOP,LEFT,LEFT_BOTTOM,BOTTOM,\
RIGHT_BOTTOM,RIGHT,RIGHT_TOP,TOP = range(8)

PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 0.05
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

class BOSS2_BULLET2:
    image = None

    def __init__(self,x = WINX//2,y=WINY//2,dir=0):
        if BOSS2_BULLET2.image == None:
            BOSS2_BULLET2.image = load_image('Enemy.png')
        self.x,self.y = x,y
        self.dir = dir
        self.velocity = RUN_SPEED_PPS


    def draw(self):
        if self.dir == LEFT_TOP:
            BOSS2_BULLET2.image.clip_draw(SIZE*0,SIZE//2*2,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == LEFT:
            BOSS2_BULLET2.image.clip_draw(SIZE*0,SIZE//2*1,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == LEFT_BOTTOM:
            BOSS2_BULLET2.image.clip_draw(SIZE*0,SIZE//2*0,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == BOTTOM:
            BOSS2_BULLET2.image.clip_draw(SIZE//2*1,SIZE//2*0,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == RIGHT_BOTTOM:
            BOSS2_BULLET2.image.clip_draw(SIZE//2*2,SIZE//2*0,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == RIGHT:
            BOSS2_BULLET2.image.clip_draw(SIZE//2*2,SIZE//2*1,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == RIGHT_TOP:
            BOSS2_BULLET2.image.clip_draw(SIZE//2*2,SIZE//2*2,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == TOP:
            BOSS2_BULLET2.image.clip_draw(SIZE//2*1,SIZE//2*2,SIZE//2,SIZE//2,self.x,self.y)


    def update(self):
        if self.dir == LEFT_TOP:
            self.x -= self.velocity
            self.y += self.velocity
        elif self.dir == LEFT:
            self.x -= self.velocity
        elif self.dir == LEFT_BOTTOM:
            self.x -= self.velocity
            self.y -= self.velocity
        elif self.dir == BOTTOM:
            self.y -= self.velocity
        elif self.dir == RIGHT_BOTTOM:
            self.x += self.velocity
            self.y -= self.velocity
        elif self.dir == RIGHT:
            self.x += self.velocity
        elif self.dir == RIGHT_TOP:
            self.x += self.velocity
            self.y += self.velocity
        elif self.dir == TOP:
            self.y += self.velocity

        if self.x <SIZE or self.x > WINX-SIZE or \
                self.y <SIZE or self. y >WINY-SIZE:
            game_world.remove_object(self)


