from pico2d import*
import game_framework
import game_world
from class_ARROW import ARROW

#윈도우 크기
WINX  = 1600
WINY  = 1000
#사진 크기
SIZE = 64
#방향별 사진
UP,DOWN,LEFT,RIGHT = SIZE*3, SIZE*2, SIZE*1, SIZE*0

#Link Run Speed
PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

#Link Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0/TIME_PER_ACTION
FRAMES_PER_ACTION = 8

#Link Event
UP_DOWN,DOWN_DOWN,LEFT_DOWN,RIGHT_DOWN,\
UP_UP,DOWN_UP,LEFT_UP,RIGHT_UP,\
ATTACK_DOWN,ATTACK_UP,AIM_TIMER= range(11)


key_event_table = {
    (SDL_KEYDOWN, SDLK_w): UP_DOWN,
    (SDL_KEYDOWN, SDLK_s): DOWN_DOWN,
    (SDL_KEYDOWN,SDLK_a): LEFT_DOWN,
    (SDL_KEYDOWN,SDLK_d): RIGHT_DOWN,
    (SDL_KEYUP, SDLK_w): UP_UP,
    (SDL_KEYUP, SDLK_s): DOWN_UP,
    (SDL_KEYUP, SDLK_a): LEFT_UP,
    (SDL_KEYUP, SDLK_d): RIGHT_UP,
    (SDL_KEYDOWN, SDLK_j):ATTACK_DOWN,
    (SDL_KEYUP, SDLK_j): ATTACK_UP
}

class IdleState:

    @staticmethod
    def enter(Link, event):
        Link.frame = 0
        Link.image = load_image('Standing.png')

        if event == UP_DOWN:
            Link.velocityY += RUN_SPEED_PPS
            Link.dir = UP
        elif event == DOWN_DOWN:
            Link.velocityY -= RUN_SPEED_PPS
            Link.dir = DOWN
        elif event == UP_UP:
            Link.velocityY -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            Link.velocityY += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            Link.velocityX -= RUN_SPEED_PPS
            Link.dir = LEFT
        elif event == RIGHT_DOWN:
            Link.velocityX += RUN_SPEED_PPS
            Link.dir = RIGHT
        elif event == LEFT_UP:
            Link.velocityX += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            Link.velocityX -= RUN_SPEED_PPS


    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % 1

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, Link.dir, SIZE, SIZE, Link.x, Link.y)


class RunState:
    @staticmethod
    def enter(Link, event):
        Link.image = load_image('Walking.png')
        Link.frame = 0

        if event == UP_DOWN:
            Link.velocityY += RUN_SPEED_PPS
            Link.dir = UP
        elif event == DOWN_DOWN:
            Link.velocityY -= RUN_SPEED_PPS
            Link.dir = DOWN
        elif event == UP_UP:
            Link.velocityY -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            Link.velocityY += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            Link.velocityX -= RUN_SPEED_PPS
            Link.dir = LEFT
        elif event == RIGHT_DOWN:
            Link.velocityX += RUN_SPEED_PPS
            Link.dir = RIGHT
        elif event == LEFT_UP:
            Link.velocityX += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            Link.velocityX -= RUN_SPEED_PPS

    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10
        Link.x += Link.velocityX*game_framework.frame_time
        Link.y += Link.velocityY*game_framework.frame_time
        Link.x = clamp(SIZE, Link.x,WINX-SIZE)
        Link.y = clamp(SIZE,Link.y,WINY-250)

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, Link.dir, SIZE, SIZE, Link.x, Link.y)


class AimState:
    @staticmethod
    def enter(Link, event):
        Link.image = load_image('Aiming.png')
        Link.frame = 0
        Link.timer = 0
        Link.enable = False

        if event == UP_DOWN:
            Link.velocityY += RUN_SPEED_PPS
            Link.dir = UP
        elif event == DOWN_DOWN:
            Link.velocityY -= RUN_SPEED_PPS
            Link.dir = DOWN
        elif event == UP_UP:
            Link.velocityY -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            Link.velocityY += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            Link.velocityX -= RUN_SPEED_PPS
            Link.dir = LEFT
        elif event == RIGHT_DOWN:
            Link.velocityX += RUN_SPEED_PPS
            Link.dir = RIGHT
        elif event == LEFT_UP:
            Link.velocityX += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            Link.velocityX -= RUN_SPEED_PPS

    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        Link.x += Link.velocityX*game_framework.frame_time
        Link.y += Link.velocityY*game_framework.frame_time
        Link.x = clamp(SIZE, Link.x,WINX-SIZE)
        Link.y = clamp(SIZE,Link.y,WINY-250)

        Link.timer += get_time() - Link.cur_time
        Link.cur_time = get_time()

        if Link.timer >= 0.5:
            Link.enable = True
            Link.add_event(AIM_TIMER)

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, Link.dir, SIZE, SIZE, Link.x, Link.y)


class AimIdleState:
    @staticmethod
    def enter(Link, event):

        Link.image = load_image('AimStanding.png')
        Link.frame = 0
        Link.timer = 0

        if event == UP_DOWN:
            Link.velocityY += RUN_SPEED_PPS
            Link.dir = UP
        elif event == DOWN_DOWN:
            Link.velocityY -= RUN_SPEED_PPS
            Link.dir = DOWN
        elif event == UP_UP:
            Link.velocityY -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            Link.velocityY += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            Link.velocityX -= RUN_SPEED_PPS
            Link.dir = LEFT
        elif event == RIGHT_DOWN:
            Link.velocityX += RUN_SPEED_PPS
            Link.dir = RIGHT
        elif event == LEFT_UP:
            Link.velocityX += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            Link.velocityX -= RUN_SPEED_PPS


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
        Link.image.clip_draw(int(Link.frame) * SIZE, Link.dir, SIZE, SIZE, Link.x, Link.y)


class AimRunState:
    @staticmethod
    def enter(Link, event):
        Link.image = load_image('AimWalking.png')
        Link.frame = 0

        if event == UP_DOWN:
            Link.velocityY += RUN_SPEED_PPS
            Link.dir = UP
        elif event == DOWN_DOWN:
            Link.velocityY -= RUN_SPEED_PPS
            Link.dir = DOWN
        elif event == UP_UP:
            Link.velocityY -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            Link.velocityY += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            Link.velocityX -= RUN_SPEED_PPS
            Link.dir = LEFT
        elif event == RIGHT_DOWN:
            Link.velocityX += RUN_SPEED_PPS
            Link.dir = RIGHT
        elif event == LEFT_UP:
            Link.velocityX += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            Link.velocityX -= RUN_SPEED_PPS


    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        Link.x += Link.velocityX * game_framework.frame_time
        Link.y += Link.velocityY * game_framework.frame_time
        Link.x = clamp(SIZE, Link.x,WINX-SIZE)
        Link.y = clamp(SIZE,Link.y,WINY-250)


    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, Link.dir, SIZE, SIZE, Link.x, Link.y)


class ShootState:
    @staticmethod
    def enter(Link, event):
        if event == ATTACK_UP:
            if Link.enable == True:
                Link.shoot_arrow()

        Link.image = load_image('Shooting.png')
        Link.frame = 0
        Link.timer = 0

        if event == UP_DOWN:
            Link.velocityY += RUN_SPEED_PPS
            Link.dir = UP
        elif event == DOWN_DOWN:
            Link.velocityY -= RUN_SPEED_PPS
            Link.dir = DOWN
        elif event == UP_UP:
            Link.velocityY -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            Link.velocityY += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            Link.velocityX -= RUN_SPEED_PPS
            Link.dir = LEFT
        elif event == RIGHT_DOWN:
            Link.velocityX += RUN_SPEED_PPS
            Link.dir = RIGHT
        elif event == LEFT_UP:
            Link.velocityX += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            Link.velocityX -= RUN_SPEED_PPS

    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6


        if Link.enable == True:
            Link.timer += get_time() - Link.cur_time
            Link.cur_time = get_time()

            if Link.timer >= 3:
                Link.add_event(AIM_TIMER)
        else:
            Link.add_event(ATTACK_UP)

        Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        Link.x += Link.velocityX * game_framework.frame_time
        Link.y += Link.velocityY * game_framework.frame_time
        Link.x = clamp(SIZE, Link.x,WINX-SIZE)
        Link.y = clamp(SIZE,Link.y,WINY-250)


    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, Link.dir, SIZE, SIZE, Link.x, Link.y)


class DieState:
    @staticmethod
    def enter(Link, event):
        Link.image = load_image('AimStanding.png')
        Link.frame = 0

    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + 1) % 9


    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, Link.dir, SIZE, SIZE, Link.x, Link.y)


class WinState:

    @staticmethod
    def enter(Link, event):
        Link.frame = 0
        Link.image = load_image('Winning.png')


    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        pass

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, Link.dir, SIZE, SIZE, Link.x, Link.y)


next_state_table = {
    IdleState:{UP_DOWN:RunState,DOWN_DOWN:RunState,LEFT_DOWN:RunState,RIGHT_DOWN:RunState,
               UP_UP:RunState,DOWN_UP:RunState,LEFT_UP:RunState,RIGHT_UP:RunState,
               ATTACK_DOWN:AimState,ATTACK_UP:IdleState,AIM_TIMER: IdleState},

    RunState: {UP_DOWN:RunState,DOWN_DOWN:RunState,LEFT_DOWN:RunState,RIGHT_DOWN:RunState,
               UP_UP:RunState,DOWN_UP:RunState,LEFT_UP:RunState,RIGHT_UP:RunState,
               ATTACK_DOWN:AimState,ATTACK_UP:RunState,AIM_TIMER: RunState},

    AimState:{UP_DOWN:AimRunState,DOWN_DOWN:AimRunState,LEFT_DOWN:AimRunState,RIGHT_DOWN:AimRunState,
               UP_UP:RunState,DOWN_UP:RunState,LEFT_UP:RunState,RIGHT_UP:RunState,
               ATTACK_DOWN:AimState,ATTACK_UP:RunState,AIM_TIMER:AimRunState},

    AimIdleState:{UP_DOWN:AimRunState,DOWN_DOWN:AimRunState,LEFT_DOWN:AimRunState,RIGHT_DOWN:AimRunState,
               UP_UP:AimIdleState,DOWN_UP:AimIdleState,LEFT_UP:AimIdleState,RIGHT_UP:AimIdleState,
               ATTACK_DOWN:AimIdleState,ATTACK_UP:ShootState,AIM_TIMER:AimIdleState},

    AimRunState:{UP_DOWN:AimRunState,DOWN_DOWN:AimRunState,LEFT_DOWN:AimRunState,RIGHT_DOWN:AimRunState,
               UP_UP:AimRunState,DOWN_UP:AimRunState,LEFT_UP:AimRunState,RIGHT_UP:AimRunState,
               ATTACK_DOWN:AimRunState,ATTACK_UP:ShootState,AIM_TIMER:AimRunState},

    ShootState:{UP_DOWN:RunState,DOWN_DOWN:RunState,LEFT_DOWN:RunState,RIGHT_DOWN:RunState,
               UP_UP:ShootState,DOWN_UP:ShootState,LEFT_UP:ShootState,RIGHT_UP:ShootState,
               ATTACK_DOWN:ShootState,ATTACK_UP:RunState,AIM_TIMER:RunState},

    DieState:{UP_DOWN:DieState,DOWN_DOWN:DieState,LEFT_DOWN:DieState,RIGHT_DOWN:DieState,
               UP_UP:DieState,DOWN_UP:DieState,LEFT_UP:DieState,RIGHT_UP:DieState,
               ATTACK_DOWN:DieState,ATTACK_UP:DieState,AIM_TIMER:DieState},

    WinState:{UP_DOWN:WinState,DOWN_DOWN:WinState,LEFT_DOWN:WinState,RIGHT_DOWN:WinState,
               UP_UP:WinState,DOWN_UP:WinState,LEFT_UP:WinState,RIGHT_UP:WinState,
               ATTACK_DOWN:WinState,ATTACK_UP:WinState,AIM_TIMER:WinState}

}

class LINK:
    global Arrow
    x = None
    y = None
    dir = None
    life = None
    attack_speed = None
    run_speed =None

    def __init__(self):
        self.image = load_image('Standing.png')
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self,None)
        self.cur_time = 0
        self.frame = 0
        self.timer = 0
        self.velocityX,self.velocityY = 0.0,0.0
        self.enable = False

        if LINK.x ==None:
            LINK.x = WINX//2
            LINK.y = WINY//2
            LINK.dir = DOWN
            LINK.life = 3
            LINK.attack_speed = 0
            LINK.run_speed = 0


    def update_rect(self):
        pass

    def draw_rect(self):
        pass

    def shoot_arrow(self):
        Arrow = ARROW(self.x,self.y,self.dir)
        self.enable = False
        game_world.add_object(Arrow,1)

    def add_event(self,event):
        self.event_que.insert(0,event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self,event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self,event)

        self.update_rect()

    def draw(self):
        self.cur_state.draw(self)

        self.draw_rect()

    def handle_event(self,event):
        if (event.type,event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)






