import turtle
import random


def stop():
    turtle.bye()


def prepare_turtle_canvas():
    turtle.setup(1024, 768)
    turtle.bgcolor(0.2, 0.2, 0.2)
    turtle.penup()
    turtle.hideturtle()
    turtle.shape('arrow')
    turtle.shapesize(2)
    turtle.pensize(5)
    turtle.color(1, 0, 0)
    turtle.speed(100)
    turtle.goto(-500, 0)
    turtle.pendown()
    turtle.goto(480, 0)
    turtle.stamp()
    turtle.penup()
    turtle.goto(0, -360)
    turtle.pendown()
    turtle.goto(0, 360)
    turtle.setheading(90)
    turtle.stamp()
    turtle.penup()
    turtle.home()

    turtle.shape('circle')
    turtle.pensize(1)
    turtle.color(0, 0, 0)
    turtle.speed(50)

    turtle.onkey(stop, 'Escape')
    turtle.listen()


points = [(-300,200),(400,350),(300,-300),(100,100),(-200,-200)]

def draw_big_point(p):
    turtle.goto(p)
    turtle.color(0.8, 0.9, 0)
    turtle.dot(15)
    turtle.write('     '+str(p))

def draw_point(p):
    turtle.goto(p)
    turtle.dot(5, random.random(), random.random(), random.random())

def draw_curve(n):
    for i in range(5):
        draw_big_point(points[i])

    for i in range(0, 100, 4):
        t = i / 100

        x = ((-t ** 3 + 2 * t ** 2 - t) * points[(n - 1) % 5][0] + (3 * t ** 3 - 5 * t ** 2 + 2) * points[(n) % 5][0] + (
            -3 * t ** 3 + 4 * t ** 2 + t) * points[(n + 1) % 5][0] + (t ** 3 - t ** 2) * points[(n + 2) % 5][0]) / 2
        y = ((-t ** 3 + 2 * t ** 2 - t) * points[(n - 1) % 5][1] + (3 * t ** 3 - 5 * t ** 2 + 2) * points[(n) % 5][1] + (
            -3 * t ** 3 + 4 * t ** 2 + t) * points[(n + 1) % 5][1] + (t ** 3 - t ** 2) * points[(n + 2) % 5][1]) / 2
        draw_point((x,y))
    draw_point(points[(n + 2) % 5])

prepare_turtle_canvas()

n = 0
while True:
    draw_curve(n)
    n = (n+1) % 5


turtle.done()