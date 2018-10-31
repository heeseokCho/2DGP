from pico2d import*
import random
import math

#윈도우 크기
WINX  = 1600
WINY  = 1000

PI = 3.141592

class State0State:
    pass

class Stage1State:
    pass

class State2State:
    pass



class CIRCLE:

    def __init__(self):
        self.image = load_image('Circle.png')

        self.stage = 1

        if self.stage == 1:
            self.x,self.y = WINX//2+500,WINY//2
            self.r = 300
            self.dir =1
            self.angle_revolution = 0
            self.speed = 0.005
            self.timer = 0
        else:
            pass


    def draw(self):
        if self.stage == 1:
            self.image.draw(self.x - self.r * 0.01, self.y - self.r * 0.01, WINX * 2 + self.r, WINX * 2 + self.r)
        else:
            pass

    def draw_rect(self):
        pass

    def update(self):
        if self.stage == 1:
            if self.timer == 5000:
                if random.randint(0,1) == 0:
                    self.dir *= -1

            self.angle_revolution += self.dir * self.speed
            self.x = WINX//2 + self.r * math.cos(self.angle_revolution)
            self.y = WINY//2 + self.r * math.sin(self.angle_revolution)

            if self.timer % 1000 == 0:
                self.speed += 0.005

    def update_rect(self):
        pass