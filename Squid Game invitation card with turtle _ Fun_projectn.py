# Squid Game invitation card with turtle _ Fun_projectn
## Import the turtle liabrary
import turtle

## Initialize Turtle
t = turtle.Turtle()
t.pensize(5)
t.speed(3)  # Set drawing speed

## Initialize Screen
s = turtle.Screen()
s.bgcolor('brown')


## Function to draw a circle
def draw_circle():
    t.penup()
    t.goto(-150, 0)  
    t.pendown()
    t.circle(50)  

## Function to draw a triangle
def draw_triangle():
    t.penup()
    t.goto(-45, 0)  
    t.pendown()
    for _ in range(3):  
        t.forward(100)  
        t.left(120)  

## Function to draw a square
def draw_square():
    t.penup()
    t.goto(125, 0)  
    t.pendown()
    for _ in range(4):  
        t.forward(100)  
        t.left(90)  
        

## Draw the shapes
draw_circle()
draw_triangle()
draw_square()

turtle.done()