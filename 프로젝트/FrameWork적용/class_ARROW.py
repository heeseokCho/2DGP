from pico2d import*
import game_world
import game_framework
import class_LINK

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
    global Link,Circle
    image = None

    def __init__(self,x = 0,y = 0,dir = 0):
        if ARROW.image == None:
            ARROW.image = load_image('Arrow.png')

        self.x,self.y = x,y
        self.velocity = RUN_SPEED_PPS*game_framework.frame_time
        self.dir = dir


    def draw(self):
        ARROW.image.clip_draw(0, self.dir//2, SIZE // 2, SIZE // 2, self.x, self.y)

    def draw_rect(self):
        pass


    def update(self):

        if self.dir == UP:
            self.y += self.velocity
        elif self.dir == DOWN:
            self.y -= self.velocity
        elif self.dir == LEFT:
            self.x -= self.velocity
        elif self.dir == RIGHT:
            self.x += self.velocity

        if self.x < SIZE//2 or self.x > WINX-SIZE//2 or self.y <SIZE//2 or self.y > WINY-SIZE//2:
            game_world.remove_object(self)

    def update_rect(self):
        pass
