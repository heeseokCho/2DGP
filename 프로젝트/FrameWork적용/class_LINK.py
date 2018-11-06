from pico2d import*
import game_framework
import game_world
import title_state
from class_ARROW import ARROW
from class_ITEM import ITEM

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
    (pico2d.SDL_KEYDOWN, pico2d.SDLK_w): UP_DOWN,
    (pico2d.SDL_KEYDOWN, pico2d.SDLK_s): DOWN_DOWN,
    (pico2d.SDL_KEYDOWN, pico2d.SDLK_a): LEFT_DOWN,
    (pico2d.SDL_KEYDOWN, pico2d.SDLK_d): RIGHT_DOWN,
    (pico2d.SDL_KEYUP, pico2d.SDLK_w): UP_UP,
    (pico2d.SDL_KEYUP, pico2d.SDLK_s): DOWN_UP,
    (pico2d.SDL_KEYUP, pico2d.SDLK_a): LEFT_UP,
    (pico2d.SDL_KEYUP, pico2d.SDLK_d): RIGHT_UP,
    (pico2d.SDL_KEYDOWN, pico2d.SDLK_j):ATTACK_DOWN,
    (pico2d.SDL_KEYUP, pico2d.SDLK_j): ATTACK_UP
}

class IdleState:

    @staticmethod
    def enter(Link, event):
        Link.frame = 0
        Link.image = pico2d.load_image('Standing.png')

        if event == UP_DOWN:
            LINK.velocityY += RUN_SPEED_PPS
            LINK.dir = UP
        elif event == DOWN_DOWN:
            LINK.velocityY -= RUN_SPEED_PPS
            LINK.dir = DOWN
        elif event == UP_UP:
            LINK.velocityY -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            LINK.velocityY += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            LINK.velocityX -= RUN_SPEED_PPS
            LINK.dir = LEFT
        elif event == RIGHT_DOWN:
            LINK.velocityX += RUN_SPEED_PPS
            LINK.dir = RIGHT
        elif event == LEFT_UP:
            LINK.velocityX += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            LINK.velocityX -= RUN_SPEED_PPS


    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % 1

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, LINK.dir, SIZE, SIZE, Link.x, Link.y)


class RunState:
    @staticmethod
    def enter(Link, event):
        Link.image = pico2d.load_image('Walking.png')
        Link.frame = 0

        if event == UP_DOWN:
            LINK.velocityY += RUN_SPEED_PPS
            LINK.dir = UP
        elif event == DOWN_DOWN:
            LINK.velocityY -= RUN_SPEED_PPS
            LINK.dir = DOWN
        elif event == UP_UP:
            LINK.velocityY -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            LINK.velocityY += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            LINK.velocityX -= RUN_SPEED_PPS
            LINK.dir = LEFT
        elif event == RIGHT_DOWN:
            LINK.velocityX += RUN_SPEED_PPS
            LINK.dir = RIGHT
        elif event == LEFT_UP:
            LINK.velocityX += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            LINK.velocityX -= RUN_SPEED_PPS

    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10
        LINK.x += LINK.velocityX*game_framework.frame_time
        LINK.y += LINK.velocityY*game_framework.frame_time
        LINK.x = pico2d.clamp(SIZE, LINK.x, WINX - SIZE)
        LINK.y = pico2d.clamp(SIZE, LINK.y, WINY - 250)

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, LINK.dir, SIZE, SIZE, Link.x, Link.y)


class AimState:
    @staticmethod
    def enter(Link, event):
        Link.image = pico2d.load_image('Aiming.png')
        Link.frame = 0
        Link.timer = 0
        Link.enable = False

        if event == UP_DOWN:
            LINK.velocityY += RUN_SPEED_PPS
            LINK.dir = UP
        elif event == DOWN_DOWN:
            LINK.velocityY -= RUN_SPEED_PPS
            LINK.dir = DOWN
        elif event == UP_UP:
            LINK.velocityY -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            LINK.velocityY += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            LINK.velocityX -= RUN_SPEED_PPS
            LINK.dir = LEFT
        elif event == RIGHT_DOWN:
            LINK.velocityX += RUN_SPEED_PPS
            LINK.dir = RIGHT
        elif event == LEFT_UP:
            LINK.velocityX += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            LINK.velocityX -= RUN_SPEED_PPS

    @staticmethod
    def exit(Link, event):
        if Link.enable == False:
            Link.bgm = load_wav('ShotFail.wav')
            Link.bgm.set_volume(30)
            Link.bgm.play()

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        LINK.x += LINK.velocityX*game_framework.frame_time
        LINK.y += LINK.velocityY*game_framework.frame_time
        LINK.x = pico2d.clamp(SIZE, LINK.x, WINX - SIZE)
        LINK.y = pico2d.clamp(SIZE, LINK.y, WINY - 250)

        Link.timer += pico2d.get_time() - Link.cur_time
        Link.cur_time = pico2d.get_time()

        if Link.timer >= 0.5:
            Link.enable = True
            Link.add_event(AIM_TIMER)

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, LINK.dir, SIZE, SIZE, Link.x, Link.y)


class AimIdleState:
    @staticmethod
    def enter(Link, event):

        Link.image = pico2d.load_image('AimStanding.png')
        Link.frame = 0
        Link.timer = 0

        if event == UP_DOWN:
            LINK.velocityY += RUN_SPEED_PPS
            LINK.dir = UP
        elif event == DOWN_DOWN:
            LINK.velocityY -= RUN_SPEED_PPS
            LINK.dir = DOWN
        elif event == UP_UP:
            LINK.velocityY -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            LINK.velocityY += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            LINK.velocityX -= RUN_SPEED_PPS
            LINK.dir = LEFT
        elif event == RIGHT_DOWN:
            LINK.velocityX += RUN_SPEED_PPS
            LINK.dir = RIGHT
        elif event == LEFT_UP:
            LINK.velocityX += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            LINK.velocityX -= RUN_SPEED_PPS


    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 1

        Link.timer += pico2d.get_time() - Link.cur_time
        Link.cur_time = pico2d.get_time()

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, LINK.dir, SIZE, SIZE, Link.x, Link.y)


class AimRunState:
    @staticmethod
    def enter(Link, event):
        Link.image = pico2d.load_image('AimWalking.png')
        Link.frame = 0

        if event == UP_DOWN:
            LINK.velocityY += RUN_SPEED_PPS
            LINK.dir = UP
        elif event == DOWN_DOWN:
            LINK.velocityY -= RUN_SPEED_PPS
            LINK.dir = DOWN
        elif event == UP_UP:
            LINK.velocityY -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            LINK.velocityY += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            LINK.velocityX -= RUN_SPEED_PPS
            LINK.dir = LEFT
        elif event == RIGHT_DOWN:
            LINK.velocityX += RUN_SPEED_PPS
            LINK.dir = RIGHT
        elif event == LEFT_UP:
            LINK.velocityX += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            LINK.velocityX -= RUN_SPEED_PPS


    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        LINK.x += LINK.velocityX * game_framework.frame_time
        LINK.y += LINK.velocityY * game_framework.frame_time
        LINK.x = pico2d.clamp(SIZE, LINK.x, WINX - SIZE)
        LINK.y = pico2d.clamp(SIZE, LINK.y, WINY - 250)


    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, LINK.dir, SIZE, SIZE, Link.x, Link.y)


class ShootState:
    @staticmethod
    def enter(Link, event):
        if event == ATTACK_UP:
            if Link.enable == True:
                Link.shoot_arrow()

        Link.image = pico2d.load_image('Shooting.png')
        Link.frame = 0
        Link.timer = 0

        if event == UP_DOWN:
            LINK.velocityY += RUN_SPEED_PPS
            LINK.dir = UP
        elif event == DOWN_DOWN:
            LINK.velocityY -= RUN_SPEED_PPS
            LINK.dir = DOWN
        elif event == UP_UP:
            LINK.velocityY -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            LINK.velocityY += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            LINK.velocityX -= RUN_SPEED_PPS
            LINK.dir = LEFT
        elif event == RIGHT_DOWN:
            LINK.velocityX += RUN_SPEED_PPS
            LINK.dir = RIGHT
        elif event == LEFT_UP:
            LINK.velocityX += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            LINK.velocityX -= RUN_SPEED_PPS

    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6


        if Link.enable == True:
            Link.timer += pico2d.get_time() - Link.cur_time
            Link.cur_time = pico2d.get_time()

            if Link.timer >= 3:
                Link.add_event(AIM_TIMER)

        else:
            Link.add_event(ATTACK_UP)


        Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        LINK.x += LINK.velocityX * game_framework.frame_time
        LINK.y += LINK.velocityY * game_framework.frame_time
        LINK.x = pico2d.clamp(SIZE, LINK.x, WINX - SIZE)
        LINK.y = pico2d.clamp(SIZE, LINK.y, WINY - 250)


    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, LINK.dir, SIZE, SIZE, Link.x, Link.y)


class DieState:
    @staticmethod
    def enter(Link, event):
        Link.image = pico2d.load_image('AimStanding.png')
        Link.frame = 0
        Link.timer = 0

    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 9

        Link.timer += pico2d.get_time() - Link.cur_time
        Link.cur_time = pico2d.get_time()

        if Link.timer >= 5:
            game_framework.change_state(title_state)

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, LINK.dir, SIZE, SIZE, Link.x, Link.y)


class WinState:

    @staticmethod
    def enter(Link, event):
        Link.image = pico2d.load_image('Winning.png')
        Link.frame = 0


    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 9

        Link.timer += pico2d.get_time() - Link.cur_time
        Link.cur_time = pico2d.get_time()

        if Link.timer >= 5:
            game_framework.change_state(title_state)

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, LINK.dir, SIZE, SIZE, Link.x, Link.y)


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
    velocityX,velocityY = None,None
    life = None
    arrow_speed = None
    run_speed =None
    bgm = None

    def __init__(self):
        self.image = pico2d.load_image('Standing.png')
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self,None)
        self.cur_time = 0
        self.frame = 0
        self.timer = 0
        self.enable = False
        self.arrow = []

        if LINK.x == None:
            LINK.x = WINX//2
            LINK.y = WINY//2
            LINK.dir = DOWN
            LINK.life = 3
            LINK.arrow_speed = 1
            LINK.run_speed = 2
            LINK.velocityX = 0.0
            LINK.velocityY = 0.0

    def get_bb(self):
        return LINK.x-10,LINK.y-10,LINK.x+10,LINK.y+10

    def draw_ability(self):
        if ITEM.image != None:
            for i in range(LINK.life):
                ITEM.image.clip_draw(0, 2 * SIZE // 2, SIZE // 2, SIZE // 2, LINK.x-SIZE//3+ i * SIZE//3, LINK.y - SIZE*1//3,SIZE//3,SIZE//3)
            for i in range(LINK.arrow_speed):
                ITEM.image.clip_draw(0, 1 * SIZE // 2, SIZE // 2, SIZE // 2, LINK.x-SIZE//3+i * SIZE//3, LINK.y-SIZE*2//3,SIZE//3,SIZE//3)
            for i in range(LINK.run_speed):
                ITEM.image.clip_draw(0, 0 * SIZE // 2, SIZE // 2, SIZE // 2, LINK.x-SIZE//3+i * SIZE//3, LINK.y - SIZE * 3//3,SIZE//3,SIZE//3)

    def shoot_arrow(self):
        Arrow = ARROW(LINK.x,LINK.y,LINK.dir)
        self.arrow.append(Arrow)
        self.enable = False
        game_world.add_object(Arrow,1)

        self.bgm = load_wav('Shot.wav')
        self.bgm.set_volume(30)
        self.bgm.play()

    def add_event(self,event):
        self.event_que.insert(0,event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self,event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self,event)

    def draw(self):
        self.cur_state.draw(self)
        self.draw_ability()

        draw_rectangle(*self.get_bb())

    def handle_event(self,event):
        if (event.type,event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)






