from pico2d import *
open_canvas()
grass = load_image('grass.png')
character = load_image('animation_sheet.png')

x = 0
frame = 0

Left = False

while(True) :
    clear_canvas()
    grass.draw(400, 30)

    if(Left == True):
        character.clip_draw(frame*100, 0, 100, 100, x, 90)
    elif(Left == False):
        character.clip_draw(frame * 100, 100, 100, 100, x, 90)

    update_canvas()
    frame = (frame+1) % 8

    if(Left == False):
        x += 5

        if(x > 795):
            Left = True
            
    elif(Left == True):
        x -=5

        if(x < 5):
            Left = False


    delay(0.05)
    get_events()


close_canvas()

