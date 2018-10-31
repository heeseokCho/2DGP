from pico2d import*

WINX,WINY = 1600,900

class BACKGROUND:
    def __init__(self):
        self.image = load_image('Background.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(WINX//2,WINY//2,WINX,WINY)