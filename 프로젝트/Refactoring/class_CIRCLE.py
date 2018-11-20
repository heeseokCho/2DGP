from pico2d import*
import game_framework
import random
import math

import main_state_bonus
import main_state1_day
import main_state2_sunset


#윈도우 크기
WINX  = 1600
WINY  = 1000
SIZE = 64
PI = 3.141592


#Circle Run velocity
PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

DEGREE_PER_TIME = PI/36

#Circle events
TIMER = range(0)


class Stage0State:
    @staticmethod
    def enter(Circle, event):
        Circle.timer =0
        Circle.cur_time = get_time()

        Circle.dirX, Circle.dirY = 0, 0

        CIRCLE.x, CIRCLE.y = main_state2_sunset.LINK.x, main_state2_sunset.LINK.y
        Circle.r = 380
        if random.randint(0, 1) == 0:
            Circle.dirX = -1
        else:
            Circle.dirX = 1

        if random.randint(0, 1) == 0:
            Circle.dirY = -1
        else:
            Circle.dirY = 1

            Circle.velocity = RUN_SPEED_PPS / 1000

    @staticmethod
    def exit(Circle, event):
        pass

    @staticmethod
    def do(Circle):
        Circle.timer+=get_time()-Circle.cur_time
        Circle.cur_time = get_time()

        if Circle.timer >5:
            Circle.velocity += RUN_SPEED_PPS/3000

            Circle.timer = 0

        if Circle.r < 100:
            Circle.dir = 1
        elif Circle.r > 400:
            Circle.dir = -1

        if(CIRCLE.x > WINX-Circle.r):
            Circle.dirX = -1
        elif(CIRCLE.x < Circle.r):
            Circle.dirX = 1
        if (CIRCLE.y > WINY- Circle.r):
            Circle.dirY = -1
        elif (CIRCLE.y < Circle.r):
            Circle.dirY = 1


        if main_state_bonus.Link != None and main_state_bonus.Link.collide_able:
            CIRCLE.x += Circle.dirX * Circle.velocity
            CIRCLE.y += Circle.dirY * Circle.velocity
            Circle.r += Circle.dir * Circle.velocity*3



    @staticmethod
    def draw(Circle):
        Circle.image.opacify(0.85)
        Circle.image.draw(CIRCLE.x - Circle.r * 0.01, CIRCLE.y - Circle.r * 0.01, WINX * 2 + Circle.r,
                          WINX * 2 + Circle.r)




class Stage1State:
    @staticmethod
    def enter(Circle,event):
        Circle.cur_state = Stage1State

        CIRCLE.x, CIRCLE.y = WINX // 2, WINY // 2
        Circle.r = 300
        Circle.degree = 0

        Circle.degree = math.atan2(main_state2_sunset.LINK.y - CIRCLE.y, main_state2_sunset.LINK.x - CIRCLE.x)

        CIRCLE.x, CIRCLE.y = CIRCLE.x + 300 * math.cos(Circle.degree), \
                             CIRCLE.y + 300 * math.sin(Circle.degree)

    @staticmethod
    def exit(Circle,event):
        pass

    @staticmethod
    def do(Circle):
        Circle.degree += Circle.dir*(DEGREE_PER_TIME+Circle.velocity)*game_framework.frame_time

        Circle.timer+=get_time()-Circle.cur_time
        Circle.cur_time = get_time()

        if Circle.timer >= 10:
            Circle.velocity += PI/64
            if random.randint(0, 1) == 0:
                Circle.dir *= -1
            Circle.timer = 0

        if main_state1_day.Link != None and main_state1_day.Link.collide_able:
            CIRCLE.x =WINX//2+ 8*PIXEL_PER_METER*math.cos(Circle.degree)
            CIRCLE.y =WINY//2+ 8*PIXEL_PER_METER*math.sin(Circle.degree)

    @staticmethod
    def draw(Circle):
        Circle.image.opacify(0.85)
        Circle.image.draw(CIRCLE.x - Circle.r * 0.01, CIRCLE.y - Circle.r * 0.01, WINX * 2 + Circle.r, WINX * 2 + Circle.r)



class Stage2State:
    @staticmethod
    def enter(Circle, event):
        Circle.dirX, Circle.dirY = 0, 0

        CIRCLE.x, CIRCLE.y = main_state2_sunset.LINK.x, main_state2_sunset.LINK.y
        Circle.r = 380
        if random.randint(0, 1) == 0:
            Circle.dirX = -1
        else:
            Circle.dirX = 1

        if random.randint(0, 1) == 0:
            Circle.dirY = -1
        else:
            Circle.dirY = 1

            Circle.dir = -1
            Circle.velocity = RUN_SPEED_PPS / 1000

    @staticmethod
    def exit(Circle, event):
        pass

    @staticmethod
    def do(Circle):
        Circle.timer+=get_time()-Circle.cur_time
        Circle.cur_time = get_time()

        if Circle.timer >= 12:
            Circle.velocity += RUN_SPEED_PPS/5000

            Circle.timer = 0

        if Circle.r < 100:
            Circle.dir = 1
        elif Circle.r > 400:
            Circle.dir = -1

        if(CIRCLE.x > WINX-Circle.r):
            Circle.dirX = -1
        elif(CIRCLE.x < Circle.r):
            Circle.dirX = 1
        if (CIRCLE.y > WINY - Circle.r):
            Circle.dirY = -1
        elif (CIRCLE.y < Circle.r):
            Circle.dirY = 1

        if main_state2_sunset.Link != None and main_state2_sunset.Link.collide_able:
            CIRCLE.x += Circle.dirX * Circle.velocity
            CIRCLE.y += Circle.dirY * Circle.velocity
            Circle.r += Circle.dir * Circle.velocity*2



    @staticmethod
    def draw(Circle):
        Circle.image.opacify(0.85)
        Circle.image.draw(CIRCLE.x - Circle.r * 0.01, CIRCLE.y - Circle.r * 0.01, WINX * 2 + Circle.r,
                          WINX * 2 + Circle.r)


next_state_table = {}

class CIRCLE:
    image = None
    x,y =0,0

    def __init__(self,phase):
        if CIRCLE.image == None:
            CIRCLE.image = load_image('Circle.png')

        self.event_que = []
        self.cur_state = Stage0State

        self.cur_time = 0
        self.timer = 0
        self.r =0
        self.dir = 1
        self.velocity = 0
        CIRCLE.x,CIRCLE.y = 0,0

        if phase == 0:
            self.cur_state = Stage0State
            self.cur_state.enter(self, None)

        elif phase == 1:
            self.cur_state = Stage1State
            self.cur_state.enter(self, None)

        elif phase == 2:
            self.cur_state = Stage2State
            self.cur_state.enter(self, None)



    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())


    def draw_rect(self):
        pass

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def update_rect(self):
        pass

    def handle_event(self,event):
        pass

    def get_bb(self):
        if self.cur_state == Stage0State:
            return CIRCLE.x - 320 - self.r / 8, CIRCLE.y - 320 - self.r / 8, \
                   CIRCLE.x + 320 + self.r / 8, CIRCLE.y + 320 + self.r / 8
        elif self.cur_state == Stage1State:
            return CIRCLE.x-self.r-SIZE,CIRCLE.y-self.r-SIZE,CIRCLE.x+self.r+SIZE,CIRCLE.y+self.r+SIZE
        elif self.cur_state == Stage2State:
            return CIRCLE.x - 320-self.r/8, CIRCLE.y - 320-self.r/8,\
                   CIRCLE.x + 320+self.r/8, CIRCLE.y + 320+self.r/8