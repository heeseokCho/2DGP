from pico2d import*
import game_world

from class_BOSS1_BULLET2 import BOSS1_BULLET2

import random

WINX,WINY = 1600,1000
SIZE  = 64

PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

class BOSS1_BULLET1:
    image = None

    def __init__(self):
        if BOSS1_BULLET1.image == None:
            BOSS1_BULLET1.image = load_image('Boss1Bullet1.png')
        self.x = random.randint(SIZE,WINX-SIZE)
        self.y = random.randint(SIZE,WINY-SIZE)
        self.cur_time = 0
        self.timer = 0

    def shoot_bullet(self):
        if random.randint(0,1) == 0:
            bullet2 = [BOSS1_BULLET2(self.x,self.y,i) for i in range(0,8,2)]
        else:
            bullet2 = [BOSS1_BULLET2(self.x, self.y, i+1) for i in range(0,8, 2)]

        for o in bullet2:
            game_world.add_object(o,1)

    def draw(self):
        self.image.draw(self.x,self.y,SIZE,SIZE)

    def update(self):
        self.timer += get_time()-self.cur_time
        self.cur_time = get_time()

        if self.timer >=5:
            self.shoot_bullet()
            self.timer = 0
