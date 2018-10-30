from pico2d import*

#윈도우 크기
WINX  = 1600
WINY  = 1000

class BACKGROUND:
    def __init__(self):
        self.image = load_image('Background.png')

    def draw(self):
        self.image.draw(WINX // 2, WINY // 2, WINX, WINY)

    def update(self):
        pass