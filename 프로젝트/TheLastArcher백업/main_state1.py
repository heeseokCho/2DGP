from pico2d import*
import random
import title_state
import game_framework
import math

name = "MainState"

#윈도우 크기
WINX  = 1600
WINY  = 1000
#사진 크기
SIZE = 64
#방향별 사진
UP,DOWN,LEFT,RIGHT = SIZE*3, SIZE*2, SIZE*1, SIZE*0

#8방
LEFTUP,RIGHTUP,RIGHTDOWN,LEFTDOWN = 11,22,33,44

#상태 (상태이름, 프레임개수)
STANDING,WALKING,SHOOTING,AIMING,AIMWALKING,DIEING,AIMSTANDING,WINNING =\
[0,1],   [1,10], [2,6],   [3,3], [4,8],     [5,9], [6,1],       [7,1]

Background = None
Link = None
Circle = None
Boss1 = None
Boss1_Bullet1 = []
Boss1_Bullet2 = []
Arrow = []
Enemy = []
Timer = 0

class ENEMY:
    global Circle
    image = None
    def __init__(self):
        self.x, self.y = 0,0
        self.dir = 0
        self.dirX,self.dirY = 0,0

        self.Rect = [0,0,0,0]
        self.speed = 5

        if ENEMY.image == None:
            ENEMY.image = load_image('Enemy.png')

        if self.dir == LEFTUP or self.dir == UP or self.dir == RIGHTUP:
            self.dirY = 1
        elif self.dir == LEFTDOWN or self.dir == DOWN or self.dir == RIGHTDOWN:
            self.dirY = -1
        if self.dir == LEFTUP or self.dir == LEFT or self.dir == LEFTDOWN:
            self.dirX= -1
        elif self.dir == RIGHTUP or self.dir == RIGHT or self.dir == RIGHTDOWN:
            self.dirX = 1

    def Draw(self):
        if self.dir == LEFTUP:
            ENEMY.image.clip_draw(0,64, SIZE/2, SIZE/2, self.x, self.y)
        elif self.dir == UP:
            ENEMY.image.clip_draw(32,64, SIZE/2, SIZE/2, self.x, self.y)
        elif self.dir == RIGHTUP:
            ENEMY.image.clip_draw(64,64, SIZE/2, SIZE/2, self.x, self.y)
        elif self.dir == RIGHT:
            ENEMY.image.clip_draw(64,32, SIZE/2, SIZE/2, self.x, self.y)
        elif self.dir == RIGHTDOWN:
            ENEMY.image.clip_draw(64,0, SIZE/2, SIZE/2, self.x, self.y)
        elif self.dir == DOWN:
            ENEMY.image.clip_draw(32,0, SIZE/2, SIZE/2, self.x, self.y)
        elif self.dir == LEFTDOWN:
            ENEMY.image.clip_draw(0,0, SIZE/2, SIZE/2, self.x, self.y)
        elif self.dir == LEFT:
            ENEMY.image.clip_draw(0,32, SIZE/2, SIZE/2, self.x, self.y)

    def DrawRectangle(self):
        draw_rectangle(self.Rect[0],self.Rect[1],self.Rect[2],self.Rect[3])

    def Update(self):

        self.x += self.dirX * self.speed
        self.y += self.dirY * self.speed

class ARROW:
    global Link
    global Circle
    image = None

    def __init__(self):
        self.x,self.y = Link.x,Link.y
        self.Dir = None
        self.Speed = 10
        #좌상우하
        self.Rect = [self.x,self.y,self.x,self.y]

        if ARROW.image == None:
            ARROW.image = load_image('Arrow.png')

    def Update(self):
        if self.Dir == UP:
            self.y += self.Speed
        elif self.Dir == DOWN:
            self.y -=self.Speed
        elif self.Dir == LEFT:
            self.x -=self.Speed
        elif self.Dir == RIGHT:
            self.x +=self.Speed

        if self.Dir == UP:
            self.Rect = [self.x - 4, self.y + 16, self.x + 4, self.y + 8]
        elif self.Dir == DOWN:
            self.Rect = [self.x - 4, self.y - 8, self.x + 4, self.y - 16]
        elif self.Dir == LEFT:
            self.Rect = [self.x - 16, self.y + 4, self.x - 8, self.y - 4]
        elif self.Dir == RIGHT:
            self.Rect = [self.x + 8, self.y + 4, self.x + 16, self.y - 4]


    def Draw(self):
        ARROW.image.clip_draw(0, self.Dir//2,SIZE//2, SIZE//2, self.x, self.y)

    def DrawRectangle(self):
        draw_rectangle(self.Rect[0],self.Rect[1],self.Rect[2],self.Rect[3])

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

class BOSS1_BULLET1:
    image = None
    def __init__(self):
        self.x = random.randint(100,WINX-100)
        self.y = random.randint(100,WINY-300)
        self.Rect = [self.x-SIZE/4,self.y+SIZE/4,self.x+SIZE/4,self.y-SIZE/4]
        self.timer = 0

        if BOSS1_BULLET1.image == None:
            BOSS1_BULLET1.image = load_image('Boss1Bullet1.png')

    def Draw(self):
        BOSS1_BULLET1.image.draw(self.x,self.y,SIZE,SIZE)

    def DrawRectangle(self):
        draw_rectangle(self.Rect[0],self.Rect[1],self.Rect[2],self.Rect[3])

    def Update(self):
        self. timer += 1

        if self.timer % 160 == 0:
            self.timer = 0


            if random.randint(0, 1) == 1:
                BOSS1_BULLET2.Direction = 1

            for i in range(4):

                Boss1_Bullet2.append(BOSS1_BULLET2())
                Boss1_Bullet2[-1].x = self.x
                Boss1_Bullet2[-1].y = self.y
                BOSS1_BULLET2.Direction = BOSS1_BULLET2.Direction + 2

            BOSS1_BULLET2.Direction = 0

class BOSS1_BULLET2:
    global Boss1
    image = None
    Direction = 0

    def __init__(self):
        self.x,self.y = Boss1.x,Boss1.y
        self.dir = BOSS1_BULLET2.Direction
        self.speed = 4
        self.Rect = [self.x-SIZE//8,self.y+SIZE//8,self.x+SIZE//8,self.y-SIZE//8]

        if BOSS1_BULLET2.image == None:
            BOSS1_BULLET2.image = load_image('Boss1Bullet2.png')

    def Draw(self):
        if self.dir == 0:
            BOSS1_BULLET2.image.clip_draw(SIZE*0,SIZE//2*2,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == 1:
            BOSS1_BULLET2.image.clip_draw(SIZE*0,SIZE//2*1,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == 2:
            BOSS1_BULLET2.image.clip_draw(SIZE*0,SIZE//2*0,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == 3:
            BOSS1_BULLET2.image.clip_draw(SIZE//2*1,SIZE//2*0,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == 4:
            BOSS1_BULLET2.image.clip_draw(SIZE//2*2,SIZE//2*0,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == 5:
            BOSS1_BULLET2.image.clip_draw(SIZE//2*2,SIZE//2*1,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == 6:
            BOSS1_BULLET2.image.clip_draw(SIZE//2*2,SIZE//2*2,SIZE//2,SIZE//2,self.x,self.y)
        elif self.dir == 7:
            BOSS1_BULLET2.image.clip_draw(SIZE//2*1,SIZE//2*2,SIZE//2,SIZE//2,self.x,self.y)

    def DrawRectangle(self):
        draw_rectangle(self.Rect[0],self.Rect[1],self.Rect[2],self.Rect[3])

    def Update(self):
        if self.dir == 0:
            self.x -= self.speed
            self.y += self.speed
        elif self.dir == 1:
            self.x -= self.speed
        elif self.dir == 2:
            self.x -= self.speed
            self.y -= self.speed
        elif self.dir == 3:
            self.y -= self.speed
        elif self.dir == 4:
            self.x += self.speed
            self.y -= self.speed
        elif self.dir == 5:
            self.x += self.speed
        elif self.dir == 6:
            self.x += self.speed
            self.y += self.speed
        elif self.dir == 7:
            self.y += self.speed

        self.Rect = [self.x - SIZE // 8, self.y + SIZE // 8, self.x + SIZE // 8, self.y - SIZE // 8]

class BOSS1:
    global Boss1_Bullet1
    global Boss2_Bullet2

    def __init__(self):
        self.image = load_image('Boss1.png')
        self.frame = 0
        self.x,self.y = WINX//2, WINY//2
        self.dirX,self.dirY = 0,0
        self.timer = 0


    def SetState(self,_state):
        self.state = _state

    def Draw(self):
        self.image.clip_draw((int(self.frame / 10)) * SIZE*3, 0, SIZE*3, SIZE*3, self.x, self.y)


    def Update(self):
        self.timer+=1
        self.frame = (self.frame + 1) % (5*10)

        if self.frame == 4:
            Boss1_Bullet1.append(BOSS1_BULLET1())

        if self.timer%160 ==0:
            self.timer = 0
            for i in range(8):
                Boss1_Bullet2.append(BOSS1_BULLET2())
                BOSS1_BULLET2.Direction = (BOSS1_BULLET2.Direction+1)%8




class BULLET:
    pass

class CIRCLE:
    global Timer

    def __init__(self):
        self.image = load_image('Circle.png')
        self.x,self.y = WINX//2+500,WINY//2
        self.r = 300
        self.dir =1
        self.angle_revolution = 0
        self.speed = 0.005
        self.Rect = [[self.x - self.r + 320 - 70, self.y + self.r - 20 + 70, self.x + self.r - 320 + 70,self.y - self.r + 20 - 70],
                     [self.x - self.r + 300 - 70, self.y + self.r - 25 + 70, self.x + self.r - 300 + 70,self.y - self.r + 25 - 70],
                     [self.x - self.r + 275 - 70, self.y + self.r - 30 + 70, self.x + self.r - 275 + 70,self.y - self.r + 30 - 70],
                     [self.x - self.r + 260 - 70, self.y + self.r - 35 + 70, self.x + self.r - 260 + 70,self.y - self.r + 35 - 70],
                     [self.x - self.r + 235 - 70, self.y + self.r - 40 + 70, self.x + self.r - 235 + 70,self.y - self.r + 40 - 70],
                     [self.x - self.r + 200 - 70, self.y + self.r - 55 + 70, self.x + self.r - 200 + 70,self.y - self.r + 55 - 70],
                     [self.x - self.r + 180 - 70, self.y + self.r - 65 + 70, self.x + self.r - 180 + 70,self.y - self.r + 65 - 70],
                     [self.x - self.r + 160 - 70, self.y + self.r - 80 + 70, self.x + self.r - 160 + 70,self.y - self.r + 80 - 70],
                     [self.x - self.r + 140 - 70, self.y + self.r - 100 + 70, self.x + self.r - 140 + 70,self.y - self.r + 100 - 70],
                     [self.x - self.r + 130 - 70, self.y + self.r - 110 + 70, self.x + self.r - 130 + 70,self.y - self.r + 110 - 70],
                     [self.x - self.r + 120 - 70, self.y + self.r - 120 + 70, self.x + self.r - 120 + 70,self.y - self.r + 120 - 70],
                     [self.x - self.r + 110 - 70, self.y + self.r - 130 + 70, self.x + self.r - 110 + 70, self.y - self.r + 130 - 70],
                     [self.x - self.r + 100 - 70, self.y + self.r - 140 + 70, self.x + self.r - 100 + 70,self.y - self.r + 140 - 70],
                     [self.x - self.r + 90 - 70, self.y + self.r - 150 + 70, self.x + self.r - 90 + 70,self.y - self.r + 150 - 70],
                     [self.x - self.r + 80 - 70, self.y + self.r - 160 + 70, self.x + self.r - 80 + 70,self.y - self.r + 160 - 70],
                     [self.x - self.r + 75 - 70, self.y + self.r - 170 + 70, self.x + self.r - 75 + 70,self.y - self.r + 170 - 70],
                     [self.x - self.r + 70 - 70, self.y + self.r - 180 + 70, self.x + self.r - 70 + 70,self.y - self.r + 180 - 70],
                     [self.x - self.r + 65 - 70, self.y + self.r - 190 + 70, self.x + self.r - 65 + 70,self.y - self.r + 190 - 70],
                     [self.x - self.r + 60 - 70, self.y + self.r - 200 + 70, self.x + self.r - 60 + 70,self.y - self.r + 200 - 70],
                     [self.x - self.r + 55 - 70, self.y + self.r - 210 + 70, self.x + self.r - 55 + 70,self.y - self.r + 210 - 70],
                     [self.x - self.r + 50 - 70, self.y + self.r - 220 + 70, self.x + self.r - 50 + 70,self.y - self.r + 220 - 70],
                     [self.x - self.r + 45 - 70, self.y + self.r - 235 + 70, self.x + self.r - 45 + 70,self.y - self.r + 235 - 70],
                     [self.x - self.r + 40 - 70, self.y + self.r - 245 + 70, self.x + self.r - 40 + 70,self.y - self.r + 245 - 70],
                     [self.x - self.r + 30 - 70, self.y + self.r - 260 + 70, self.x + self.r - 30 + 70,self.y - self.r + 260 - 70],
                     [self.x - self.r + 25 - 70, self.y + self.r - 300 + 70, self.x + self.r - 25 + 70,self.y - self.r + 300 - 70],
                     [self.x - self.r + 20 - 70, self.y + self.r - 320 + 70, self.x + self.r - 20 + 70,self.y - self.r + 320 - 70]]
        self.RectNum = len(self.Rect)
        self.timer = 0


    def Draw(self):
        self.image.draw(self.x - self.r * 0.01, self.y - self.r * 0.01, WINX * 2 + self.r, WINX * 2 + self.r)

    def DrawRectangle(self):
        for i in range(self.RectNum):
            draw_rectangle(self.Rect[i][0],self.Rect[i][1],self.Rect[i][2],self.Rect[i][3])

    def Update(self):
        if Timer == 5000:
            if random.randint(0,1) == 0:
                self.dir *= -1

        self.angle_revolution += self.dir * self.speed
        self.x = WINX//2 + self.r * math.cos(self.angle_revolution)
        self.y = WINY//2 + self.r * math.sin(self.angle_revolution)

        if Timer % 1000 == 0:
            self.speed += 0.005

        self.Rect = [[self.x - self.r +320-70, self.y + self.r - 20 +70, self.x + self.r - 320+70, self.y - self.r + 20 -70],
                    [self.x - self.r + 300-70, self.y + self.r - 25 +70, self.x + self.r - 300+70, self.y - self.r + 25 -70],
                    [self.x - self.r + 275-70, self.y + self.r - 30 +70, self.x + self.r - 275+70, self.y - self.r + 30 -70],
                    [self.x - self.r + 260-70, self.y + self.r - 35 +70, self.x + self.r - 260+70, self.y - self.r + 35 -70],
                    [self.x - self.r + 235-70, self.y + self.r - 40 +70, self.x + self.r - 235+70, self.y - self.r + 40 -70],
                    [self.x - self.r + 200-70, self.y + self.r - 55 +70, self.x + self.r - 200+70, self.y - self.r + 55 -70],
                    [self.x - self.r + 180-70, self.y + self.r - 65 +70, self.x + self.r - 180+70, self.y - self.r + 65 -70],
                    [self.x - self.r + 160-70, self.y + self.r - 80 +70, self.x + self.r - 160+70, self.y - self.r + 80 -70],
                    [self.x - self.r + 140-70, self.y + self.r - 100+70, self.x + self.r - 140+70, self.y - self.r + 100-70],
                    [self.x - self.r + 130-70, self.y + self.r - 110+70, self.x + self.r - 130+70, self.y - self.r + 110-70],
                    [self.x - self.r + 120-70, self.y + self.r - 120+70, self.x + self.r - 120+70, self.y - self.r + 120-70],
                    [self.x - self.r + 110-70, self.y + self.r - 130+70, self.x + self.r - 110+70, self.y - self.r + 130-70],
                    [self.x - self.r + 100-70, self.y + self.r - 140+70, self.x + self.r - 100+70, self.y - self.r + 140-70],
                    [self.x - self.r + 90 -70, self.y + self.r - 150+70, self.x + self.r - 90 +70, self.y - self.r + 150-70],
                    [self.x - self.r + 80 -70, self.y + self.r - 160+70, self.x + self.r - 80 +70, self.y - self.r + 160-70],
                    [self.x - self.r + 75 -70, self.y + self.r - 170+70, self.x + self.r - 75 +70, self.y - self.r + 170-70],
                    [self.x - self.r + 70 -70, self.y + self.r - 180+70, self.x + self.r - 70 +70, self.y - self.r + 180-70],
                    [self.x - self.r + 65 -70, self.y + self.r - 190+70, self.x + self.r - 65 +70, self.y - self.r + 190-70],
                    [self.x - self.r + 60 -70, self.y + self.r - 200+70, self.x + self.r - 60 +70, self.y - self.r + 200-70],
                    [self.x - self.r + 55 -70, self.y + self.r - 210+70, self.x + self.r - 55 +70, self.y - self.r + 210-70],
                    [self.x - self.r + 50 -70, self.y + self.r - 220+70, self.x + self.r - 50 +70, self.y - self.r + 220-70],
                    [self.x - self.r + 45 -70, self.y + self.r - 235+70, self.x + self.r - 45 +70, self.y - self.r + 235-70],
                    [self.x - self.r + 40 -70, self.y + self.r - 245+70, self.x + self.r - 40 +70, self.y - self.r + 245-70],
                    [self.x - self.r + 30 -70, self.y + self.r - 260+70, self.x + self.r - 30 +70, self.y - self.r + 260-70],
                    [self.x - self.r + 25 -70, self.y + self.r - 300+70, self.x + self.r - 25 +70, self.y - self.r + 300-70],
                    [self.x - self.r + 20 -70, self.y + self.r - 320+70, self.x + self.r - 20 +70, self.y - self.r + 320-70] ]



class BACKGROUND:
    def __init__(self):
        self.image = load_image('Background.png')

    def Draw(self):
        self.image.draw(WINX // 2, WINY // 2, WINX, WINY)

    def Update(self):
        pass


def DeleteBullets():
    #링크 화살

    DeleteArrow = []
    for i in Arrow:
        if i.x > Circle.x + 400:
            DeleteArrow.append(i)
        elif i.x < Circle.x - 400:
            DeleteArrow.append(i)
        if i.y > Circle.y + 400:
            DeleteArrow.append(i)
        elif i.y < Circle.y - 400:
            DeleteArrow.append(i)

    for i in DeleteArrow:
        if i in Arrow:
            Arrow.remove(i)


    DeleteBullet2 = []
    for i in Boss1_Bullet2:
        if i.x > Circle.x + 400:
            DeleteBullet2.append(i)
        elif i.x < Circle.x - 400:
            DeleteBullet2.append(i)
        if i.y > Circle.y + 400:
            DeleteBullet2.append(i)
        elif i.y < Circle.y - 400:
            DeleteBullet2.append(i)

    for i in DeleteBullet2:
        if i in Boss1_Bullet2:
            Boss1_Bullet2.remove(i)



def enter():
    global Link,Boss1,Boss2,Circle,Background

    Background = BACKGROUND()
    Link = LINK()
    Circle = CIRCLE()
    Boss1 = BOSS1()


def exit():
    global Link, Boss1, Boss2, Circle
    del (Link)
    del(Boss1)
    del(Circle)
    del(Arrow)

def pause():
    pass

def resume():
    pass

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
                game_framework.change_state(title_state)

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

def update():
    global Timer

    Timer +=1

    if Timer > 9999:
        Timer = 0

    Link.Update()
    Boss1.Update()
    Circle.Update()
    DeleteBullets()

    for i in Arrow:
        i.Update()
    for i in Boss1_Bullet1:
        i.Update()
    for i in Boss1_Bullet2:
        i.Update()



def draw():
    clear_canvas()

    Background.Draw()

    Boss1.Draw()

    for i in Boss1_Bullet1:
        i.Draw()
        i.DrawRectangle()

    for i in Boss1_Bullet2:
        i.Draw()
        #i.DrawRectangle()

    if(len(Arrow) > 0):
        for i in Arrow:
            i.Draw()
            i.DrawRectangle()


    Circle.Draw()
    #Circle.DrawRectangle()

    Link.Draw()
    #Link.DrawRectangle()





    update_canvas()
    delay(0.03)