from pico2d import *

WINX  = 1600
WINY  = 1000
open_canvas(WINX,WINY)

Link_Walking = load_image('Walking.png')
Link_Standing = load_image('Standing.png')
Link_Shooting = load_image('Shooting.png')
Link_Aiming = load_image('Aiming.png')
Link_AimWalking = load_image('AimWalking.png')
Link_Dieing = load_image('Dieing.png')
Arrow = load_image('Arrow.png')

#사진 크기
Size = 64
#방향별 사진
Up,Down,Left,Right = Size*3, Size*2, Size*1, Size*0
#상태
Walking,Standing,Shooting,Aiming,AimWalking,Dieing = 0,1,2,3,4,5
#바라보는 방향
Look = Down
#상태
State = Standing
#동작하고있는지
Charging = False
#프레임
frame = 0
#사진 종류
Link_State = 0
#사진개수
PictureNum = 1
#일시적인 동작 카운트
Cnt = 0

DirX = 0
DirY = 0
x, y = WINX // 2, WINY//2
Running = True

def handle_events():
    global Running
    global DirX, DirY
    global Look, State
    global Cnt, PictureNum
    global Charging
    global frame

    events = get_events()
    for event in events:
        frame = 0
        if event.type == SDL_QUIT:
            Running = False

        #키를 땠을 때
        if event.type == SDL_KEYUP:
            if event.key == SDLK_d:
                DirX -= 1
            elif event.key == SDLK_a:
                DirX += 1
            elif event.key == SDLK_w:
                DirY -= 1
            elif event.key == SDLK_s:
                DirY += 1
            elif event.key == SDLK_j:
                Cnt = 0
                Charging = False
                if DirX == 0 and DirY == 0:
                    State = Standing
                    PictureNum = 1
                else:
                    State = Walking
                    PictureNum = 10

            if DirX == 0 and DirY == 0 and State != AimWalking:
                State = Standing
                PictureNum = 1

        #키가 눌렸을 때
        elif event.type == SDL_KEYDOWN:
            frame = 0

            if event.key == SDLK_ESCAPE:
                Running = False
            elif event.key == SDLK_d:
                DirX += 1
                Look = Right

                if Cnt <= 3:
                    State = Walking
                    PictureNum = 10
                else:
                    State = AimWalking
                    PictureNum = 8

            elif event.key == SDLK_a:
                DirX -= 1
                Look = Left
                if Cnt <= 3:
                    State = Walking
                    PictureNum = 10
                else:
                    State = AimWalking
                    PictureNum = 8
            elif event.key == SDLK_w:
                DirY += 1
                Look = Up
                if Cnt <= 3:
                    State = Walking
                    PictureNum = 10
                else:
                    State = AimWalking
                    PictureNum = 8
                PictureNum = 10
            elif event.key == SDLK_s:
                DirY -= 1
                Look = Down
                if Cnt <= 3:
                    State = Walking
                    PictureNum = 10
                else:
                    State = AimWalking
                    PictureNum = 8

            elif event.key == SDLK_j:
                Charging = True
                State = Aiming
                PictureNum = 3



while Running:
    clear_canvas()

    if State == Standing:
        Link_Standing.clip_draw(frame * Size, Look, Size, Size, x, y)
    elif State == Walking:
        Link_Walking.clip_draw(frame * Size, Look, Size, Size, x, y)
    elif State == Aiming:
        Link_Aiming.clip_draw(frame * Size, Look, Size, Size, x, y)
    elif State == AimWalking:
        Link_AimWalking.clip_draw(frame * Size, Look, Size, Size, x, y)
    elif State == Shooting:
        Link_Shooting.clip_draw(frame * Size, Look, Size, Size, x, y)
    elif State == Dieing:
        Link_Dieing.clip_draw(frame * Size, Look, Size, Size, x, y)

    x += DirX * 10
    y += DirY * 10
    if Charging == True:
        Cnt += 1

    if Cnt > 3:
        State = AimWalking
        PictureNum = 8

    frame = (frame + 1) % PictureNum


    update_canvas()
    handle_events()

    delay(0.05)





