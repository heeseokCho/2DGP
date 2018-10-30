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

#상태 (상태이름, 프레임개수,현재 프레임)
STANDING,WALKING,SHOOTING,AIMING,AIMWALKING,DIEING,AIMSTANDING,WINNING =\
[0,1],   [1,10], [2,6],   [3,3], [4,8],     [5,9], [6,1],       [7,1]

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
        if event == RIGHT_DOWN:
            Link.velocityX += 1
        elif event == LEFT_DOWN:
            Link.velocityX -= 1
        elif event == RIGHT_UP:
            Link.velocityX -= 1
        elif event == LEFT_UP:
            Link.velocityX += 1
        elif event == RIGHT_DOWN:
            Link.velocityY += 1
        elif event == LEFT_DOWN:
            Link.velocityY -= 1
        elif event == RIGHT_UP:
            Link.velocityY -= 1
        elif event == LEFT_UP:
            Link.velocityY += 1

    @staticmethod
    def exit(Link, event):
        pass

    @staticmethod
    def do(Link):
        Link.frame = 0

    @staticmethod
    def draw(Link):
        if Link.dir == UP:
            Link.image.clip_draw(Link.frame * 100, 300, 100, 100, Link.x, Link.y)
        elif Link.dir == DOWN:
            Link.image.clip_draw(Link.frame * 100, 200, 100, 100, Link.x, Link.y)
        elif Link.dir == LEFT:
            Link.image.clip_draw(Link.frame * 100, 100, 100, 100, Link.x, Link.y)
        elif Link.dir == RIGHT:
            Link.image.clip_draw(Link.frame * 100, 0, 100, 100, Link.x, Link.y)
class LINK:
    global Arrow

    def __init__(self):
        self.image = load_image('Standing.png')
        self.state = STANDING
        self.look = DOWN
        self.aimStart = False
        self.chargeStart = False
        self.shootStart = False
        self.frame = 0
        self.aimCnt = 0
        self.chargeCnt = 0
        self.shootCnt = 0
        self.x,self.y = WINX//2, WINY//2
        self.dir
        self.velocityX,self.velocityY = 0,0

        #좌상우하
        self.RectBody = [self.x-16,self.y+20,self.x+16,self.y-20]
        self.RectFoot = [self.x - 8, self.y - 12, self.x + 8, self.y - 20]

    def SetState(self,_state):

        self.state = _state

        if self.state == STANDING:
            self.image =  load_image('Standing.png')
        elif self.state == WALKING:
            self.image = load_image('Walking.png')
        elif self.state == AIMING:
            self.image = load_image('Aiming.png')
        elif self.state == AIMWALKING:
            self.image = load_image('AimWalking.png')
        elif self.state == SHOOTING:
            self.image = load_image('Shooting.png')
        elif self.state == DIEING:
            self.image = load_image('Dieing.png')
        elif self.state == AIMSTANDING:
            self.image = load_image('AimStanding.png')

    def Draw(self):
        #조준할때는 느리게 그림
        if self.state == AIMING:
            self.image.clip_draw((int(self.frame / 4)) * SIZE, self.look, SIZE, SIZE, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * SIZE, self.look,
                                SIZE, SIZE, self.x, self.y)

    def DrawRectangle(self):
        draw_rectangle(self.RectBody[0],self.RectBody[1],self.RectBody[2],self.RectBody[3])
        draw_rectangle(self.RectFoot[0],self.RectFoot[1],self.RectFoot[2],self.RectFoot[3])


    def Update(self):
        #조준할때는 느리게 그림
        if self.state == AIMING:
            self.frame = (self.frame + 1) % (self.state[1]*4)
        else:
            self.frame = (self.frame + 1) % self.state[1]


        self.x += self.dirX * 8
        self.y += self.dirY * 8

        self.RectBody[0] = self.x-16
        self.RectBody[2] = self.x+16
        self.RectBody[1] = self.y-20
        self.RectBody[3] = self.y+20

        self.RectFoot[0] = self.x-8
        self.RectFoot[2] = self.x+8
        self.RectFoot[1] = self.y-12
        self.RectFoot[3] = self.y-20

        self.x = clamp(SIZE/2,self.x,WINX-SIZE/2)
        self.y = clamp(SIZE/2, self.y, WINY-SIZE/2-200)

        #조준시작했는지 체크
        self.AimCheck()
        #발사시작했는지 체크
        self.ShootCheck()



    def MoveToStopCheck(self):
        if self.dirX == 0 and self.dirY == 0:
            if self.aimCnt <= 3:
                self.SetState(STANDING)
            else:
                self.SetState(AIMSTANDING)

    def AimCheck(self):
        if self.aimStart == True:
            self.aimCnt += 1

        if self.aimCnt > AIMING[1]:
            self.SetState(AIMWALKING)
            self.aimStart = False

    def ShootCheck(self):
        if self.shootStart == True:
            Link.SetState(SHOOTING)

            if self.shootCnt == 0:
                #화살만듬
                Arrow.append(ARROW())
                Arrow[-1].Dir = Link.look

            self.shootCnt += 1

        if self.shootCnt > SHOOTING[1]:
            self.shootCnt = 0
            self.shootStart = False


            if self.dirX == 0 and self.dirY == 0:
                self.SetState(STANDING)
            else:
                self.SetState(WALKING)
            self.MoveToStopCheck()

    def CheckAimComplete(self):
        if self.aimCnt <= AIMING[1]:
            self.SetState(WALKING)
        else:
            self.SetState(AIMWALKING)

    def GoUp(self):
        self.CheckAimComplete()

        self.dirY += 1
        self.look = UP

    def GoDown(self):
        self.CheckAimComplete()

        self.dirY -= 1
        self.look = DOWN

    def GoLeft(self):
        self.CheckAimComplete()

        self.dirX -= 1
        self.look = LEFT

    def GoRight(self):
        self.CheckAimComplete()

        self.dirX += 1
        self.look = RIGHT