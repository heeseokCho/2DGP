from pico2d import *

#define
WINX  = 1600
WINY  = 1000
open_canvas(WINX,WINY)

Link_Walking = load_image('Walking.png')
Link_Standing = load_image('Standing.png')
Link_Shooting = load_image('Shooting.png')
Link_Aiming = load_image('Aiming.png')
Link_AimWalking = load_image('AimWalking.png')
Link_Dieing = load_image('Dieing.png')
Arrow = load_image('Arrow.png')

#사진 크기
SIZE = 64
#방향별 사진
UP,DOWN,LEFT,RIGHT = SIZE*3, SIZE*2, SIZE*1, SIZE*0
#상태
STANDING,WALKING,SHOOTING,AIMING,AIMWALKING,DIEING,AIMSTANDING,WINNING =\
[0,1],   [1,10], [2,6],   [3,3], [4,8],     [5,9], [6,1],       [7,1]



#class
class LINK:
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
        self.dirX,self.dirY = 0,0

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
        elif self.state == WINNING:
            self.image = load_image('Winning.png')

    def Draw(self):
        #조준할때는 느리게 그림
        if self.state == AIMING:
            self.image.clip_draw((int(self.frame / 4)) * SIZE, self.look, SIZE, SIZE, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * SIZE, self.look,
                                SIZE, SIZE, self.x, self.y)


    def Update(self):
        #조준할때는 느리게 그림
        if self.state == AIMING:
            self.frame = (self.frame + 1) % (self.state[1]*4)
        else:
            self.frame = (self.frame + 1) % self.state[1]


        self.x += self.dirX * 8
        self.y += self.dirY * 8

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

    def ShootCheck(self):
        if self.shootStart == True:
            self.SetState(SHOOTING)
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

#global variable
Running = True
Link = LINK()

#function
def handle_events():
    global Running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Running = False

        #키가 눌렸을 때
        elif event.type == SDL_KEYDOWN:
            Link.frame = 0
            #이동
            if event.key == SDLK_d:
                Link.GoRight()

            elif event.key == SDLK_a:
                Link.GoLeft()

            elif event.key == SDLK_w:
                Link.GoUp()

            elif event.key == SDLK_s:
                Link.GoDown()
            #조준
            elif event.key == SDLK_j:
                Link.frame = 0
                Link.aimStart = True
                Link.SetState(AIMING)

            #종료
            elif event.key == SDLK_ESCAPE:
                Running = False

        ### 여기서 부턴 리소스를 확인하기 위함
            ##죽는애니메이션
            elif event.key == SDLK_1:
                Link.SetState(DIEING)
            ##클리어애니메이션
            elif event.key == SDLK_2:
                Link.SetState(WINNING)
        #####################

        #키를 땠을 때
        if event.type == SDL_KEYUP:
            Link.frame = 0

            if event.key == SDLK_d:
                Link.dirX -= 1

            elif event.key == SDLK_a:
                Link.dirX += 1

            elif event.key == SDLK_w:
                Link.dirY -= 1

            elif event.key == SDLK_s:
                Link.dirY += 1

            elif event.key == SDLK_j:
                if Link.aimCnt > 3:
                    Link.aimCnt = 0
                    Link.aimStart = False
                    Link.shootStart = True
                    Link.SetState(SHOOTING)
                else:
                    Link.aimCnt = 0
                    Link.aimStart = False
                    Link.SetState(WALKING)



        #현재 멈춰있는지
            Link.MoveToStopCheck()



while Running:
    clear_canvas()

    Link.Update()
    Link.Draw()


    update_canvas()
    handle_events()

    delay(0.05)





