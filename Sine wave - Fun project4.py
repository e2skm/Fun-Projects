# Sine wave - Fun project4
## Import the necessary liabraries
import math
import turtle
import time
## Create a turtle instace, a canvas and specify other attributes
t = turtle.Turtle()
s = turtle.Screen()
t.speed(0)
t.color('cyan')
s.bgcolor('black')
## For better visualization 
s.setup(width=1000,height=500)
t.pendown()
t.goto(-360,0)
t.penup()
t.goto(360,0)
t.pendown()
## Draw a Sine wave
for x in range(-360,360):
    y = 100 * math.sin(math.radians(x))
    t.goto(x,y)
    time.sleep(0.02) ## pause for a slower/better visual
## Complete draw
turtle.done()