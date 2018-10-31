from pico2d import*
import game_world

#윈도우크기
WINX,WINY = 1600,1000
#사진 크기
SIZE = 64
#방향별 사진
UP,DOWN,LEFT,RIGHT = SIZE*3, SIZE*2, SIZE*1, SIZE*0


class ARROW:
    global Link,Circle
    image = None

    def __init__(self,x = 0,y = 0,dir = DOWN,velocity = 1):
        if ARROW.image == None:
            ARROW.image = load_image('Arrow.png')

        self.x,self.y = x,y
        self.velocity = velocity
        self.dir = dir


    def draw(self):
        ARROW.image.clip_draw(0, self.dir // 2, SIZE // 2, SIZE // 2, self.x, self.y)

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

        if self.x < SIZE or self.x > WINX-SIZE or self.y <SIZE or self.y > WINY-SIZE:
            game_world.remove_object(self)

    def update_rect(self):
        pass
