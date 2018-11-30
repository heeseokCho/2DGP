import game_framework
from pico2d import*
import game_world

import class_LINK
from class_BULLET_MINE import BULLET_MINE
from class_BULLET_SEED import BULLET_SEED

WINX,WINY = 1600, 1000
PI = 3.141592
SIZE = 64

LEFT_TOP,LEFT,LEFT_BOTTOM,BOTTOM,\
RIGHT_BOTTOM,RIGHT,RIGHT_TOP,TOP = range(8)

# Boss1 Run Speed
PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

DEGREE_PER_TIME = PI

# Boss1 Action Speed
TIME_PER_ACTION = 3
ACTION_PER_TIME = 1.0/TIME_PER_ACTION
FRAMES_PER_ACTION = 8



next_state_table ={}

class RunState:
    @staticmethod
    def enter(Boss1,event):
        Boss1.frame= 0

    @staticmethod
    def exit(Boss1,event):
        pass

    @staticmethod
    def do(Boss1):
        Boss1.frame = (Boss1.frame +FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time)%5

        Boss1.timer += get_time() - Boss1.cur_time
        Boss1.cur_time = get_time()

        if Boss1.timer >=4:
            Boss1.shoot_bullet2()
            Boss1.shoot_bullet1()
            Boss1.timer = 0

        if Boss1.life <= 0:
            class_LINK.LINK.cur_stage = 2

    @staticmethod
    def draw(Boss1):
        Boss1.image.clip_draw(int(Boss1.frame)*SIZE*3,0,SIZE*3,SIZE*3,Boss1.x,Boss1.y)


class BOSS1_PLANT:
    bullet_mine = []
    bullet_seed = []

    def __init__(self):
        self.x, self.y = WINX//2, WINY//2
        self.image = load_image('Boss1_plant.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = RunState
        self.cur_state.enter(self, None)
        self.cur_time = 0
        self.degree = 0
        self.timer = 0
        self.life = 0.9



        self.bgm = load_wav('BossShot.ogg')

    #지뢰
    def shoot_bullet1(self):
        bullet_mine = BULLET_MINE()
        BOSS1_PLANT.bullet_mine.append(bullet_mine)

        game_world.add_object(bullet_mine,1)
        self.bgm.set_volume(30)
        self.bgm.play()

    #8방
    def shoot_bullet2(self):
        bullet_seed = [BULLET_SEED(self.x,self.y,i) for i in range(8)]
        for i in bullet_seed:
            BOSS1_PLANT.bullet_seed.append(i)

        for o in bullet_seed:
            game_world.add_object(o,1)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

        #draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x-SIZE*2/3, self.y-SIZE*2/3, self.x+SIZE*2/3, self.y+SIZE*2/3
