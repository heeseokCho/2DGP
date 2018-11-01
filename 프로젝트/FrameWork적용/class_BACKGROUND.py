from pico2d import*

#윈도우 크기
WINX  = 1600
WINY  = 1000

class BACKGROUND():
    global phase

    def __init__(self,phase = 0):
        if phase == 1:
            self.image = load_image('Background.png')

        elif phase == 2:
            self.image = load_image('Background2.png')

    def draw(self):
        self.image.draw(WINX // 2, WINY // 2, WINX, WINY)

    def update(self):
        pass