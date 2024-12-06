# Star Drawing - Fun project3
## Import the drawing liabrary
import turtle
## Create a turtle instance and specify it's attributes
t = turtle.Turtle()
s = turtle.Screen()
t.color('yellow')
t.speed(1.5)
s.bgcolor('black')
## Draw
for i in range(50):
    t.forward(200)
    t.right(144)
    t.forward(200)
    t.left(72)
turtle.done()