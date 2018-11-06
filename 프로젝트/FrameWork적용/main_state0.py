from pico2d import*

import title_state
import main_state1
import main_state2

import game_framework
import game_world
import math
import random

from class_LINK import LINK
from class_BACKGROUND import BACKGROUND
from class_CIRCLE import CIRCLE
from class_STAGE0 import STAGE0

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
Stage0 = None
Bgm = None

def enter():
    global Link,Circle,Background, Stage0,Bgm

    game_world.objects = [[],[],[]]



    Background = BACKGROUND(1)
    Link = LINK()
    Stage0 = STAGE0()
    Circle = CIRCLE(0)

    game_world.add_object(Background,0)
    game_world.add_object(Circle,2)
    game_world.add_object(Link,1)
    game_world.add_object(Stage0,1)

    Bgm = load_music('Field.mp3')
    Bgm.set_volume(40)
    Bgm.repeat_play()

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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            game_framework.change_state(main_state1)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            game_framework.change_state(main_state2)

        else:
            Link.handle_event(event)

def update():
    for game_object in game_world.all_objects():
        game_object.update()

    for enemy in Stage0.enemy:
        if collide(Link,enemy):
            Stage0.enemy.remove(enemy)
            game_world.remove_object(enemy)

    for enemy in Stage0.enemy:
        for arrow in Link.arrow:
            if collide(arrow,enemy):
                Stage0.enemy.remove(enemy)
                game_world.remove_object(enemy)
                Link.arrow.remove(arrow)
                game_world.remove_object(arrow)

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()

def collide(a,b):
    left_a,bottom_a,right_a,top_a=a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a>right_b:return False
    if right_a<left_b:return False
    if top_a < bottom_a: return False
    if bottom_a > top_b : return False

    return True


