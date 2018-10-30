from pico2d import*
import game_world
from class_ARROW import ARROW

#윈도우 크기
WINX  = 1600
WINY  = 1000
#사진 크기
SIZE = 64
#방향별 사진
UP,DOWN,LEFT,RIGHT = SIZE*3, SIZE*2, SIZE*1, SIZE*0

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
    (SDL_KEYUP,SDLK_j): ATTACK_UP
}

class IdleState:

    @staticmethod
    def enter(Link, event):
        Link.frame = 0
        Link.image = load_image('Standing.png')

        if event == UP_DOWN:
            Link.velocityY += 1
        elif event == DOWN_DOWN:
            Link.velocityY -= 1
        elif event == LEFT_DOWN:
            Link.velocityX -= 1
        elif event == RIGHT_DOWN:
            Link.velocityX += 1
        elif event == UP_UP:
            Link.velocityY -= 1
        elif event == DOWN_UP:
            Link.velocityY += 1
        elif event == RIGHT_UP:
            Link.velocityX -= 1
        elif event == LEFT_UP:
            Link.velocityX += 1

    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        pass

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(Link.frame * SIZE, Link.dir, SIZE, SIZE, Link.x, Link.y)


class RunState:
    @staticmethod
    def enter(Link, event):
        Link.image = load_image('Walking.png')
        Link.frame = 0

        if event == UP_DOWN:
            Link.velocityY += 1
            Link.dir = UP
        elif event == DOWN_DOWN:
            Link.velocityY -= 1
            Link.dir = DOWN
        elif event == LEFT_DOWN:
            Link.velocityX -= 1
            Link.dir = LEFT
        elif event == RIGHT_DOWN:
            Link.velocityX += 1
            Link.dir = RIGHT
        elif event == UP_UP:
            Link.velocityY -= 1
        elif event == DOWN_UP:
            Link.velocityY += 1
        elif event == RIGHT_UP:
            Link.velocityX -= 1
        elif event == LEFT_UP:
            Link.velocityX += 1


    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + 1) % 10
        Link.x += Link.velocityX
        Link.y += Link.velocityY
        Link.x = clamp(SIZE, Link.x, 1600 - SIZE)
        Link.y = clamp(SIZE, Link.y, 1000 - SIZE)

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(Link.frame * SIZE, Link.dir, SIZE, SIZE, Link.x, Link.y)


class AimState:
    @staticmethod
    def enter(Link, event):
        Link.image = load_image('Aiming.png')
        Link.frame = 0
        Link.timer = 10
        Link.enable = False

    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + 1) % 3
        Link.timer -=1

        if Link.timer == 0:
            Link.enable = True

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(Link.frame * SIZE, Link.dir, SIZE, SIZE, Link.x, Link.y)


class AimIdleState:
    def enter(Link, event):
        Link.image = load_image('AimStanding.png')
        Link.frame = 0

        if event == UP_DOWN:
            Link.velocityY += 1
        elif event == DOWN_DOWN:
            Link.velocityY -= 1
        elif event == LEFT_DOWN:
            Link.velocityX -= 1
        elif event == RIGHT_DOWN:
            Link.velocityX += 1
        elif event == UP_UP:
            Link.velocityY -= 1
        elif event == DOWN_UP:
            Link.velocityY += 1
        elif event == RIGHT_UP:
            Link.velocityX -= 1
        elif event == LEFT_UP:
            Link.velocityX += 1

    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.timer -=1

        if Link.timer == 0:
            Link.enable = True

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(Link.frame * SIZE, Link.dir, SIZE, SIZE, Link.x, Link.y)


class AimRunState:
    @staticmethod
    def enter(Link, event):
        Link.image = load_image('AimWalking.png')
        Link.frame = 0

        if event == UP_DOWN:
            Link.velocityY += 1
            Link.dir = UP
        elif event == DOWN_DOWN:
            Link.velocityY -= 1
            Link.dir = DOWN
        elif event == LEFT_DOWN:
            Link.velocityX -= 1
            Link.dir = LEFT
        elif event == RIGHT_DOWN:
            Link.velocityX += 1
            Link.dir = RIGHT
        elif event == UP_UP:
            Link.velocityY -= 1
        elif event == DOWN_UP:
            Link.velocityY += 1
        elif event == RIGHT_UP:
            Link.velocityX -= 1
        elif event == LEFT_UP:
            Link.velocityX += 1

    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + 1) % 8
        Link.x += Link.velocityX
        Link.y += Link.velocityY
        Link.x = clamp(SIZE, Link.x, 1600 - SIZE)
        Link.y = clamp(SIZE, Link.y, 1000 - SIZE)
        Link.timer -=1

        if Link.timer == 0:
            Link.enable = True

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(Link.frame * SIZE, Link.dir, SIZE, SIZE, Link.x, Link.y)


class ShootState:
    @staticmethod
    def enter(Link, event):
        Link.image = load_image('Shooting.png')
        Link.frame = 0
        Link.timer = 10

    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = (Link.frame + 1) % 6
        Link.timer -= 1

        if Link.enable == True:
            pass
        else:
            Link.add_event(IdleState)

    @staticmethod
    def draw(Link):
        Link.image.clip_draw(Link.frame * SIZE, Link.dir, SIZE, SIZE, Link.x, Link.y)


class DieState:
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
        Link.image.clip_draw(Link.frame * SIZE, 0, SIZE, SIZE, Link.x, Link.y)


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
        Link.image.clip_draw(Link.frame * SIZE, 0, SIZE, SIZE, Link.x, Link.y)


next_state_table = {
    IdleState:{UP_DOWN:RunState,DOWN_DOWN:RunState,LEFT_DOWN:RunState,RIGHT_DOWN:RunState,
               UP_UP:IdleState,DOWN_UP:IdleState,LEFT_UP:IdleState,RIGHT_UP:IdleState,
               ATTACK_DOWN:AimState,ATTACK_UP:IdleState},

    RunState: {UP_DOWN:RunState,DOWN_DOWN:RunState,LEFT_DOWN:RunState,RIGHT_DOWN:RunState,
               UP_UP:IdleState,DOWN_UP:IdleState,LEFT_UP:IdleState,RIGHT_UP:IdleState,
               ATTACK_DOWN:AimState,ATTACK_UP:RunState},

    AimState:{UP_DOWN:AimState,DOWN_DOWN:AimState,LEFT_DOWN:AimState,RIGHT_DOWN:AimState,
               UP_UP:AimState,DOWN_UP:AimState,LEFT_UP:AimState,RIGHT_UP:AimState,
               ATTACK_DOWN:AimState,ATTACK_UP:IdleState,AIM_TIMER:AimState},

    AimIdleState:{UP_DOWN:AimRunState,DOWN_DOWN:AimRunState,LEFT_DOWN:AimRunState,RIGHT_DOWN:AimRunState,
               UP_UP:AimIdleState,DOWN_UP:AimIdleState,LEFT_UP:AimIdleState,RIGHT_UP:AimIdleState,
               ATTACK_DOWN:AimIdleState,ATTACK_UP:IdleState,AIM_TIMER:AimIdleState},

    AimRunState:{UP_DOWN:AimRunState,DOWN_DOWN:AimRunState,LEFT_DOWN:AimRunState,RIGHT_DOWN:AimRunState,
               UP_UP:AimIdleState,DOWN_UP:AimIdleState,LEFT_UP:AimIdleState,RIGHT_UP:AimIdleState,
               ATTACK_DOWN:AimRunState,ATTACK_UP:ShootState,AIM_TIMER:AimRunState},

    ShootState:{UP_DOWN:ShootState,DOWN_DOWN:ShootState,LEFT_DOWN:ShootState,RIGHT_DOWN:ShootState,
               UP_UP:ShootState,DOWN_UP:ShootState,LEFT_UP:ShootState,RIGHT_UP:ShootState,
               ATTACK_DOWN:ShootState,ATTACK_UP:IdleState,AIM_TIMER:ShootState},

    DieState:{UP_DOWN:DieState,DOWN_DOWN:DieState,LEFT_DOWN:DieState,RIGHT_DOWN:DieState,
               UP_UP:DieState,DOWN_UP:DieState,LEFT_UP:DieState,RIGHT_UP:DieState,
               ATTACK_DOWN:DieState,ATTACK_UP:DieState,AIM_TIMER:DieState},

    WinState:{UP_DOWN:WinState,DOWN_DOWN:WinState,LEFT_DOWN:WinState,RIGHT_DOWN:WinState,
               UP_UP:WinState,DOWN_UP:WinState,LEFT_UP:WinState,RIGHT_UP:WinState,
               ATTACK_DOWN:WinState,ATTACK_UP:WinState,AIM_TIMER:WinState}

}

class LINK:
    global Arrow

    def __init__(self):
        self.image = load_image('Standing.png')
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self,None)
        self.frame = 0
        self.x,self.y = WINX//2, WINY//2
        self.dir = DOWN
        self.timer = 0
        self.velocityX,self.velocityY = 0,0
        self.enable = False

    def update_rect(self):
        pass

    def draw_rect(self):
        pass

    def shoot_arrow(self):
        pass

    def add_event(self,event):
        self.event_que.imsert(0,event)

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






