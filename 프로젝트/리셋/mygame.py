import game_framework
from pico2d import*

import title_state
WINX = 1600
WINY = 900

open_canvas(WINX,WINY)
game_framework.run(title_state)
close_canvas()