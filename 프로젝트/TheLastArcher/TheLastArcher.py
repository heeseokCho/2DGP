from pico2d import *

WINX  = 1600
WINY  = 1000
open_canvas(WINX,WINY)

x, y = WINX // 2, WINY//2
Running = True

def handle_events():
    global Running

    events = get_events()
    for event in events:
        frame = 0
        if event.type == SDL_QUIT:
            Running = False

        #키를 땠을 때
        if event.type == SDL_KEYUP:
            pass
        #키가 눌렸을 때
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                Running = False

while Running:
    clear_canvas()

    update_canvas()
    handle_events()

    delay(0.05)





