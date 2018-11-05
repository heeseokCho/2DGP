from pico2d import*

import title_state
import main_state0
import main_state2

import game_framework
import game_world
import math
import random

from class_LINK import LINK
from class_BOSS1 import BOSS1
from class_BACKGROUND import BACKGROUND
from class_CIRCLE import CIRCLE

name = "MainState"

#윈도우 크기
WINX  = 1600
WINY  = 1000
#사진 크기
SIZE = 64
#방향별 사진
UP,DOWN,LEFT,RIGHT = SIZE*3, SIZE*2, SIZE*1, SIZE*0

Background = None
Link = None
Circle = None
Boss1 = None
Bgm = None

def enter():
    global Link,Circle,Background,Bgm
    game_world.objects = [[], [], []]

    Background = BACKGROUND(1)
    Link = LINK()
    Boss1 = BOSS1()
    Circle = CIRCLE(1)

    Bgm = load_music('BossBattle1.mp3')
    Bgm.set_volume(40)
    Bgm.repeat_play()

    game_world.add_object(Background,0)
    game_world.add_object(Boss1,1)
    game_world.add_object(Circle,2)
    game_world.add_object(Link,1)

def exit():
    game_world.clear()

def pause():
    pass

def resume():
    pass

def handle_events():
    global Running
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_0:
            game_framework.change_state(main_state0)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            game_framework.change_state(main_state2)
        else:
            Link.handle_event(event)

def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()

