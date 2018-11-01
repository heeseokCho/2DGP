from pico2d import*
import game_world

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
        pass

    def draw(self):
        self.image.draw(self.x,self.y)

    def update(self):
        self.timer += get_time()-self.cur_time
        self.cur_time = get_time()

        if self.timer >=5:
            self.shoot_bullet()
            self.timer = 0
