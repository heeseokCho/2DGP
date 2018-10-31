import game_framework
from pico2d import *
from class_ARROW import ARROW

import game_world

import math
import random
PI = 3.141592

# Link Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

DEGREE_PER_TIME = PI

# Link Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0/TIME_PER_ACTION
FRAMES_PER_ACTION = 8

RIGHT,LEFT,DOWN,UP = range(4)
SIZE = 32



# Link Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP= range(4)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
}


# Link States

class IdleState:

    @staticmethod
    def enter(Link, event):
        Link.timer = 0
        if event == RIGHT_DOWN:
            Link.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            Link.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            Link.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            Link.velocity += RUN_SPEED_PPS

    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 1

        Link.timer += get_time() - Link.cur_time
        Link.cur_time = get_time()


    @staticmethod
    def draw(Link):
        if Link.dir == LEFT:
            Link.image.clip_draw(int(Link.frame),LEFT*SIZE , SIZE, SIZE, Link.x, Link.y)
        elif Link.dir == RIGHT:
            Link.image.clip_draw(int(Link.frame),RIGHT*SIZE, SIZE, SIZE, Link.x, Link.y)

class RunState:

    @staticmethod
    def enter(Link, event):
        # fill here
        if event == RIGHT_DOWN:
            Link.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            Link.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            Link.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            Link.velocity += RUN_SPEED_PPS

        Link.dir = clamp(-1,Link.velocity,1)

    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame +FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time)%8
        # fill here
        Link.x+=Link.velocity*game_framework.frame_time
        Link.x = clamp(25, Link.x, 1600 - 25)

    @staticmethod
    def draw(Link):
        if Link.dir == 1:
            Link.image.clip_draw(int(Link.frame) * 100, 100, 100, 100, Link.x, Link.y)
        else:
            Link.image.clip_draw(int(Link.frame) * 100, 0, 100, 100, Link.x, Link.y)





next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState},
}

class LINK:

    def __init__(self):
        self.x, self.y = 1600 // 2, 90
        # Link is only once created, so instance image loading is fine
        self.image = load_image('Walking.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.cur_time = 0
        self.degree = 0
        self.timer = 0


    def shoot_arrow(self):
        arrow = ARROW(self.x, self.y, self.dir*3)
        game_world.add_object(arrow, 1)


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


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

