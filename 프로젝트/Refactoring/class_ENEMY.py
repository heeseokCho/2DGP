from pico2d import*
import game_framework
import game_world

import random
import class_STAGE0
from class_LINK import LINK

WINX,WINY = 1600,1000
SIZE = 64

LEFT_TOP,LEFT,LEFT_BOTTOM,BOTTOM,\
RIGHT_BOTTOM,RIGHT,RIGHT_TOP,TOP = range(8)

PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 12
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

class ENEMY:
    image = None
    def __init__(self,dir = 0):
        if ENEMY.image == None:
            ENEMY.image = load_image('Enemy.png')

        self.dir = dir
        self.size = random.randint(1,2)

        if self.dir == LEFT_TOP:
            self.dirX, self.dirY = -1, 1
        elif self.dir == LEFT:
            self.dirX, self.dirY = -1, 0
        elif self.dir== LEFT_BOTTOM:
            self.dirX, self.dirY = -1, -1
        elif self.dir == BOTTOM:
            self.dirX, self.dirY = 0, -1
        elif self.dir == RIGHT_BOTTOM:
            self.dirX, self.dirY = 1, -1
        elif self.dir == RIGHT:
            self.dirX, self.dirY = 1, 0
        elif self.dir == RIGHT_TOP:
            self.dirX, self.dirY = 1, 1
        elif self.dir == TOP:
            self.dirX, self.dirY = 0, 1

        if random.randint(0,1) == 0:
            self.x = random.randint(int(LINK.x-300),int(LINK.x-100))
        else:
            self.x = random.randint(int(LINK.x + 100),int(LINK.x+300))

        if random.randint(0,1) == 0:
            self.y = random.randint(int(LINK.y-300),int(LINK.y-100))
        else:
            self.y = random.randint(int(LINK.y + 100),int(LINK.y+300))

    def draw(self):

        if self.dir == LEFT_TOP:
            ENEMY.image.clip_draw(SIZE*0,SIZE//2*2,SIZE//2,SIZE//2,self.x,self.y,SIZE//self.size,SIZE//self.size)
        elif self.dir == LEFT:
            ENEMY.image.clip_draw(SIZE*0,SIZE//2*1,SIZE//2,SIZE//2,self.x,self.y,SIZE//self.size,SIZE//self.size)
        elif self.dir == LEFT_BOTTOM:
            ENEMY.image.clip_draw(SIZE*0,SIZE//2*0,SIZE//2,SIZE//2,self.x,self.y,SIZE//self.size,SIZE//self.size)
        elif self.dir == BOTTOM:
            ENEMY.image.clip_draw(SIZE//2*1,SIZE//2*0,SIZE//2,SIZE//2,self.x,self.y,SIZE//self.size,SIZE//self.size)
        elif self.dir == RIGHT_BOTTOM:
            ENEMY.image.clip_draw(SIZE//2*2,SIZE//2*0,SIZE//2,SIZE//2,self.x,self.y,SIZE//self.size,SIZE//self.size)
        elif self.dir == RIGHT:
            ENEMY.image.clip_draw(SIZE//2*2,SIZE//2*1,SIZE//2,SIZE//2,self.x,self.y,SIZE//self.size,SIZE//self.size)
        elif self.dir == RIGHT_TOP:
            ENEMY.image.clip_draw(SIZE//2*2,SIZE//2*2,SIZE//2,SIZE//2,self.x,self.y,SIZE//self.size,SIZE//self.size)
        elif self.dir == TOP:
            ENEMY.image.clip_draw(SIZE//2*1,SIZE//2*2,SIZE//2,SIZE//2,self.x,self.y,SIZE//self.size,SIZE//self.size)

        draw_rectangle(*self.get_bb())

    def update(self):
       self.x += self.dirX*RUN_SPEED_PPS*game_framework.frame_time
       self.y += self.dirY*RUN_SPEED_PPS*game_framework.frame_time

       if self.x > WINX or self.x < 0 or self.y > WINY-250 or self.y < 0:
        class_STAGE0.STAGE0.enemy.remove(self)
        game_world.remove_object(self)

    def get_bb(self):
        if self.size == 1:
            return self.x-12,self.y-12,self.x+12,self.y+12
        else:
            return self.x - 8, self.y - 8, self.x + 8, self.y + 8



