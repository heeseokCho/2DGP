from pico2d import*
import game_world

#윈도우 크기
WINX  = 1600
WINY  = 1000
#사진 크기
SIZE = 64
#방향별 사진
UP,DOWN,LEFT,RIGHT = SIZE*3, SIZE*2, SIZE*1, SIZE*0


class ARROW:
    global Link
    global Circle
    image = None

    def __init__(self):
        self.x,self.y = 0,0
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