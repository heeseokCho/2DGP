import game_framework
from pico2d import*
import main_state1
import main_state2
import main_state0

name = "TitleState"

Main_image = None
Title_image = None
Start_image = None
Manual_image = None
Exit_image = None
Bgm = None


#윈도우 크기
WINX  = 1600
WINY  = 1000

def enter():
    global Main_image
    global Title_image
    global Start_image
    global Manual_image
    global Exit_image
    global Bgm


    Main_image = load_image('Main.png')
    Title_image = load_image('Title.png')
    Start_image = load_image('Start.png')
    Manual_image = load_image('Manual.png')
    Exit_image = load_image('Exit.png')

    Bgm = load_music('MainMenu.mp3')
    Bgm.set_volume(30)
    Bgm.repeat_play()

def exit():
    global Main_image
    del (Main_image)
    global Title_image
    del (Title_image)
    global Start_image
    del (Start_image)
    global Manual_image
    del (Manual_image)
    global Exit_image
    del (Exit_image)

def handle_events():
    global phase
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
                game_framework.change_state(main_state1)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
                game_framework.change_state(main_state2)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_0):
                game_framework.change_state(main_state0)

def draw():
    clear_canvas()
    Main_image.draw(WINX//2,WINY//2)
    Title_image.draw(500,800)
    Start_image.draw(250,600)
    Manual_image.draw(300,400)
    Exit_image.draw(350,200)
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass