# Text Fireworks - Fun project6

## Import all the necessary liabraries
import turtle,random

## Set up the screen
screen = turtle.Screen()
screen.bgcolor('black')
screen.title('Fireworks with Text')

## Define a function to create fireworks
def fireworks():
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.color(random.choice(['red','green','blue','yellow','cyan','purple','white','orange','gold','silver']))
    t.penup()
    t.goto(random.randint(-200,200),random.randint(-200,200))
    t.pendown()
    for _ in range(36):
        t.forward(50)
        t.backward(50)
        t.right(10)
        
## Define a function to display text with fireworks
def display_text(message,fontsize):
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.color('white')
    pen.penup()
    pen.goto(0,200)
    pen.write(message,align='center',font=('Arial',fontsize,'bold'))
    
## Test above function with input (Create Main function)
display_text('Happy New year!!!',24)

for _ in range(10):
    fireworks()
    
screen.mainloop()