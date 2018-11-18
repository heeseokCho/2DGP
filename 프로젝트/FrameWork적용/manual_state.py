import game_framework
from pico2d import*
import title_state

name = "TitleState"

image = None


#윈도우 크기
WINX  = 1600
WINY  = 1000

def enter():
    global image

    image = load_image('InGame.png')

def exit():
    global image
    del (image)

def handle_events():
    global phase
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()

def draw():
    clear_canvas()
    image.draw(WINX//2,WINY//2)

    update_canvas()

def update():
    pass


def pause():
    pass


def resume():
    pass