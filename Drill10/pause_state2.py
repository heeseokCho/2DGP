import game_framework
from pico2d import*

import main_state

name = "PauseState"
image = None
frame = 0

def enter():
    global image
    image = load_image('pause.png')

def exit():
    global image
    del(image)

def handle_events():
    global frame

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type,event.key) == (SDL_KEYDOWN,SDLK_ESCAPE):
                game_framework.quit()
            elif(event.type,event.key) == (SDL_KEYDOWN,SDLK_SPACE):
                game_framework.change_state(main_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
                frame = 0
                game_framework.pop_state()


def draw():
    clear_canvas()
    main_state.boy.draw()
    main_state.grass.draw()
    if(frame % 400 < 200):
        image.clip_draw(250,250,400,400,800//2,600//2)

    update_canvas()

def update():
    global frame
    frame = (frame+1)%400

def pause():
    pass

def resume():
    pass
