from pico2d import*

open_canvas()

grass = load_image('grass.png')
character = load_image('animation_sheet.png')

x = 800 // 2
frame = 0

def run_to_left():
    global x

    global frame

    while x > 0 + 25:
        clear_canvas()

        frame = (frame + 1) % 8

        grass.draw(800 // 2, 30)
        character.clip_draw(frame * 100, 0, 100, 100, x, 90)
        x -= 2

        delay(0.01)

        update_canvas()

def run_to_right():
    global x

    global frame

    while x < 800 - 25:
        clear_canvas()

        frame = (frame + 1) % 8

        grass.draw(800 // 2, 30)
        character.clip_draw(frame * 100, 100, 100, 100, x, 90)
        x += 2

        delay(0.01)

        update_canvas()

while True:

    run_to_left()
    run_to_right()

close_canvas()