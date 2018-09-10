import os

os.chdir('C:\\Users\\CHS\Desktop\\조희석\\전공\\2D Git\\2018\\2018-2DGP\\Labs\\Lecture04')

from pico2d import*

import math

open_canvas()

character = load_image('character.png')
grass = load_image('grass.png')

x = 400
y = 90

cx = 400
cy = 300
cr = 300-90
theta = -90
radian = math.radians(-90)

rect = True

while(True):
    
    clear_canvas_now()
    grass.draw_now(400,30)
    
    if(rect == True):
         #right
        if(y == 90 and x < 800-20):
            x = x + 5

            #한바퀴 돌면 원으로 바뀜
            if (x == 395 and y == 90):
                rect = False

            #up
        if(x == 800-20 and y < 600-50):
            y = y + 5

            #left
        if(y == 600-50 and x  > 0+10):
            x = x-5

            #down
        if(x == 0+10 and y > 90):
            y = y - 5
            

    elif(rect == False):
        x = cx+cr * math.cos(radian)
        y = cy+cr * math.sin(radian)
        theta = theta + 2
        radian = math.radians(theta)
       


        if(theta >= 270):
            theta = -90
            x = 400
            y = 90
            rect = True

    character.draw_now(x,y)

    delay(0.01)


clear_canvas_now()



