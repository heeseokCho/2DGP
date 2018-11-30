from pico2d import*
import game_world

from class_BULLET_SEED import BULLET_SEED
import class_BOSS1_PLANT

import random

WINX,WINY = 1600,1000
SIZE  = 64

PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

class BULLET_MINE:
    image = None
    bullet_seed = []

    def __init__(self):
        if BULLET_MINE.image == None:
            BULLET_MINE.image = load_image('Bullet_mine.png')
        self.x = random.randint(SIZE,WINX-SIZE)
        self.y = random.randint(SIZE,WINY-250)
        self.cur_time = 0
        self.timer = 0

    def shoot_bullet(self):
        if random.randint(0,1) == 0:
            bullet_seed = [BULLET_SEED(self.x,self.y,i) for i in range(0,8,2)]
        else:
            bullet_seed = [BULLET_SEED(self.x,self.y,i+1) for i in range(0,8, 2)]

        for o in bullet_seed:
            class_BOSS1_PLANT.BOSS1_PLANT.bullet_seed.append(o)
            game_world.add_object(o,1)

    def draw(self):
        self.image.draw(self.x,self.y,SIZE,SIZE)
        #draw_rectangle(*self.get_bb())

    def update(self):
        self.timer += get_time()-self.cur_time
        self.cur_time = get_time()

        if self.timer >=8:
            self.shoot_bullet()
            self.timer = 0

    def get_bb(self):
        return self.x-4, self.y-4, self.x+4, self.y+4