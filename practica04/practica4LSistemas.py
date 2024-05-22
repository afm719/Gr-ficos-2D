# -*- coding: utf-8 -*-
"""

@author: Arahí Fernández Monagas

Gráficos por Computador
    Práctica 4  

"""
import tkinter as tk
import numpy as np
import math
import random

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600

# Colors
global DRAW_COLOR
DRAW_COLOR = '#000000'
BUTTON_COLOR = '#C0C0C0'
ACTIVE_BUTTON_COLOR = '#A0A0A0'


################################## FUNCTIONS #################################

# Removes all objects from canvas    
def clearCanvas():
    canvas.delete("all")
     

# Transforms the coordinates from cartesian to (right-left, up-down)
def adjust(x, y):
    newX = x + CANVAS_WIDTH/2
    newY = (-1) * (y - CANVAS_HEIGHT/2)
    return newX, newY




# Initiates the modified curves function
def startModifiedCurves():
    
    n = 2
    alpha = 90
    axiom = "F-F-F-F"
    rules = [["F","F+FF-FF-F-F+F+FF-F-F+F+FF+FF-F"]]
    
    text = generateLSystem(n, axiom, rules)
    origin = np.array([-100, -100])
    zoom = 5
    direction = 90
    renderLSystem(text, origin, alpha, direction, zoom)


# Initiates the Gasket function  
def startGasket():
    
    n = 6
    alpha = 60
    axiom = "R"
    rules = [["L", "R+L+R"],
             ["R", "L-R-L"]]
    
    text = generateLSystem(n, axiom, rules)
    origin = np.array([-250, -200])
    zoom = 8
    direction = 0
    renderLSystem(text, origin, alpha, direction, zoom)
    

# Initiates the Gasket function      
def startIslands():
    
    n = 2
    alpha = 90
    axiom = "F+F+F+F"
    rules = [["F", "F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF"],
             ["f", "ffffff"]]
    
    text = generateLSystem(n, axiom, rules)
    origin = np.array([100, -100])
    zoom = 5
    direction = 90
    renderLSystem(text, origin, alpha, direction, zoom)
    
    
    
# Initiates a plant function
def startPlantA():
    
    n = 5
    alpha = 22.5
    axiom = "X"
    rules = [["F", "FF"],
             ["X", "F-[[X]+X]+F[+FX]-X"]]
    
    text = generateLSystem(n, axiom, rules)
    origin = np.array([0, -200])
    zoom = 5
    direction = 90
    renderLSystem(text, origin, alpha, direction, zoom)
    

# Initiates a plant function
def startPlantB():
    
    n = 7
    alpha = 25.7
    axiom = "X"
    rules = [["F", "FF"],
             ["X", "F[+X][-X]FX"]]
    
    text = generateLSystem(n, axiom, rules)
    origin = np.array([0, -250])
    zoom = 2
    direction = 90
    renderLSystem(text, origin, alpha, direction, zoom)
    

# Initiates a plant function    
def startPlantC():
    
    n = 5
    alpha = 20
    axiom = "F"
    rules = [["F", "F[+F]F[-F][F]"]]
    
    text = generateLSystem(n, axiom, rules)
    origin = np.array([0, -250])
    zoom = 8
    direction = 90
    renderLSystem(text, origin, alpha, direction, zoom)
        

# Generates a sentence given an axiom and a set of rules
# n: number of generations
# axiom: initial axiom
# rules: a list of rules [[A, AB], ...[...]]    
def generateLSystem(n, axiom, rules):
    
    lastText = axiom
    constant = True

    for i in range(n):
        newText = ""
        for char in lastText:
            possibleRules = []
            for rule in rules:
                if(rule[0] == char):
                    constant = False
                    possibleRules.append(rule[1])
   
            if (constant):
                newText = newText + char
            else:
                ruleToApply = random.choice(possibleRules)  
                newText = newText + ruleToApply
            constant = True
            
        lastText = newText
        
    return lastText
        

# Generates a sentence given an axiom and a set of rules
# text: sentence composed of F, L, R, +, -, [ or ] characters
# origin: starting point
# alpha: angle for each rotation
# direction: initial direction (right=0, up=90, left=180, down=270)
# zoom: distance for each step
def renderLSystem(text, origin, alpha, direction, zoom):
    
    clearCanvas()
    
    currentPos = origin
    newPos = origin
    
    directionRad = math.radians(direction)
    alphaRad = math.radians(alpha)

    states = []
    directions = []

    for char in text:
        
        if char == "-":
            directionRad = directionRad - alphaRad
  
        elif char == "+":
            directionRad = directionRad + alphaRad
        
        elif char == "[":
            states.append(currentPos)
            directions.append(directionRad)
            
        elif char == "]":
            currentPos = states.pop()
            directionRad = directions.pop()
            
        elif char == "F" or char == "L"  or char == "R":
            newPos = [currentPos[0]+zoom*math.cos(directionRad), currentPos[1]+zoom*math.sin(directionRad)]
            
            x1, y1 = adjust(currentPos[0], currentPos[1])
            x2, y2 = adjust(newPos[0], newPos[1])
            canvas.create_line(x1, y1, x2, y2, fill=DRAW_COLOR)
            
            currentPos = newPos
            
        elif char == "f":
            newPos = [currentPos[0]+zoom*math.cos(directionRad), currentPos[1]+zoom*math.sin(directionRad)]
            currentPos = newPos
            
        
            
    
################################## WINDOW ###################################
# Create Window
window = tk.Tk()
window.geometry("1000x700")
window.title("Computer Graphics")


# Configure window
window.columnconfigure(0, weight=3)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.columnconfigure(3, weight=1)
window.columnconfigure(4, weight=1)
for i in range(10):
    window.rowconfigure(i, weight=1)



################################### CANVAS ##################################
# Create canvas
canvas = tk.Canvas(window, width = CANVAS_WIDTH,  height = CANVAS_HEIGHT, bg = "white",  highlightthickness=0, highlightbackground="white")
canvas.place(x=40, y=60)


################################### BUTTONS #################################
# Modified curves
modifiedCurvesButton = tk.Button(window, width = 15, text = "Modified Curves", command = startModifiedCurves, activebackground=ACTIVE_BUTTON_COLOR)
modifiedCurvesButton.place(x=700, y=80) 

# Gasket
gasketButton = tk.Button(window, width = 15, text = "Gasket", command = startGasket, activebackground=ACTIVE_BUTTON_COLOR)
gasketButton.place(x=850, y=80) 

# Islands
islandsButton = tk.Button(window, width = 15, text = "Islands", command = startIslands, activebackground=ACTIVE_BUTTON_COLOR)
islandsButton.place(x=700, y=120) 

# Plant A
plantAButton = tk.Button(window, width = 15, text = "Plant A", command = startPlantA,  activebackground=ACTIVE_BUTTON_COLOR)
plantAButton.place(x=850, y=120)

# Plant B
plantBButton = tk.Button(window, width = 15, text = "Plant B", command = startPlantB, activebackground=ACTIVE_BUTTON_COLOR)
plantBButton.place(x=700, y=160)  

# Plant C
plantCButton = tk.Button(window, width = 15, text = "Plant C", command = startPlantC, activebackground=ACTIVE_BUTTON_COLOR)
plantCButton.place(x=850, y=160)  


################################### LABELS #################################
# Fractals
fractalsLbl = tk.Label(window, text = "L-Systems", font=("Arial", 18))
fractalsLbl.place(x=270, y=15)


################################# INTERACTIONS ###############################
canvas.focus_set()


window.mainloop()