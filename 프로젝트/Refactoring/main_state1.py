from pico2d import*

import title_state
import main_state_bonus
import main_state2

import game_framework
import game_world
import math
import random

from class_LINK import LINK
from class_ARROW import ARROW
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
    global Link,Circle,Background,Boss1,Bgm
    game_world.objects = [[], [], []]

    Background = BACKGROUND(0)
    Link = LINK()
    Boss1 = BOSS1()
    Circle = CIRCLE(1)

    Bgm = load_music('BossBattle1.ogg')
    Bgm.set_volume(40)
    Bgm.repeat_play()

    game_world.add_object(Background,0)
    game_world.add_object(Boss1,1)
    game_world.add_object(Circle,2)
    game_world.add_object(Link,1)

def exit():
    BOSS1.bullet1 = []
    BOSS1.bullet2 = []
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
            game_framework.change_state(main_state_bonus)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            game_framework.change_state(main_state2)
        else:
            Link.handle_event(event)

def update():
    for game_object in game_world.all_objects():
        game_object.update()

    if Link.cur_state != Link.collide_able == True:
        collide_objects()

    if LINK.cur_stage == 2:
        game_framework.change_state(main_state_bonus)

    if Link.end == True:
        Link.reset_all()
        game_framework.change_state(title_state)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()

def collide(a,b):
    left_a,bottom_a,right_a,top_a= a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def collideout_circle():
    left_b, bottom_b, right_b, top_b = Circle.get_bb()

    #right_b- CIRCLE.x = bb.r
    if (LINK.x-CIRCLE.x)**2+(LINK.y-CIRCLE.y)**2 >\
            (right_b-CIRCLE.x)**2:
        return True


def collide_objects():
    if collideout_circle():
        if not Link.invincibility:
            LINK.life -= 1
        Link.invincibility_time = get_time()
        Link.invincibility = True

    #적과 화살 충돌
    for arrow in Link.arrow:
        if collide(Boss1,arrow):
            LINK.arrow.remove(arrow)
            Boss1.life -= ARROW.damage
            game_world.remove_object(arrow)

    #링크와 지뢰 충돌
    for bullet1 in BOSS1.bullet1:
        if collide(Link,bullet1):
            BOSS1.bullet1.remove(bullet1)
            game_world.remove_object(bullet1)
            if not Link.invincibility:
                LINK.life -= 1
            Link.invincibility_time = get_time()
            Link.invincibility = True

    #링크와 적탄 충돌
    for bullet2 in BOSS1.bullet2:
        if collide(Link,bullet2):
            BOSS1.bullet2.remove(bullet2)
            game_world.remove_object(bullet2)
            if not Link.invincibility:
                LINK.life -= 1
            Link.invincibility_time = get_time()
            Link.invincibility = True

    LINK.life = clamp(0,LINK.life,3)
