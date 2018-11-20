import game_framework
from pico2d import *
from ball import Ball

import game_world

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8



# Boy Event
RIGHT_DOWN, LEFT_DOWN,UP_DOWN,DOWN_DOWN, RIGHT_UP, LEFT_UP, UP_UP,DOWN_UP,SLEEP_TIMER, SPACE = range(10)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}


# Boy States

class IdleState:

    @staticmethod
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.x_velocity += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            boy.x_velocity -= RUN_SPEED_PPS
        if event == LEFT_DOWN:
            boy.x_velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            boy.x_velocity += RUN_SPEED_PPS

        if event == UP_DOWN:
            boy.y_velocity += RUN_SPEED_PPS
        elif event == UP_UP:
            boy.y_velocity -= RUN_SPEED_PPS
        if event == DOWN_DOWN:
            boy.y_velocity -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            boy.y_velocity += RUN_SPEED_PPS

        boy.timer = 1000

    @staticmethod
    def exit(boy, event):
        if event == SPACE:
            boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        boy.timer -= 1
        if boy.timer == 0:
            boy.add_event(SLEEP_TIMER)

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(int(boy.frame) * 100, 300, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(int(boy.frame) * 100, 200, 100, 100, boy.x, boy.y)


class RunState:

    @staticmethod
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.x_velocity += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            boy.x_velocity -= RUN_SPEED_PPS
        if event == LEFT_DOWN:
            boy.x_velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            boy.x_velocity += RUN_SPEED_PPS

        if event == UP_DOWN:
            boy.y_velocity += RUN_SPEED_PPS
        elif event == UP_UP:
            boy.y_velocity -= RUN_SPEED_PPS
        if event == DOWN_DOWN:
            boy.y_velocity -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            boy.y_velocity += RUN_SPEED_PPS

        boy.dir = clamp(-1, boy.x_velocity, 1)

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        #boy.frame = (boy.frame + 1) % 8
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        boy.x += boy.x_velocity * game_framework.frame_time
        boy.y += boy.y_velocity * game_framework.frame_time

        boy.x = clamp(25, boy.x, 1600 - 25)

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(int(boy.frame) * 100, 100, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(int(boy.frame) * 100, 0, 100, 100, boy.x, boy.y)


class SleepState:

    @staticmethod
    def enter(boy, event):
        boy.frame = 0

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_composite_draw(int(boy.frame) * 100, 300, 100, 100, 3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(int(boy.frame) * 100, 200, 100, 100, -3.141592 / 2, '', boy.x + 25, boy.y - 25, 100, 100)






next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, UP_UP: RunState,DOWN_UP: RunState,
                RIGHT_DOWN: RunState, LEFT_DOWN: RunState, UP_DOWN:RunState, DOWN_DOWN: RunState,SLEEP_TIMER: SleepState, SPACE: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,UP_UP:IdleState,DOWN_UP:IdleState,
               LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,UP_DOWN: IdleState,DOWN_DOWN: IdleState, SPACE: RunState},
    SleepState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState, LEFT_UP: RunState, RIGHT_UP: RunState, SPACE: IdleState}
}

class Boy:
    def __init__(self):
        self.x, self.y = 1600 // 2, 90
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('animation_sheet.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.dir = 1
        self.x_velocity = 0
        self.y_velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.eat_cnt = 0

        # fill here
        self.eat_sound = load_wav('pickup.wav')
        self.eat_sound.set_volume(32)

    def eat(self, ball):
        # fill here
        self.eat_sound.play()
        self.eat_cnt += 1


    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50


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
        self.font.draw(self.x - 60, self.y + 50, '(Eat: %3.2i)' % self.eat_cnt, (255, 255, 0))
        #fill here
        draw_rectangle(*self.get_bb())
        #debug_print('Velocity :' + str(self.velocity) + '  Dir:' + str(self.dir) + ' Frame Time:' + str(game_framework.frame_time))

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

