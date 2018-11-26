import random
import json
import pickle
import os

from pico2d import *
import game_framework
import game_world

import world_build_state
from boy import Boy
name = "RankingState"

boy = None

def enter():
    # game world is prepared already in world_build_state
    global boy
    boy = world_build_state.get_boy()

    game_world.load()
    for o in game_world.all_objects():
        if isinstance(o,Boy):
            boy = o

def exit():
    game_world.clear()

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
    clear_canvas()

    update_canvas()








