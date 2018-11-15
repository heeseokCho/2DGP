from pico2d import*

import title_state
import main_state1
import main_state2

import game_framework
import game_world

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



def enter():
    global Link,Circle,Background, Stage0,Bgm

    game_world.objects = [[],[],[]]

    Background = None
    Link = None
    Circle = None
    Stage0 = None
    Bgm = None


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
    STAGE0.enemy = []
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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_5:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            game_framework.change_state(main_state1)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            game_framework.change_state(main_state2)

        else:
            Link.handle_event(event)

def update():
    for game_object in game_world.all_objects():
        game_object.update()

    if Link.cur_state != Link.collide_able == True:
        collide_objects()

    if LINK.cur_stage == 1:
        game_framework.change_state(main_state1)
    elif LINK.cur_stage == 2:
        game_framework.change_state(main_state2)


    if Link.end == True:
        Link.reset()
        game_framework.change_state(title_state)

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()

def collide(a,b):
    left_a,bottom_a,right_a,top_a=a.get_bb()
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
        print("Circle Out")

    #링크와 적의 충돌
    for enemy in Stage0.enemy:
        if collide(Link,enemy):
            print("collide with enemy")
            Stage0.enemy.remove(enemy)
            game_world.remove_object(enemy)
            LINK.life -=1
            break


    #화살과 적의 충돌
    for arrow in Link.arrow:
        for enemy in STAGE0.enemy:
            if collide(arrow,enemy):
                Stage0.enemy.remove(enemy)
                LINK.arrow.remove(arrow)
                game_world.remove_object(enemy)
                game_world.remove_object(arrow)
                break

    #링크와 아이템의 충돌
    for item in STAGE0.item:
        if collide(Link,item):
            # RunSpeed, ArrowSpeed, Heart
            if item.kind == 0:
                LINK.run_speed += 1
                LINK.run_speed = clamp(0,LINK.run_speed,3)
            elif item.kind == 1:
                LINK.arrow_speed += 1
                LINK.arrow_speed = clamp(0, LINK.arrow_speed, 3)
            elif item.kind == 2:
                LINK.life +=1

            Stage0.item.remove(item)
            game_world.remove_object(item)

    LINK.life = clamp(0,LINK.life,3)




