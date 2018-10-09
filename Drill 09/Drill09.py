from pico2d import *
import random


# Game object class here
class Grass:
    def __init__(self):
        self.image = load_image('grass.png')
    def draw(self):
        self.image.draw(400,30)

class Boy:
    def __init__(self):
        self.x,self.y = 0,90
        self.frame = 0
        self.image = load_image('run_animation.png')

    def update(self):
        self.frame = (self.frame+1)%8
        self.x +=5

    def draw(self):
        self.image.clip_draw(self.frame*100,0,100,100,self.x,self.y)

class Ball:
    def __init__(self):
        if (random.randint(0,1) % 2 == 0):
            self.image= load_image('ball21x21.png')
            self.size = 21/2
        else:
            self.image = load_image('ball41x41.png')
            self.size = 41 / 2

        self.x,self.y = random.randint(100,700),600
        self.speed = random.randint(2,7)

    def update(self):
        self.y -= self.speed
        if(self.y < 50+self.size):
            self.y = 50+self.size

    def draw(self):
        self.image.draw(self.x,self.y)

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

# initialization code
open_canvas()

team = [Boy() for i in range(11)]
balls = [Ball() for i in range(20)]
grass = Grass()

running = True

# game main loop code

while running:
    handle_events()
    clear_canvas()

    grass.draw()
    for boy in team:
        boy.update()
    for boy in team:
        boy.draw()

    for ball in balls:
        ball.update()
    for ball in balls:
        ball.draw()

    update_canvas()

    delay(0.05)

# finalization code
close_canvas()