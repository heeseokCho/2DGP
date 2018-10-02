from pico2d import *
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



def draw_point(p):
    global frame, n
    clear_canvas()
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)

    if points[n - 1][0] > points[n][0]:
        character.clip_draw(frame * 100, 0, 100, 100, p[0], p[1])
    else:
        character.clip_draw(frame * 100, 100, 100, 100, p[0], p[1])

    frame = (frame + 1) % 8
    update_canvas()

def draw_line(p1,p2):

    for i in range(0,100,4):
        t = i /100
        x = (1-t)*p1[0] + t*p2[0]
        y = (1-t)*p1[1] + t*p2[1]
        draw_point((x,y))
        delay(0.05)

    draw_point(p2)

open_canvas(KPU_WIDTH,KPU_HEIGHT)

kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')

x, y = KPU_WIDTH // 2, KPU_HEIGHT // 2
frame = 0
n = 1
points = [(random.randint(0+200,1280-200),random.randint(0+200,1024-200)) for i in range(20)]
size = len(points)


while True:


    draw_line(points[n-1],points[n])

    n = (n+1) % size



    handle_events()

close_canvas()