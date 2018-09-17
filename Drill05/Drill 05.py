from pico2d import*

open_canvas()

grass = load_image('grass.png')
character = load_image('animation_sheet.png')

#step 1
point = ((203,535),(132,243),(535,470),(477,203),
         (715,136),(316,225),(510,92),(692,518),
         (682,336),(712,349))

#step 2
def goto_1():
    x, y = point[0][0], point[0][1]
    next = point[1]
    frame = 0

    while x > next[0]:
        clear_canvas()
        x -= 5
        character.clip_draw(frame*100,0,100,100,x,y)
        frame = (frame+1) % 8
        update_canvas()
        delay(0.02)

    while y > next[1]:
        clear_canvas()
        y -= 5
        character.clip_draw(frame*100,0,100,100,x,y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)
#step 3
def goto_2():
    x, y = point[1][0], point[1][1]
    next = point[2]
    frame = 0

    while x < next[0]:
        clear_canvas()
        x += 5
        character.clip_draw(frame * 100, 100, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)

    while y < next[1]:
        clear_canvas()
        y += 5
        character.clip_draw(frame * 100, 100, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)

#step 4
def goto_3():
    x, y = point[2][0], point[2][1]
    next = point[3]
    frame = 0

    while x > next[0]:
        clear_canvas()
        x -= 5
        character.clip_draw(frame * 100, 0, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)

    while y > next[1]:
        clear_canvas()
        y -= 5
        character.clip_draw(frame * 100, 0, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)

#step 5
def goto_4():
    x, y = point[3][0], point[3][1]
    next = point[4]
    frame = 0

    while x < next[0]:
        clear_canvas()
        x += 5
        character.clip_draw(frame * 100, 100, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)

    while y > next[1]:
        clear_canvas()
        y -= 5
        character.clip_draw(frame * 100, 100, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)

#step 6
def goto_5():
    x, y = point[4][0], point[4][1]
    next = point[5]
    frame = 0

    while x > next[0]:
        clear_canvas()
        x -= 5
        character.clip_draw(frame * 100, 0, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)

    while y < next[1]:
        clear_canvas()
        y += 5
        character.clip_draw(frame * 100, 0, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)

#step 7
def goto_6():
    x, y = point[5][0], point[5][1]
    next = point[6]
    frame = 0

    while x < next[0]:
        clear_canvas()
        x += 5
        character.clip_draw(frame * 100, 100, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)

    while y > next[1]:
        clear_canvas()
        y -= 5
        character.clip_draw(frame * 100, 100, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)

#step 8
def goto_7():
    x, y = point[6][0], point[6][1]
    next = point[7]
    frame = 0

    while x < next[0]:
        clear_canvas()
        x += 5
        character.clip_draw(frame * 100, 100, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)

    while y < next[1]:
        clear_canvas()
        y += 5
        character.clip_draw(frame * 100, 100, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)

#step 9
def goto_8():
    x, y = point[7][0], point[7][1]
    next = point[8]
    frame = 0

    while x > next[0]:
        clear_canvas()
        x -= 5
        character.clip_draw(frame * 100, 0, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)

    while y > next[1]:
        clear_canvas()
        y -= 5
        character.clip_draw(frame * 100, 0, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)

# step 10
def goto_9():
    x, y = point[8][0], point[8][1]
    next = point[9]
    frame = 0

    while x < next[0]:
        clear_canvas()
        x += 5
        character.clip_draw(frame * 100, 100, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)

    while y < next[1]:
        clear_canvas()
        y += 5
        character.clip_draw(frame * 100, 100, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)

#step 11
def goto_0():
    x, y = point[9][0], point[9][1]
    next = point[0]
    frame = 0

    while x > next[0]:
        clear_canvas()
        x -= 5
        character.clip_draw(frame * 100, 0, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)

    while y < next[1]:
        clear_canvas()
        y += 5
        character.clip_draw(frame * 100, 0, 100, 100, x, y)
        frame = (frame + 1) % 8
        update_canvas()
        delay(0.02)


while True:


   # goto_1()
   # goto_2()
   # goto_3()
   # goto_4()
   # goto_5()
   # goto_6()
   # goto_7()
   # goto_8()
   # goto_9()
    goto_0()


close_canvas()