from pico2d import*
import game_framework
import game_world

import class_BOSS1_PLANT

WINX,WINY = 1600,1000
SIZE  = 64

LEFT_TOP,LEFT,LEFT_BOTTOM,BOTTOM,\
RIGHT_BOTTOM,RIGHT,RIGHT_TOP,TOP = range(8)

PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 12
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

class BULLET_SEED:
    image = None

    def __init__(self, x = WINX//2, y=WINY//2, dir=0):
        if BULLET_SEED.image == None:
            BULLET_SEED.image = load_image('Bullet_seed.png')
        self.x,self.y = x,y
        self.dir = dir
        self.velocity = RUN_SPEED_PPS


    def draw(self):
        if self.dir == LEFT_TOP:
            BULLET_SEED.image.clip_draw(SIZE*0,SIZE//2*2,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == LEFT:
            BULLET_SEED.image.clip_draw(SIZE*0,SIZE//2*1,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == LEFT_BOTTOM:
            BULLET_SEED.image.clip_draw(SIZE*0,SIZE//2*0,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == BOTTOM:
            BULLET_SEED.image.clip_draw(SIZE//2*1,SIZE//2*0,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == RIGHT_BOTTOM:
            BULLET_SEED.image.clip_draw(SIZE//2*2,SIZE//2*0,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == RIGHT:
            BULLET_SEED.image.clip_draw(SIZE//2*2,SIZE//2*1,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == RIGHT_TOP:
            BULLET_SEED.image.clip_draw(SIZE//2*2,SIZE//2*2,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == TOP:
            BULLET_SEED.image.clip_draw(SIZE//2*1,SIZE//2*2,SIZE//2,SIZE//2,self.x,self.y)

        draw_rectangle(*self.get_bb())


    def update(self):
        if self.dir == LEFT_TOP:
            self.x -= self.velocity*game_framework.frame_time
            self.y += self.velocity*game_framework.frame_time
        elif self.dir == LEFT:
            self.x -= self.velocity*game_framework.frame_time
        elif self.dir == LEFT_BOTTOM:
            self.x -= self.velocity*game_framework.frame_time
            self.y -= self.velocity*game_framework.frame_time
        elif self.dir == BOTTOM:
            self.y -= self.velocity*game_framework.frame_time
        elif self.dir == RIGHT_BOTTOM:
            self.x += self.velocity*game_framework.frame_time
            self.y -= self.velocity*game_framework.frame_time
        elif self.dir == RIGHT:
            self.x += self.velocity*game_framework.frame_time
        elif self.dir == RIGHT_TOP:
            self.x += self.velocity*game_framework.frame_time
            self.y += self.velocity*game_framework.frame_time
        elif self.dir == TOP:
            self.y += self.velocity*game_framework.frame_time

        if self.x <SIZE or self.x > WINX-SIZE or \
                self.y <SIZE or self. y >WINY-250:
            if self in class_BOSS1_PLANT.BOSS1_PLANT.bullet_seed:
                class_BOSS1_PLANT.BOSS1_PLANT.bullet_seed.remove(self)
                game_world.remove_object(self)

    def get_bb(self):
        return self.x-4, self.y-4, self.x+4, self.y+4

