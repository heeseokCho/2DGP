from pico2d import*
import random

#윈도우 크기
WINX  = 1600
WINY  = 1000

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