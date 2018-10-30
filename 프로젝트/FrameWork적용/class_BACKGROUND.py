from pico2d import*

#윈도우 크기
WINX  = 1600
WINY  = 1000

class BACKGROUND:
    def __init__(self):
        self.image = load_image('Background.png')

    def Draw(self):
        self.image.draw(WINX // 2, WINY // 2, WINX, WINY)

    def Update(self):
        pass