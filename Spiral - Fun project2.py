# Spiral - Fun project2
## Import the necessary liabrary
import turtle
## Create a turtle instance specify it's attributes
t = turtle.Turtle()
s = turtle.Screen() ## Canvas setup
s.bgcolor('White') 
t.speed(0)
colors= ['red','green','blue','yellow','purple']
## Draw the spiral
for i in range(150):
    t.color(colors[i%  len(colors)]) ## Color changes
    t.circle(110)## circumference of each circle
    t.right(10)
turtle.done()

