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

#상태 (상태이름, 프레임개수,현재 프레임)
STANDING,WALKING,SHOOTING,AIMING,AIMWALKING,DIEING,AIMSTANDING,WINNING =\
[0,1],   [1,10], [2,6],   [3,3], [4,8],     [5,9], [6,1],       [7,1]

Background = None
Link = None
Circle = None
Boss2 = None
Arrow = []
Boss2_Bullet1 = []
Enemy = []
Boss2_Bullet2 = []
Timer = 0


class BOSS2_BULLET1:
    global Boss2
    global Link
    global Circle
    image = None

    def __init__(self):
        self.startX,self.startY = Boss2.x,Boss2.y
        self.endX,self.endY = 0,0
        self.x,self.y = Boss2.x,Boss2.y
        self. Speed = 8
        self.Rect = [self.x, self.y, self.x, self.y]
        self.angle_rotation = 0
        self.angle_target = 0
        self.angle= 0
        self.dir_rotation = 0
        self.speed = 3
        self.t = 0


        if BOSS2_BULLET1.image == None:
            BOSS2_BULLET1.image = load_image('Boss2_Bullet.png')

        if random.randint(0,1) == 1:
            self.dir_rotation = 1
        else: self.dir_rotation = -1

    def Update(self):
        self.angle_rotation += 10*self.dir_rotation

        self.t += 1/100
        self.x = (1 - self.t) * self.startX + self.t * self.endX
        self.y = (1 - self.t) * self.startY + self.t * self.endY

        self.Rect[0] = self.x-4
        self.Rect[1] = self.y+4
        self.Rect[2] = self.x+4
        self.Rect[3] = self.y-4




    def Draw(self):


        BOSS2_BULLET1.image.rotate_draw(math.radians(self.angle_rotation),self.x,self.y,SIZE/2,SIZE/2)


    def DrawRectangle(self):
        draw_rectangle(self.Rect[0],self.Rect[1],self.Rect[2],self.Rect[3])

class BOSS2_BULLET2:
    global Boss2
    global Circle
    image = None
    Direction = 0
    def __init__(self):
        self.x, self.y = Boss2.x,Boss2.y
        self.dir = BOSS2_BULLET2.Direction

        self.Rect = [self.x-SIZE//2,self.y+SIZE//2,self.x+SIZE//2,self.y-SIZE//2]
        self.speed = 5

        if BOSS2_BULLET2.image == None:
            BOSS2_BULLET2.image = load_image('Enemy.png')

    def Draw(self):
        if self.dir == 0:
            BOSS2_BULLET2.image.clip_draw(SIZE * 0, SIZE // 2 * 2, SIZE // 2, SIZE // 2, self.x, self.y)
        elif self.dir == 1:
            BOSS2_BULLET2.image.clip_draw(SIZE * 0, SIZE // 2 * 1, SIZE // 2, SIZE // 2, self.x, self.y)
        elif self.dir == 2:
            BOSS2_BULLET2.image.clip_draw(SIZE * 0, SIZE // 2 * 0, SIZE // 2, SIZE // 2, self.x, self.y)
        elif self.dir == 3:
            BOSS2_BULLET2.image.clip_draw(SIZE // 2 * 1, SIZE // 2 * 0, SIZE // 2, SIZE // 2, self.x, self.y)
        elif self.dir == 4:
            BOSS2_BULLET2.image.clip_draw(SIZE // 2 * 2, SIZE // 2 * 0, SIZE // 2, SIZE // 2, self.x, self.y)
        elif self.dir == 5:
            BOSS2_BULLET2.image.clip_draw(SIZE // 2 * 2, SIZE // 2 * 1, SIZE // 2, SIZE // 2, self.x, self.y)
        elif self.dir == 6:
            BOSS2_BULLET2.image.clip_draw(SIZE // 2 * 2, SIZE // 2 * 2, SIZE // 2, SIZE // 2, self.x, self.y)
        elif self.dir == 7:
            BOSS2_BULLET2.image.clip_draw(SIZE // 2 * 1, SIZE // 2 * 2, SIZE // 2, SIZE // 2, self.x, self.y)

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

class BOSS2:
    global Circle
    global Link
    global Boss2_Bullet1
    global Boss2_Revolution_Bullet
    global Boss2_Enemy

    def __init__(self):
        self.image = load_image('Boss2.png')
        self.frame = 0
        self.x, self.y = WINX // 2, WINY // 2 + Circle.r / 2
        self.dir = 1
        self.Rect = [self.x - 60, self.y + 50, self.x + 60, self.y - 70]
        self.timer = 0
        self.angle_rotation = 0
        self.angle_revolution = 0

    def SetState(self, _state):
        self.state = _state

    def Draw(self):

        self.image.clip_composite_draw((int(self.frame / 4)) * SIZE * 3, 0, SIZE * 3, SIZE * 3, self.angle_rotation,
                                       'a', self.x, self.y, SIZE * 3, SIZE * 3)

    def DrawRectangle(self):
        draw_rectangle(self.Rect[0], self.Rect[1], self.Rect[2], self.Rect[3])

    def Update(self):
        self.timer += 1

        if self.timer % 10 == 0:
            Boss2_Bullet1.append(BOSS2_BULLET1())
            Boss2_Bullet1.append(BOSS2_BULLET1())

            Boss2_Bullet1[-1].startX = self.x
            Boss2_Bullet1[-1].startY = self.y
            Boss2_Bullet1[-1].endX = Link.x + 500 * math.cos(
                math.atan2(Link.y - self.y, Link.x - self.x))
            Boss2_Bullet1[-1].endY = Link.y + 500 * math.sin(
                math.atan2(Link.y - self.y, Link.x - self.x))

            Boss2_Bullet1[-2].startX = self.x
            Boss2_Bullet1[-2].startY = self.y
            Boss2_Bullet1[-2].endX = Link.x + 500 * math.cos(
                -math.atan2(Link.y - self.y, Link.x - self.x))
            Boss2_Bullet1[-2].endY = Link.y + 500 * math.sin(
                -math.atan2(Link.y - self.y, Link.x - self.x))


        if self.timer % 40 == 0:
            for i in range(8):
                Boss2_Bullet2.append(BOSS2_BULLET2())
                BOSS2_BULLET2.Direction += 1
            BOSS2_BULLET2.Direction = 0

        if self.timer > 2000:
            self.timer = 1
            self.dir *= -1

        self.frame = (self.frame + 1) % (4 * 4)

        self.angle_rotation = math.atan2(Circle.y - self.y, Circle.x - self.x) * self.dir

        self.angle_revolution += self.dir * 0.02
        self.x = Circle.x + (Circle.r - SIZE) * math.cos(self.angle_revolution)
        self.y = Circle.y + (Circle.r - SIZE) * math.sin(self.angle_revolution)

        self.Rect = [self.x - 60, self.y + 50, self.x + 60, self.y - 70]

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

class BULLET:
    pass

class CIRCLE:
    global Timer

    def __init__(self):
        self.image = load_image('Circle.png')
        self.x,self.y = WINX//2,WINY//2
        self.r = 380
        self.Zoom = 0
        self.DirX,self.DirY = 0,0
        self.Speed = 0.2
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
        self.RectNum = len(self.Rect)


    def Draw(self):
        self.image.draw(self.x - self.r * 0.01, self.y - self.r * 0.01, WINX * 2 + self.r, WINX * 2 + self.r)

    def DrawRectangle(self):
        for i in range(self.RectNum):
            draw_rectangle(self.Rect[i][0],self.Rect[i][1],self.Rect[i][2],self.Rect[i][3])

    def Update(self):
        if Timer == 50:
            if random.randint(1,2) % 2 == 1:
                self.DirX = 1
            else:
                self.DirX = -1

            if random.randint(1,2) % 2 == 1:
                self.DirY = 1
            else:
                self.DirY = -1

            self.Zoom = -1

        if Timer % 100 == 0:
            self.Speed += 0.2

        self.x += self.DirX * self.Speed
        self.y += self.DirY * self.Speed
        self.r += self.Zoom * self.Speed

        if self.r < 100:
            self.Zoom = 1
        elif self.r > 400:
            self.Zoom = -1

        for i in range(self.RectNum):
            self.Rect[i][0] += self.DirX * self.Speed - self.Zoom*self.Speed/10
            self.Rect[i][2] += self.DirX * self.Speed + self.Zoom*self.Speed/10
            self.Rect[i][1] += self.DirY * self.Speed + self.Zoom*self.Speed/10
            self.Rect[i][3] += self.DirY * self.Speed - self.Zoom*self.Speed/10



        if(self.x > WINX-self.r):
            self.DirX = -1
        elif(self.x < self.r):
            self.DirX = 1
        if (self.y > WINY-200 - self.r):
            self.DirY = -1
        elif (self.y < self.r):
            self.DirY = 1

class BACKGROUND:
    def __init__(self):
        self.image = load_image('Background2.png')

    def Draw(self):
        self.image.draw(WINX // 2, WINY // 2, WINX, WINY)

    def Update(self):
        pass

def DeleteBullets():
    #보스2 탄
    DeleteBullet1 = []
    for i in Boss2_Bullet1:
        if i.x > Circle.x + 400:
            DeleteBullet1.append(i)
        elif i.x < Circle.x - 400:
            DeleteBullet1.append(i)
        if i.y > Circle.y + 400:
            DeleteBullet1.append(i)
        elif i.y < Circle.y - 400:
            DeleteBullet1.append(i)
    for i in DeleteBullet1:
        if i in Boss2_Bullet1:
            Boss2_Bullet1.remove(i)

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

    #보스2 적
    DeleteBullet2 = []
    for i in Boss2_Bullet2:
        if i.x > Circle.x + 400:
            DeleteBullet2.append(i)
        elif i.x < Circle.x - 400:
            DeleteBullet2.append(i)
        if i.y > Circle.y + 400:
            DeleteBullet2.append(i)
        elif i.y < Circle.y - 400:
            DeleteBullet2.append(i)
    for i in DeleteBullet2:
        if i in Boss2_Bullet2:
            Boss2_Bullet2.remove(i)

def enter():
    global Link,Boss1,Boss2,Circle,Background

    Background = BACKGROUND()
    Link = LINK()
    Circle = CIRCLE()
    Boss2 = BOSS2()


def exit():
    global Link, Boss1, Boss2, Circle
    del (Link)
    del(Boss1)
    del(Boss2)
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

    Link.Update()
    Boss2.Update()
    Circle.Update()
    DeleteBullets()

    for i in Arrow:
        i.Update()
    for i in Boss2_Bullet1:
        i.Update()
    for i in Boss2_Bullet2:
        i.Update()




def draw():
    clear_canvas()

    Background.Draw()

    Boss2.Draw()
    Boss2.DrawRectangle()

    if(len(Arrow) > 0):
        for i in Arrow:
            i.Draw()
            #i.DrawRectangle()

    if(len(Boss2_Bullet1) > 0):
        for i in Boss2_Bullet1:
            i.Draw()
            #i.DrawRectangle()
    if(len(Boss2_Bullet2) > 0):
        for i in Boss2_Bullet2:
            i.Draw()
            #i.DrawRectangle()

    Circle.Draw()
    #Circle.DrawRectangle()

    Link.Draw()
    #Link.DrawRectangle()





    update_canvas()
    delay(0.03)