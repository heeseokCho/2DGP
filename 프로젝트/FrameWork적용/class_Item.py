from pico2d import*
import game_framework
import game_world

import random

WINX,WINY = 1600,1000
SIZE  = 64

RUN_SPEED,ARROW_SPEED,HEART= range(3)


class ITEM:
    image = None

    def __init__(self):
        if ITEM.image == None:
            ITEM.image = load_image('Item.png')

        self.kind = random.randint(0,2)
        self.x = random.randint(WINX//2-500,WINX//2+500)
        self.y = random.randint(100,WINY//2+250)


    def draw(self):

        if self.kind == HEART:
            ITEM.image.clip_draw(0,HEART * SIZE//2,SIZE//2,SIZE//2,self.x,self.y)
        elif self.kind == ARROW_SPEED:
            ITEM.image.clip_draw(0, ARROW_SPEED * SIZE//2, SIZE//2, SIZE//2, self.x, self.y)
        elif self.kind == RUN_SPEED:
            ITEM.image.clip_draw(0, RUN_SPEED * SIZE//2, SIZE//2, SIZE//2, self.x, self.y)

        draw_rectangle(*self.get_bb())
    def update(self):
        pass

    def get_bb(self):
        return self.x-6,self.y-6,self.x+6,self.y+6

