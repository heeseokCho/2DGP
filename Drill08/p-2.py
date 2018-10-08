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

points = [(random.randint(0,1280),random.randint(0,1024)) for i in range(10)]
size = len(points)

x, y = KPU_WIDTH // 2, KPU_HEIGHT // 2
frame = 0
n = 0

def draw_point(p):
    global frame,n
    clear_canvas()
    kpu_ground.draw(KPU_WIDTH//2,KPU_HEIGHT//2)

    if points[n][0] > points[(n+1)%size][0]:
        character.clip_draw(frame*100,0,100,100,p[0],p[1])
    else:
        character.clip_draw(frame * 100, 100, 100, 100, p[0], p[1])

    frame = (frame+1) % 8
    update_canvas()
    delay(0.05)

    update_canvas()

def draw_curve(n):
    for i in range(0, 100, 4):
        t = i / 100

        x = ((-t ** 3 + 2 * t ** 2 - t) * points[(n - 1) % size][0] + (3 * t ** 3 - 5 * t ** 2 + 2)*points[(n) % size][0] +
             (-3 * t ** 3 + 4 * t ** 2 + t) * points[(n + 1) % size][0] + (t ** 3 - t ** 2) *points[(n + 2) % size][0]) / 2
        y = ((-t ** 3 + 2 * t ** 2 - t) * points[(n - 1) % size][1] + (3 * t ** 3 - 5 * t ** 2 + 2) *points[(n) % size][1] +
             (-3 * t ** 3 + 4 * t ** 2 + t) * points[(n + 1) % size][1] + (t ** 3 - t ** 2) *points[(n + 2) % size][1]) / 2
        draw_point((x, y))
    draw_point(points[(n+1)%size])



open_canvas(KPU_WIDTH,KPU_HEIGHT)

kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')

while True:
    draw_curve(n)

    handle_events()

close_canvas()