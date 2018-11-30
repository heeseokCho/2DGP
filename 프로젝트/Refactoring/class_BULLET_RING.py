from pico2d import*
import game_framework
import game_world
import main_state2_sunset

import class_BOSS2_DEVIL

WINX,WINY = 1600,1000
SIZE  = 64
PI = 3.141592

LEFT_TOP,LEFT,LEFT_BOTTOM,BOTTOM,\
RIGHT_BOTTOM,RIGHT,RIGHT_TOP,TOP = range(8)

PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 10
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

DEGREE_PER_TIME = PI

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0/TIME_PER_ACTION
FRAMES_PER_ACTION = 1

class BULLET_RING:
    image = None

    def __init__(self,x = WINX//2,y=WINY//2,dir=0):
        if BULLET_RING.image == None:
            BULLET_RING.image = load_image('Bullet_Ring.png')
        self.frame = 0
        self.x,self.y = x,y
        self.dir = dir
        self.velocity = RUN_SPEED_PPS
        self.degree = 0


    def draw(self):
        if main_state2_sunset.Boss2_Devil.life > 0:
            BULLET_RING.image.clip_composite_draw(int(self.frame) * SIZE // 2, 0, SIZE // 2, SIZE // 2,
                                                    math.radians(self.degree),'v', self.x, self.y, SIZE, SIZE)

            #draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

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

        self.degree += DEGREE_PER_TIME

        if self.x <0 or self.x > WINX or \
                self.y <0 or self.y > WINY:
            class_BOSS2_DEVIL.BOSS2_DEVIL.bullet_ring.remove(self)
            game_world.remove_object(self)

    def get_bb(self):
        return self.x-16,self.y-16,self.x+16,self.y+16


