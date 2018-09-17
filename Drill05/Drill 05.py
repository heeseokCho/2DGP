from pico2d import*

open_canvas()

grass = load_image('grass.png')
character = load_image('animation_sheet.png')

point = ((203,535),(132,243),(535,470),(477,203),
         (715,136),(316,225),(510,92),(692,518),
         (682,336),(712,349))

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
#step3
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

def goto_4():
    pass

def goto_5():
    pass

def goto_6():
    pass

def goto_7():
    pass

def goto_8():
    pass

def goto_9():
    pass

def goto_0():
    pass


while True:


   # goto_1()
   # goto_2()
    goto_3()
    goto_4()
    goto_5()
    goto_6()
    goto_7()
    goto_8()
    goto_9()
    goto_0()


close_canvas()