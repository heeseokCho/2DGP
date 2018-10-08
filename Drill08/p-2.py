from pico2d import*
import random

KPU_WIDTH, KPU_HEIGHT = 1280, 1024


def handle_events():
    global running
    global x,y

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            running = False

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

x, y = KPU_WIDTH // 2, KPU_HEIGHT // 2
frame = 0
n = 0

def draw_point(p):
    global fame,n
    clear_canvas()
    kpu_ground.draw(KPU_WIDTH//2,KPU_HEIGHT//2)


    update_canvas()
    
def draw_curve(n):
    pass

open_canvas(KPU_WIDTH,KPU_HEIGHT)

kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')

while True:
    draw_point((0,0))
    draw_curve(n)

    handle_events()

close_canvas()