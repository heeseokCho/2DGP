from pico2d import*
import game_framework
import game_world

import title_state
import main_state2

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
RUN_SPEED_KMPH = 16.0
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
ATTACK_DOWN,ATTACK_UP,AIM_TIMER,LIFE_ZERO,CLEAR = range(13)


key_event_table = {
    (SDL_KEYDOWN, SDLK_w): UP_DOWN,
    (SDL_KEYDOWN, SDLK_s): DOWN_DOWN,
    (SDL_KEYDOWN, SDLK_a): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_d): RIGHT_DOWN,
    (SDL_KEYUP, SDLK_w): UP_UP,
    (SDL_KEYUP, SDLK_s): DOWN_UP,
    (SDL_KEYUP, SDLK_a): LEFT_UP,
    (SDL_KEYUP, SDLK_d): RIGHT_UP,
    (SDL_KEYDOWN, SDLK_j):ATTACK_DOWN,
    (SDL_KEYUP, SDLK_j): ATTACK_UP,
}

class IdleState:

    @staticmethod
    def enter(Link, event):
        Link.frame = 0
        Link.image = load_image('Standing.png')

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
        Link.image = load_image('Walking.png')
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
        LINK.x += (LINK.velocityX*(LINK.run_speed/4+1))*game_framework.frame_time
        LINK.y += (LINK.velocityY*(LINK.run_speed/4+1))*game_framework.frame_time
        LINK.x = clamp(SIZE, LINK.x, WINX - SIZE)
        LINK.y = clamp(SIZE, LINK.y, WINY - 250)

        Link.check_end()

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, LINK.dir, SIZE, SIZE, Link.x, Link.y)


class AimState:
    @staticmethod
    def enter(Link, event):
        Link.image = load_image('Aiming.png')
        Link.frame = 0

        Link.timer = 0
        #Link.cur_time = get_time()

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
            Link.bgm.set_volume(50)
            Link.bgm.play()

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        LINK.x += (LINK.velocityX*(LINK.run_speed/4+1)) * game_framework.frame_time
        LINK.y += (LINK.velocityY*(LINK.run_speed/4+1)) * game_framework.frame_time
        LINK.x = clamp(SIZE, LINK.x, WINX - SIZE)
        LINK.y = clamp(SIZE, LINK.y, WINY - 250)

        Link.timer += get_time() - Link.cur_time
        Link.cur_time = get_time()

        if Link.timer >= 0.3:
            Link.enable = True
            Link.add_event(AIM_TIMER)

        Link.check_end()

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, LINK.dir, SIZE, SIZE, Link.x, Link.y)


class AimIdleState:
    @staticmethod
    def enter(Link, event):

        Link.image = load_image('AimStanding.png')
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
        Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 1

        Link.check_end()

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, LINK.dir, SIZE, SIZE, Link.x, Link.y)


class AimRunState:
    @staticmethod
    def enter(Link, event):
        Link.image = load_image('AimWalking.png')
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
        LINK.x += (LINK.velocityX*(LINK.run_speed/4+1)) * game_framework.frame_time
        LINK.y += (LINK.velocityY*(LINK.run_speed/4+1)) * game_framework.frame_time
        LINK.x = clamp(SIZE, LINK.x, WINX - SIZE)
        LINK.y = clamp(SIZE, LINK.y, WINY - 250)

        Link.check_end()
    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, LINK.dir, SIZE, SIZE, Link.x, Link.y)


class ShootState:
    @staticmethod
    def enter(Link, event):
        if event == ATTACK_UP:
            if Link.enable == True:
                Link.shoot_arrow()

        Link.image = load_image('Shooting.png')
        Link.frame = 0
        Link.timer = 0
        #Link.cur_time = get_time()

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
            Link.timer += get_time() - Link.cur_time
            Link.cur_time = get_time()

            if Link.timer >= 1:
                Link.add_event(AIM_TIMER)

        else:
            Link.add_event(ATTACK_UP)


        Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        LINK.x += (LINK.velocityX*(LINK.run_speed/4+1)) * game_framework.frame_time
        LINK.y += (LINK.velocityY*(LINK.run_speed/4+1)) * game_framework.frame_time
        LINK.x = clamp(SIZE, LINK.x, WINX - SIZE)
        LINK.y = clamp(SIZE, LINK.y, WINY - 250)

        Link.check_end()

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, LINK.dir, SIZE, SIZE, Link.x, Link.y)


class DieState:

    @staticmethod
    def enter(Link, event):
        if event == LIFE_ZERO:
            Link.image = load_image('Dieing.png')
            Link.frame = 0

            title_state.Bgm = load_music('GameOver.mp3')
            title_state.Bgm.set_volume(50)
            title_state.Bgm.repeat_play()

            Link.timer = 0
            Link.cur_time = get_time()

            Link.collide_able = False



    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        if int(Link.frame) < 8:
            Link.frame = (Link.frame + FRAMES_PER_ACTION * ACTION_PER_TIME/2 * game_framework.frame_time) % 9

        Link.timer += get_time() - Link.cur_time
        Link.cur_time = get_time()

        #print(Link.timer)
        if Link.timer >= 8:
            Link.end = True

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(int(Link.frame) * SIZE, 0, SIZE, SIZE, Link.x, Link.y)


class WinState:

    @staticmethod
    def enter(Link, event):
        Link.image = load_image('Winning.png')
        Link.frame = 0
        Link.timer = 0
        Link.cur_time = get_time()

        Link.collide_able = False

        title_state.Bgm = load_music('GameClear.mp3')
        title_state.Bgm.set_volume(50)
        title_state.Bgm.repeat_play()



    @staticmethod
    def exit(Link, event):
        main_state2.game_cleared = False

    @staticmethod
    def do(Link):

        Link.timer += get_time() - Link.cur_time
        Link.cur_time = get_time()

        if Link.timer >= 5:
            Link.end = True

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(0, 0, SIZE, SIZE, Link.x, Link.y)


next_state_table = {
    IdleState:{UP_DOWN:RunState,DOWN_DOWN:RunState,LEFT_DOWN:RunState,RIGHT_DOWN:RunState,
               UP_UP:RunState,DOWN_UP:RunState,LEFT_UP:RunState,RIGHT_UP:RunState,
               ATTACK_DOWN:AimState,ATTACK_UP:IdleState,AIM_TIMER: IdleState,LIFE_ZERO:DieState,
               CLEAR:WinState},

    RunState: {UP_DOWN:RunState,DOWN_DOWN:RunState,LEFT_DOWN:RunState,RIGHT_DOWN:RunState,
               UP_UP:RunState,DOWN_UP:RunState,LEFT_UP:RunState,RIGHT_UP:RunState,
               ATTACK_DOWN:AimState,ATTACK_UP:RunState,AIM_TIMER: RunState,LIFE_ZERO:DieState,
               CLEAR: WinState},

    AimState:{UP_DOWN:AimRunState,DOWN_DOWN:AimRunState,LEFT_DOWN:AimRunState,RIGHT_DOWN:AimRunState,
               UP_UP:RunState,DOWN_UP:RunState,LEFT_UP:RunState,RIGHT_UP:RunState,
               ATTACK_DOWN:AimState,ATTACK_UP:RunState,AIM_TIMER:AimRunState,LIFE_ZERO:DieState,
              CLEAR: WinState},

    AimIdleState:{UP_DOWN:AimRunState,DOWN_DOWN:AimRunState,LEFT_DOWN:AimRunState,RIGHT_DOWN:AimRunState,
               UP_UP:AimIdleState,DOWN_UP:AimIdleState,LEFT_UP:AimIdleState,RIGHT_UP:AimIdleState,
               ATTACK_DOWN:AimIdleState,ATTACK_UP:ShootState,AIM_TIMER:AimIdleState,LIFE_ZERO:DieState,
                  CLEAR: WinState},

    AimRunState:{UP_DOWN:AimRunState,DOWN_DOWN:AimRunState,LEFT_DOWN:AimRunState,RIGHT_DOWN:AimRunState,
               UP_UP:AimRunState,DOWN_UP:AimRunState,LEFT_UP:AimRunState,RIGHT_UP:AimRunState,
               ATTACK_DOWN:AimRunState,ATTACK_UP:ShootState,AIM_TIMER:AimRunState,LIFE_ZERO:DieState,
                 CLEAR: WinState},

    ShootState:{UP_DOWN:RunState,DOWN_DOWN:RunState,LEFT_DOWN:RunState,RIGHT_DOWN:RunState,
               UP_UP:ShootState,DOWN_UP:ShootState,LEFT_UP:ShootState,RIGHT_UP:ShootState,
               ATTACK_DOWN:ShootState,ATTACK_UP:RunState,AIM_TIMER:RunState,LIFE_ZERO:DieState,
                CLEAR: WinState},

    DieState:{UP_DOWN:None,DOWN_DOWN:None,LEFT_DOWN:None,RIGHT_DOWN:None,
               UP_UP:None,DOWN_UP:None,LEFT_UP:None,RIGHT_UP:None,
               ATTACK_DOWN:None,ATTACK_UP:None,AIM_TIMER:None,LIFE_ZERO:None,
              CLEAR: None},

    WinState:{UP_DOWN:None,DOWN_DOWN:None,LEFT_DOWN:None,RIGHT_DOWN:None,
               UP_UP:None,DOWN_UP:None,LEFT_UP:None,RIGHT_UP:None,
               ATTACK_DOWN:None,ATTACK_UP:None,AIM_TIMER:None,LIFE_ZERO:None,
              CLEAR: None}

}

class LINK:
    global Arrow
    x = WINX // 2
    y = WINY // 2
    dir = DOWN
    velocityX,velocityY = 0.0,0.0
    life = 3
    arrow_speed = 0
    run_speed = 0
    bgm = None
    arrow = []
    cur_stage = 0



    def __init__(self):
        self.image = load_image('Standing.png')
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self,None)
        self.cur_time = get_time()
        self.frame = 0
        self.timer = 0
        self.enable = False
        self.end = False
        self.collide_able = True

    def reset(self):
        LINK.dir = DOWN
        LINK.life = 3
        LINK.arrow_speed = 0
        LINK.run_speed = 0

        LINK.cur_stage = 0

    def reset_all(self):
        LINK.x = WINX // 2
        LINK.y = WINY // 2
        LINK.dir = DOWN
        LINK.velocityX, velocityY = 0.0, 0.0
        LINK.life = 3
        LINK.arrow_speed = 0
        LINK.run_speed = 0
        LINK.bgm = None
        LINK.arrow = []
        LINK.cur_stage = 0
        LINK.dir = DOWN
        LINK.life = 3
        LINK.arrow_speed = 0
        LINK.run_speed = 0
        LINK.cur_stage = 0

    def check_end(self):
        if LINK.life == 0:
            self.add_event(LIFE_ZERO)

        if main_state2.game_cleared == True:
            main_state2.game_cleared = False
            self.add_event(CLEAR)

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

        LINK.arrow.append(Arrow)
        self.enable = False
        game_world.add_object(Arrow,1)

        self.bgm = load_wav('Shot.wav')
        self.bgm.set_volume(50)
        self.bgm.play()

    def add_event(self,event):
        self.event_que.insert(0,event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self,event)
            if next_state_table[self.cur_state][event] != None:
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






