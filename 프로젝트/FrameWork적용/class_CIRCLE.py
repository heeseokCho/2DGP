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
RUN_velocity_KMPH = 20.0
RUN_velocity_MPM = (RUN_velocity_KMPH*1000.0/60.0)
RUN_velocity_MPS = (RUN_velocity_MPM / 60.0)
RUN_velocity_PPS = (RUN_velocity_MPS*PIXEL_PER_METER)

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

        Circle.velocity = 0

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
                pass
                #Circle.dir *= -1
            Circle.timer = 0

        Circle.x =WINX//2+ 8*PIXEL_PER_METER*math.cos(Circle.degree)
        Circle.y =WINY//2+ 8*PIXEL_PER_METER*math.sin(Circle.degree)

    @staticmethod
    def draw(Circle):
        Circle.image.opacify(0.5)
        Circle.image.draw(Circle.x - Circle.r * 0.01, Circle.y - Circle.r * 0.01, WINX * 2 + Circle.r, WINX * 2 + Circle.r)




class State2State:
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


next_tate_table = {}

class CIRCLE:

    def __init__(self):
        self.image = load_image('Circle.png')
        self.event_que = []
        self.cur_state = Stage1State
        self.cur_state.enter(self,None)
        self.cur_time = 0
        self.x,self.y = WINX//2+500,WINY//2
        self.r = 300
        self.dir =1
        self.degree = 0
        self.velocity = 0.005
        self.timer = 0


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
