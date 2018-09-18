from pico2d import *

KPU_WIDTH, KPU_HEIGHT = 1280, 1024

def handle_events():
    global running
    global x, y
    global select
    global cx, cy
    global dx, dy

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            running = False

        elif event.type == SDL_MOUSEMOTION:
            cx, cy = event.x, KPU_HEIGHT - 1 - event.y

        elif event.type == SDL_MOUSEBUTTONDOWN:
            select = True
            dx, dy = event.x, KPU_HEIGHT - 1 - event.y

        elif event.type == SDL_MOUSEBUTTONDOWN:
            pass

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False




open_canvas(KPU_WIDTH,KPU_HEIGHT)

kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')
hand_arrow = load_image('hand_arrow.png')

select = False
running = True
x, y = KPU_WIDTH // 2, KPU_HEIGHT // 2
frame = 0
hide_cursor()
dir1 = 0

dir2 = 0
cx, cy = KPU_WIDTH // 2, KPU_HEIGHT // 2
dx, dy = KPU_WIDTH // 2, KPU_HEIGHT // 2

while running:
    clear_canvas()
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)

    if (dx > x):
        dir1 = 1
    else:
        dir1 = -1

    if (dy > y):
        dir2 = 1
    else:
        dir2 = -1

    if (dir1 == 1):
        while (x < dx):
            x = x + 3
            clear_canvas()
            kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
            character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)
            hand_arrow.clip_draw(0, 0, 100, 100, cx-50, cy-50)
            update_canvas()
            frame = (frame + 1) % 8

            delay(0.02)
            handle_events()

    else:
        while (x > dx):
            x = x - 3
            clear_canvas()
            kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
            hand_arrow.clip_draw(0, 0, 100, 100, cx-50, cy-50)
            character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)
            update_canvas()
            frame = (frame + 1) % 8

            delay(0.02)
            handle_events()

    if (dir2 == 1):
        while (y < dy):
            y = y + 3
            clear_canvas()
            kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
            hand_arrow.clip_draw(0, 0, 100, 100, cx-50, cy-50)
            character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)
            update_canvas()
            frame = (frame + 1) % 8

            delay(0.02)
            handle_events()
    else:
        while (y > dy):
            y = y - 3
            clear_canvas()
            hand_arrow.clip_draw(0, 0, 100, 100, cx, cy)
            kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
            character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)

            update_canvas()
            frame = (frame + 1) % 8

            delay(0.02)
            handle_events()

    hand_arrow.clip_draw(0, 0, 100, 100, cx - 50, cy - 50)

    if(select == False):
        frame = (frame + 1) % 8
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)

        update_canvas()


        delay(0.02)
    handle_events()

close_canvas()