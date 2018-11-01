from pico2d import*
import game_framework
import random
import math

#윈도우 크기
WINX  = 1600
WINY  = 1000

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


class State0State:
    @staticmethod
    def enter(Circle, event):
        pass

    @staticmethod
    def exit(Circle, event):
        pass

    @staticmethod
    def do(Circle):
        pass

    @staticmethod
    def draw(Circle):
        pass




class Stage1State:
    @staticmethod
    def enter(Circle,event):
        Circle.x, Circle.y = WINX // 2 + 500, WINY // 2
        Circle.r = 300
        Circle.dir = 1
        Circle.degree = 0
        Circle.timer = 0
        Circle.velocity = 0.05

    @staticmethod
    def exit(Circle,event):
        pass

    @staticmethod
    def do(Circle):
        Circle.degree +=  + Circle.dir*(DEGREE_PER_TIME+Circle.velocity)*game_framework.frame_time

        Circle.timer+=get_time()-Circle.cur_time
        Circle.cur_time = get_time()

        if Circle.timer >= 20:
            Circle.velocity += PI/36
            if random.randint(0, 1) == 0:
                Circle.dir *= -1
            Circle.timer = 0

        Circle.x =WINX//2+ 8*PIXEL_PER_METER*math.cos(Circle.degree)
        Circle.y =WINY//2+ 8*PIXEL_PER_METER*math.sin(Circle.degree)

    @staticmethod
    def draw(Circle):
        Circle.image.opacify(0.85)
        Circle.image.draw(Circle.x - Circle.r * 0.01, Circle.y - Circle.r * 0.01, WINX * 2 + Circle.r, WINX * 2 + Circle.r)



class Stage2State:
    @staticmethod
    def enter(Circle, event):
        Circle.x, Circle.y = WINX // 2, WINY // 2
        Circle.r = 380
        if random.randint(0,1) ==0:
            Circle.dirX = -1
        else: Circle.dirX = 1

        if random.randint(0,1) ==0:
            Circle.dirY = -1
        else: Circle.dirY = 1

        Circle.dir = -1
        Circle.velocity = RUN_SPEED_PPS

    @staticmethod
    def exit(Circle, event):
        pass

    @staticmethod
    def do(Circle):
        Circle.timer+=get_time()-Circle.cur_time
        Circle.cur_time = get_time()

        if Circle.timer >= 15:
            Circle.velocity += RUN_SPEED_PPS/5000
            if random.randint(0, 1) == 0:
                Circle.dirX = -1
            else: Circle.dirX = 1
            if random.randint(0, 1) == 0:
                Circle.dirY = -1
            else: Circle.dirY = 1

            Circle.timer = 0

        if Circle.r < 100:
            Circle.dir = 1
        elif Circle.r > 400:
            Circle.dir = -1

        if(Circle.x > WINX-Circle.r):
            Circle.dirX = -1
        elif(Circle.x < Circle.r):
            Circle.dirX = 1
        if (Circle.y > WINY-200 - Circle.r):
            Circle.dirY = -1
        elif (Circle.y < Circle.r):
            Circle.dirY = 1

        Circle.x += Circle.dirX * Circle.velocity
        Circle.y += Circle.dirY * Circle.velocity
        Circle.r += Circle.dir * Circle.velocity*2



    @staticmethod
    def draw(Circle):
        Circle.image.opacify(0.85)
        Circle.image.draw(Circle.x - Circle.r * 0.01, Circle.y - Circle.r * 0.01, WINX * 2 + Circle.r,
                          WINX * 2 + Circle.r)


next_state_table = {}

class CIRCLE:
    image = None

    def __init__(self,phase):
        if CIRCLE.image == None:
            CIRCLE.image = load_image('Circle.png')
        self.cur_state = Stage1State
        self.event_que = []
        self.cur_state.enter(self, None)
        self.cur_time = 0
        self.x,self.y,self.r =0,0,0
        self.dir = 1
        self.velocity = 0

        if phase == 1:
            self.cur_state = Stage1State

            self.degree = 0
        elif phase == 2:
            self.cur_state = Stage2State
            self.dirX,self.dirY =0,0

            self.x, self.y = WINX // 2, WINY // 2
            self.r = 380
            if random.randint(0, 1) == 0:
                self.dirX = -1
            else:
                self.dirX = 1

            if random.randint(0, 1) == 0:
                self.dirY = -1
            else:
                self.dirY = 1

                self.dir = -1
                self.velocity = RUN_SPEED_PPS/1000


    def draw(self):
        self.cur_state.draw(self)


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
