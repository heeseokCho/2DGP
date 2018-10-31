from pico2d import*
import game_world

WINX,WINY = 1600,900
SIZE = 64

class ARROW:
    image = None
    def __init(self,x = 800,y = 450,velocity = 1):
        if ARROW.image == None:
            ARROW.image = load_image('Arrow.png')
            self.x,self.y,self.velocity = x,y,velocity

    def draw(self):
        self.image.draw(self.x,self.y)

    def update(self):
        self.x += self.velocity

        if self.x <SIZE or self.x > 1600-SIZE:
            game_world.remove_object(self)