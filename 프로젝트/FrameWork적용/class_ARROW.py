from pico2d import*
import game_world
import game_framework

#윈도우크기
WINX,WINY = 1600,1000
#사진 크기
SIZE = 64
#방향별 사진
UP,DOWN,LEFT,RIGHT = SIZE*3, SIZE*2, SIZE*1, SIZE*0


#Link Run Speed
PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 25.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

class ARROW:
    image = None

    def __init__(self,x = 0,y = 0,dir = 0):
        if ARROW.image == None:
            ARROW.image = load_image('Arrow.png')

        self.x,self.y = x,y
        self.velocity = RUN_SPEED_PPS
        self.dir = dir


    def draw(self):
        ARROW.image.clip_draw(0, self.dir//2, SIZE // 2, SIZE // 2, self.x, self.y)

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.dir ==UP:
            return self.x-4,self.y+8,self.x+4,self.y+16
        elif self.dir == DOWN:
            return self.x - 10, self.y - 10, self.x + 10, self.y + 10
        elif self.dir == LEFT:
            return self.x - 10, self.y - 10, self.x + 10, self.y + 10
        elif self.dir == RIGHT:
            return self.x - 10, self.y - 10, self.x + 10, self.y + 10



    def update(self):

        if self.dir == UP:
            self.y += self.velocity*game_framework.frame_time
        elif self.dir == DOWN:
            self.y -= self.velocity*game_framework.frame_time
        elif self.dir == LEFT:
            self.x -= self.velocity*game_framework.frame_time
        elif self.dir == RIGHT:
            self.x += self.velocity*game_framework.frame_time

        if self.x <SIZE or self.x > WINX-SIZE or self.y <SIZE or self. y >WINY-SIZE:
            game_world.remove_object(self)

