import random
import json
import pickle
import os

from pico2d import *
import game_framework
import game_world

import world_build_state
name = "RankingState"

ranking = []
font = None

def enter():
    # game world is prepared already in world_build_state
    global font
    font = load_font('ENCR10B.TTF',20)
    load_ranking()

def exit():
    pass

def pause():
    pass


def resume():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(world_build_state)


def update():
    pass


def draw():
    global ranking
    global font

    clear_canvas()
    space = 0
    for data in ranking:
        space += 20
        font.draw(100,800-space,'# %d Time: %3.2f' % (data[0],data[1]),(0,0,0))
    update_canvas()

def load_ranking():
    global ranking

    with open('ranking_data.json','r')as f:
        ranking = json.load(f)






