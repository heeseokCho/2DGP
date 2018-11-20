from pico2d import *

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

open_canvas(WINX,WINY)

Background = load_image('Background.png')

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

        self.RectBody[0] +=self.dirX * 8
        self.RectBody[2] += self.dirX * 8
        self.RectBody[1] += self.dirY * 8
        self.RectBody[3] += self.dirY * 8

        self.RectFoot[0] += self.dirX * 8
        self.RectFoot[2] += self.dirX * 8
        self.RectFoot[1] += self.dirY * 8
        self.RectFoot[3] += self.dirY * 8

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
            Link.SetState(SHOOTING)
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

class BOSS1:
    def __init__(self):
        self.image = load_image('Standing.png')
        self.state = STANDING
        self.look = DOWN
        self.frame = 0
        self.x,self.y = WINX//2, WINY//2
        self.dirX,self.dirY = 0,0


    def SetState(self,_state):
        self.state = _state

    def Draw(self):
        self.image.clip_draw((int(self.frame / 4)) * SIZE, self.look, SIZE, SIZE, self.x, self.y)


    def Update(self):
        self.frame = (self.frame + 1) % self.state[1]

        self.x += self.dirX * 8
        self.y += self.dirY * 8

class BOSS2:
    def __init__(self):
        self.image = load_image('Boss2.png')
        self.frame = 0
        self.x,self.y = WINX//2, WINY//2
        self.dirX,self.dirY = 0,0
        self.Rect = [self.x-60,self.y+50,self.x+60,self.y-70]

    def SetState(self,_state):
        self.state = _state

    def Draw(self):
        self.image.clip_draw((int(self.frame / 4)) * SIZE*3, 0, SIZE*3, SIZE*3, self.x, self.y)

    def DrawRectangle(self):
        draw_rectangle(self.Rect[0], self.Rect[1], self.Rect[2], self.Rect[3])

    def Update(self):
        self.frame = (self.frame + 1) % (4*4)

        self.x += self.dirX * 8
        self.y += self.dirY * 8

class CIRCLE:
    def __init__(self):
        self.image = load_image('Circle.png')
        self.x,self.y = WINX//2,WINY//2
        self.r = 380
        self.Rect =[[self.x - self.r + 320, self.y + self.r - 20 , self.x + self.r - 320, self.y - self.r + 20 ],
                    [self.x - self.r + 300, self.y + self.r - 25 , self.x + self.r - 300, self.y - self.r + 25 ],
                    [self.x - self.r + 275, self.y + self.r - 30 , self.x + self.r - 275, self.y - self.r + 30 ],
                    [self.x - self.r + 260, self.y + self.r - 35 , self.x + self.r - 260, self.y - self.r + 35 ],
                    [self.x - self.r + 235, self.y + self.r - 40 , self.x + self.r - 235, self.y - self.r + 40 ],
                    [self.x - self.r + 200, self.y + self.r - 55 , self.x + self.r - 200, self.y - self.r + 55 ],
                    [self.x - self.r + 180, self.y + self.r - 65 , self.x + self.r - 180, self.y - self.r + 65 ],
                    [self.x - self.r + 160, self.y + self.r - 80 , self.x + self.r - 160, self.y - self.r + 80 ],
                    [self.x - self.r + 140, self.y + self.r - 100, self.x + self.r - 140, self.y - self.r + 100],
                    [self.x - self.r + 130, self.y + self.r - 110, self.x + self.r - 130, self.y - self.r + 110],
                    [self.x - self.r + 120, self.y + self.r - 120, self.x + self.r - 120, self.y - self.r + 120],
                    [self.x - self.r + 110, self.y + self.r - 130, self.x + self.r - 110, self.y - self.r + 130],
                    [self.x - self.r + 100, self.y + self.r - 140, self.x + self.r - 100, self.y - self.r + 140],
                    [self.x - self.r + 90 , self.y + self.r - 150, self.x + self.r - 90 , self.y - self.r + 150],
                    [self.x - self.r + 80 , self.y + self.r - 160, self.x + self.r - 80 , self.y - self.r + 160],
                    [self.x - self.r + 75 , self.y + self.r - 170, self.x + self.r - 75 , self.y - self.r + 170],
                    [self.x - self.r + 70 , self.y + self.r - 180, self.x + self.r - 70 , self.y - self.r + 180],
                    [self.x - self.r + 65 , self.y + self.r - 190, self.x + self.r - 65 , self.y - self.r + 190],
                    [self.x - self.r + 60 , self.y + self.r - 200, self.x + self.r - 60 , self.y - self.r + 200],
                    [self.x - self.r + 55 , self.y + self.r - 210, self.x + self.r - 55 , self.y - self.r + 210],
                    [self.x - self.r + 50 , self.y + self.r - 220, self.x + self.r - 50 , self.y - self.r + 220],
                    [self.x - self.r + 45 , self.y + self.r - 235, self.x + self.r - 45 , self.y - self.r + 235],
                    [self.x - self.r + 40 , self.y + self.r - 245, self.x + self.r - 40 , self.y - self.r + 245],
                    [self.x - self.r + 30 , self.y + self.r - 260, self.x + self.r - 30 , self.y - self.r + 260],
                    [self.x - self.r + 25 , self.y + self.r - 300, self.x + self.r - 25 , self.y - self.r + 300],
                    [self.x - self.r + 20 , self.y + self.r - 320, self.x + self.r - 20 , self.y - self.r + 320]
                    ]


    def Draw(self):
        self.image.draw(self.x - self.r * 0.01, self.y - self.r * 0.01, WINX * 2 + self.r, WINX * 2 + self.r)

    def DrawRectangle(self):
        for i in range(len(self.Rect)):
            draw_rectangle(self.Rect[i][0],self.Rect[i][1],self.Rect[i][2],self.Rect[i][3])

    def Update(self):
        pass

Running = True
Link = LINK()
Boss1 = BOSS1()
Boss2 = BOSS2()
Circle = CIRCLE()

#원크기, 좌표


def handle_events():
    global Running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Running = False

        #키가 눌렸을 때
        elif event.type == SDL_KEYDOWN:
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



        #키를 땠을 때
        if event.type == SDL_KEYUP:
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


deltaX = 1
deltaCircle = 1
while Running:
    clear_canvas()

    Background.draw(WINX//2,WINY//2,WINX,WINY)

    #CircleX +=deltaCircle*3




    #CircleR-=1

    Circle.Draw()
    Circle.DrawRectangle()

    Link.Update()
    Link.Draw()
    Link.DrawRectangle()

    Boss2.Update()
    Boss2.Draw()
    Boss2.DrawRectangle()



    #deltaX  -= 1



    update_canvas()
    handle_events()
    delay(0.03)





