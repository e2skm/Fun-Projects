# Draw a cross - Fun projectn

## Import the Turtle graphics liabrary for animations 
import turtle

## Turtle instance
t = turtle.Turtle()

## Set Screen Dimensions
s = turtle.Screen()
s.setup(800,600)
## Set background color
s.bgcolor('white')

## Set pen color
t.pencolor('black')

## Set pen Thickness 
t.pensize(5)

## Set drawing speed
t.speed(1.2)

## Start drawing
t.begin_fill()
t.fillcolor('gold')
t.pendown()
for i in range(2):
    t.fd(100)
    t.rt(90)
    t.backward(100)
    t.rt(90)
    t.fd(100)
    t.rt(90)
for i in range(2):
    t.fd(100)
    t.lt(90)
t.forward(100)
t.right(90)
t.forward(200)
t.left(90)
t.forward(100)
t.left(90)
t.forward(200)
t.end_fill()
t.penup()

## Add text at the bottom
t.goto(-55,-250)
t.write('God is Love', align='center' , font=('Arial', 18 , 'bold'))

## End turtle
turtle.done()

