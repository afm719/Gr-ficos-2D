# -*- coding: utf-8 -*-
"""

@author: Arahí Fernández Monagas

Gráficos por Computador
    Práctica 3 : Fractales

"""

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk


CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

MANDELBROT_ITER = 100
JULIA_ITER = 50

# Colors
global COLOR
COLOR = '#000000'
ACTIVE_BUTTON_COLOR = '#A0A0A0'


# Transforms the coordinates from cartesian to (right-left, up-down)
def adjust(x, y):
    newX = x + CANVAS_WIDTH/2
    newY = (-1) * (y - CANVAS_HEIGHT/2)
    return newX, newY

def clear_canvas():
    canvas.delete("all")
    imageLbl.config(image='') 
 
    
##########################################################################################################################################
                                                        
                                                        #Fractales Recursivas
                                                        
##########################################################################################################################################

# Initializes the Sierpinski Triangle function
def initSierpinski(x1, y1, x2, y2, x3, y3):
    clear_canvas()
    
    x1, y1 = adjust(x1, y1)
    x2, y2 = adjust(x2, y2)
    x3, y3 = adjust(x3, y3)
    
    n = iterField.get("1.0","end-1c")
    if (n == ''):
        n = 0
    else:
        n = int(n)
    
    drawSierpinski(x1, y1, x2, y2, x3, y3, n)
 
def drawSierpinski(x1, y1, x2, y2, x3, y3, n):
    
    if(n == 0):
        canvas.create_line(x1, y1, x2, y2)
        canvas.create_line(x2, y2, x3, y3)
        canvas.create_line(x1, y1, x3, y3)
        
    else:
        ax = x1 + (x2 - x1) / 2
        ay = y1 + (y2 - y1) / 2
        
        bx = x3 + (x2 - x3) / 2
        by = y3 + (y2 - y3) / 2
        
        cx = x1 + (x3 - x1) / 2
        cy = y1 + (y3 - y1) / 2
        
        drawSierpinski(ax, ay, x2, y2, bx, by, n-1)
        drawSierpinski(x1, y1, ax, ay, cx, cy, n-1)
        drawSierpinski(cx, cy, bx, by, x3, y3, n-1)

# Initializes the Korch Curve function
def initKorch(x1, y1, x4, y4):
    clear_canvas()
    
    x1, y1 = adjust(x1, y1)
    x4, y4 = adjust(x4, y4)
    
    n = iterField.get("1.0","end-1c")
    if (n == ''):
        n = 0
    else:
        n = int(n)
    
    drawKorch(x1, y1, x4, y4, n)
    
def drawKorch(x1, y1, x4, y4, n):
    
    if (n == 0):
        canvas.create_line(x1, y1, x4, y4)
    
    else:
        dx = (x4 - x1) / 3
        dy = (y4 - y1) / 3
        
        x2 = x1 + dx
        y2 = y1 + dy
        
        x3 = x2 + dx
        y3 = y2 + dy
        
        x = (dx - np.sqrt(3) * dy) / 2 + x1 + dx
        y = (np.sqrt(3) * dx + dy) / 2 + y1 + dy
        
        drawKorch(x1, y1, x2, y2, n-1)
        drawKorch(x2, y2, x, y, n-1)
        drawKorch(x, y, x3, y3, n-1)
        drawKorch(x3, y3, x4, y4, n-1)
    
# Initializes the Sierpinski Carpet function
def initCarpet(x1, y1, x2, y2, x3, y3, x4, y4):
    clear_canvas()
    
    x1, y1 = adjust(x1, y1)
    x2, y2 = adjust(x2, y2)
    x3, y3 = adjust(x3, y3)
    x4, y4 = adjust(x4, y4)
    
    n = iterField.get("1.0","end-1c")
    if (n == ''):
        n = 0
    else:
        n = int(n)

    drawCarpet(x1, y1, x2, y2, x3, y3, x4, y4, n)
    
         
def drawCarpet(x1, y1, x2, y2, x3, y3, x4, y4, n):

     if(n == 0):
         canvas.create_line(x1, y1, x2, y2)
         canvas.create_line(x2, y2, x3, y3)
         canvas.create_line(x3, y3, x4, y4)
         canvas.create_line(x1, y1, x4, y4)
     
     else:
         
         ax1, ay1 = x1, y1
         ax2, ay2 = x1 + (x2-x1) / 3, y1
         ax3, ay3 = x1 + (x2-x1) / 3, y1 + (y4 - y1) / 3
         ax4, ay4 = x1, y1 + (y4 - y1) / 3
         
         bx1, by1 = ax2, ay2
         bx2, by2 = x1 + 2*(x2-x1) / 3, y1
         bx3, by3 = x1 + 2*(x2-x1) / 3, y1 + (y4 - y1) / 3
         bx4, by4 = ax3, ay3
         
         cx1, cy1 = bx2, by2
         cx2, cy2 = x2, y2
         cx3, cy3 = x2, y1 + (y4 - y1) / 3
         cx4, cy4 = bx3, by3
         
         dx1, dy1 = ax4, ay4
         dx2, dy2 = ax3, ay3
         dx3, dy3 = ax2, y1 + 2*(y4 - y1) / 3
         dx4, dy4 = x1, dy3
         
         ex1, ey1 = ax3, ay3
         ex2, ey2 = bx3, by3
         ex3, ey3 = bx2, dy3
         ex4, ey4 = ax2, dy3 
         
         fx1, fy1 = bx3, by3
         fx2, fy2 = cx3, cy3
         fx3, fy3 = x2, dy3
         fx4, fy4 = ex3, dy3 
         
         gx1, gy1 = dx4, dy4
         gx2, gy2 = dx3, dy3
         gx3, gy3 = ax2, y4
         gx4, gy4 = x4, y4 
         
         hx1, hy1 = dx3, dy3
         hx2, hy2 = ex3, ey3
         hx3, hy3 = bx2, y4
         hx4, hy4 = ax2, y4 
         
         ix1, iy1 = ex3, ey3
         ix2, iy2 = x2, dy3
         ix3, iy3 = x3, y3
         ix4, iy4 = bx2, y4 
         
         canvas.create_line(ex1, ey1, ex2, ey2)
         canvas.create_line(ex2, ey2, ex3, ey3)
         canvas.create_line(ex3, ey3, ex4, ey4)
         canvas.create_line(ex1, ey1, ex4, ey4)
         
         drawCarpet(ax1, ay1, ax2, ay2, ax3, ay3, ax4, ay4, n-1)
         drawCarpet(bx1, by1, bx2, by2, bx3, by3, bx4, by4, n-1)
         drawCarpet(cx1, cy1, cx2, cy2, cx3, cy3, cx4, cy4, n-1)
         drawCarpet(dx1, dy1, dx2, dy2, dx3, dy3, dx4, dy4, n-1)
         drawCarpet(fx1, fy1, fx2, fy2, fx3, fy3, fx4, fy4, n-1)
         drawCarpet(gx1, gy1, gx2, gy2, gx3, gy3, gx4, gy4, n-1)
         drawCarpet(hx1, hy1, hx2, hy2, hx3, hy3, hx4, hy4, n-1)
         drawCarpet(ix1, iy1, ix2, iy2, ix3, iy3, ix4, iy4, n-1)
         
         

##########################################################################################################################################
                                                        
                                                        #Fractales basados en funciones complejas
                                                        
##########################################################################################################################################

# Initializes the Mandelbrot function
def initMandelbrot():
    clear_canvas()
    mandelbrot_set()

def mandelbrot_set():
    xMin = -2.25
    yMin = -1.75
    xMax = 1.25
    yMax = 1.75
    r = 3.5 * CANVAS_WIDTH / CANVAS_HEIGHT / 2
    xMin = - r - 0.5
    xMax = r -0.5
    for x in range(0, CANVAS_WIDTH):
        for y in range(0, CANVAS_HEIGHT):
            c = complex(xMin + (x / CANVAS_WIDTH) * (xMax - xMin),
                        yMin + (y / CANVAS_HEIGHT) * (yMax - yMin))
            n = mandelbrot(c)
            colorS = 255 - int(n * 255 / MANDELBROT_ITER)
            colorH = hex(colorS)[2:]
            color = "#" + str(colorH) * 3
            canvas.create_rectangle((x, y) * 2, outline=color, fill=color)

def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MANDELBROT_ITER:
        z = z * z + c
        n += 1
    return n

# Initializes the Julia function
def initJulia():
    clear_canvas()
    julia_set()

def julia_set():

    xMin = -2
    yMin = -1.75
    xMax = 2
    yMax = 1.75
    r = 3.5 * CANVAS_WIDTH / CANVAS_HEIGHT / 2
    xMin = - r - 0.5
    xMax = r -0.5
    
    c = -0.698 - 0.286j 
    for x in range(0, CANVAS_WIDTH):
        for y in range(0, CANVAS_HEIGHT):
            z = complex(xMin + (x / CANVAS_WIDTH) * (xMax - xMin),
                        yMin + (y / CANVAS_HEIGHT) * (yMax - yMin))
            n = julia(z, c)
            colorS = 255 - int(n * 255 / MANDELBROT_ITER)
            colorH = hex(colorS)[2:]
            color = "#" + str(colorH) * 3
            canvas.create_rectangle((x, y) * 2, outline=color, fill=color)

def julia(z, c):
    n = 0
    while abs(z) <= 2 and n < MANDELBROT_ITER:
        z = z * z + c
        n += 1
    return n


##########################################################################################################################################
                                                        
                                                        #Sistemas de funciones iteradas (IFS)
                                                        
##########################################################################################################################################



# Initializes the Barnsley Fern function    
def initBarnsley():

    clear_canvas()
    
    fern = np.matrix([[0, 0, 0, 0.16, 0, 0, 0.01],
                      [0.85, 0.04, -0.04, 0.85, 0, 1.60, 0.85],
                      [0.20, -0.26, 0.23, 0.22, 0, 1.60, 0.07],
                      [-0.15, 0.28, 0.26, 0.24, 0, 0.44, 0.07]])
    coord = np.array([0, 0, 1])
    nIter = 50000
    zoom = 40
    xMove = 0
    yMove = -200
    
    ifs(fern, coord, nIter, zoom, xMove, yMove)


# Initializes the Crystal function  
def initCrystal():

    clear_canvas()
    
    crystal = np.matrix([[0.255, 0.,0., 0.255,0.372, 0.671, 0.25],
                         [0.255, 0.,0., 0.255,0.115, 0.223, 0.25],
                         [0.255, 0.,0., 0.255,0.631, 0.223, 0.25],
                         [0.37, -0.642,0.642, 0.37,0.636, -0.006, 0.25]])
    
    coord = np.array([0, 0, 1])
    nIter = 80000
    zoom = 500
    xMove = -250
    yMove = -275
    
    ifs(crystal, coord, nIter, zoom, xMove, yMove)

# Initializes the Dragon function  
def initDragon():

    clear_canvas()
    
    dragon = np.matrix([[0.82,0.28,-0.21,0.86,-1.88,-0.11, 0.5],
                         [0.09,0.52,-0.46,-0.38,0.79,8.10, 0.5]])
    
    coord = np.array([0, 0, 1])
    nIter = 300000
    zoom = 35
    xMove = 0
    yMove = -180
    
    ifs(dragon, coord, nIter, zoom, xMove, yMove)

# Initializes the Chaos function  
def initChaos():
    
    clear_canvas()

    chaos = np.matrix([[0, 0.053,-0.429, 0,-7.083, 5.43, 1/19],
                       [0.143, 0,0, -0.053,-5.619, 8.513, 1/19],
                       [0.143, 0,0, 0.083,-5.619, 2.057, 1/19],
                       [0, 0.053,0.429, 0,-3.952, 5.43, 1/19],
                       [0.119, 0,0, 0.053,-2.555, 4.536, 1/19],
                       [-0.0123806,-0.0649723,0.423819,0.00189797,-1.226, 5.235, 1/19],
                       [0.0852291,0.0506328,0.420449,0.0156626,-0.421, 4.569, 1/19],
                       [0.104432,0.00529117,0.0570516,0.0527352,0.976, 8.113, 1/19],
                       [-0.00814186,-0.0417935,0.423922,0.00415972,1.934, 5.37, 1/19],
                       [0.093, 0,0, 0.053,0.861, 4.536, 1/19],
                       [0, 0.053,-0.429, 0,2.447, 5.43, 1/19],
                       [0.119, 0,0, -0.053,3.363, 8.513, 1/19],
                       [0.119, 0,0, 0.053,3.363, 1.487, 1/19],
                       [0, 0.053,0.429, 0,3.972, 4.569, 1/19],
                       [0.123998, -0.00183957,0.000691208, 0.0629731,6.275,7.716, 1/19],
                       [0, 0.053,0.167, 0,5.215, 6.483, 1/19],
                       [0.071, 0,0, 0.053,6.279, 5.298, 1/19],
                       [0, -0.053,-0.238, 0,6.805, 3.714, 1/19],
                       [-0.121, 0,0, 0.053,5.941, 1.487, 1/19]])

    coord = np.array([0, 0, 1])
    nIter = 15000
    zoom = 35
    xMove = 0
    yMove = -180
    
    ifs(chaos, coord, nIter, zoom, xMove, yMove)
    
def initZigZag():
    clear_canvas()

    zigzag = np.matrix([[-0.63,-0.61,-0.55,0.66,3.84,1.28, 0.5],
                         [-0.04,0.44,0.21,0.04,2.07,8.33,0.5]])

    coord = np.array([0, 0, 1])
    n_iter = 10000
    zoom = 35
    x_move = 0
    y_move = -180

    ifs(zigzag, coord, n_iter, zoom, x_move, y_move)

def initLeaf():
    clear_canvas()

    zigzag = np.matrix([[0.242,-0.640,-0.909,-0.318, 4.612,5.593, 0.5],
                         [-0.091,-0.557,-0.485, 0.155,-1.064,5.654,0.5]])

    coord = np.array([0, 0, 1])
    n_iter = 10000
    zoom = 35
    x_move = 0
    y_move = -180

    ifs(zigzag, coord, n_iter, zoom, x_move, y_move)

def ifs(transformations, coord, nIter, zoom, xMove, yMove):
    
    nTransformations = np.size(transformations,0)
    probabilities = np.transpose(transformations[:, -1])
    probabilities = probabilities.tolist()[0]
    newCoord = coord
    
    for i in range (nIter):
        
        if i>10:
            x, y = adjust(int(zoom * newCoord.item(0)) + xMove, int(zoom * newCoord.item(1)) + yMove)
            canvas.create_rectangle((x,y) * 2, outline = COLOR, fill= COLOR)

        randomTransformation = np.random.choice(np.arange(0, nTransformations), p=probabilities)
        f = transformations[randomTransformation]
        
        matrix = np.matrix([[f.item(0), f.item(1), f.item(4)],
                            [f.item(2), f.item(3), f.item(5)],
                            [0, 0,  1]])
        
        newCoord = np.array(np.matmul(matrix, newCoord))[0]
        

##########################################################################################################################################
                                                        
                                                        #Create Window and components 
                                                        
##########################################################################################################################################


# Create main window 
window = tk.Tk()
window.title("Gráficos por computador y Realidad Virtual")
window.geometry("1200x600")

# Canvas dimensions
canvas_width = 600  
canvas_height = 400  

canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="white")

canvas.place(x=40, y=60)

#############################################################################################################################################################################

iterField = tk.Text(window,height=1, width=5)
iterField.place(x=700, y=275)
imageLbl = tk.Label(image='', background='white')
imageLbl .place(x=45, y=65)

iterLbl = tk.Label(window, text = "Recursive Fractals", font=("Arial", 12))
iterLbl.place(x=700, y=75)

# Agrega botones para los fractales
# Sierpinski triangle
sierpinskiButton = tk.Button(window, width=15, text="Sierpinski Triangle", command=lambda: initSierpinski(-125, -108, 0, 108, 125, -108))
sierpinskiButton.place(x=700, y=125)

# Korch curve
korchButton = tk.Button(window, width=15, text="Korch Curve", command=lambda: initKorch(125, 0, -125, 0))
korchButton.place(x=700, y=175)

# Sierpinski carpet
carpetButton = tk.Button(window, width=15, text="Sierpinski Carpet", command=lambda: initCarpet(-100, 100, 100, 100, 100, -100, -100, -100))
carpetButton.place(x=700, y=225)


#############################################################################################################################################################################

complexLbl = tk.Label(window, text = "Fractals based on complex functions", font=("Arial", 12))
complexLbl.place(x=900, y=75)
# Mandelbrot
mandelbrotButton = tk.Button(window, width = 20, text = "Mandelbrot", command = initMandelbrot, activebackground=ACTIVE_BUTTON_COLOR)
mandelbrotButton.place(x=900, y=125) 

# Julia
juliaButton = tk.Button(window, width = 20, text = "Julia", command = initJulia, activebackground=ACTIVE_BUTTON_COLOR)
juliaButton.place(x=900, y=175) 

#############################################################################################################################################################################

# Barnsley fern
barnsleyButton = tk.Button(window, width = 20, text = "Barnsley Fern", command = initBarnsley, activebackground=ACTIVE_BUTTON_COLOR)
barnsleyButton.place(x=700, y=395) 

# Crystal
crystalButton = tk.Button(window, width = 20, text = "Crystal", command = initCrystal, activebackground=ACTIVE_BUTTON_COLOR)
crystalButton.place(x=850, y=395) 

# Dragon
dragonButton = tk.Button(window, width = 20, text = "Dragon", command = initDragon, activebackground=ACTIVE_BUTTON_COLOR)
dragonButton.place(x=700, y=425) 

# Chaos
chaosButton = tk.Button(window, width = 20, text = "Chaos", command = initChaos, activebackground=ACTIVE_BUTTON_COLOR)
chaosButton.place(x=850, y=425) 

# ZigZag
zigZagButton = tk.Button(window, width = 20, text = "ZigZag", command = initZigZag, activebackground=ACTIVE_BUTTON_COLOR)
zigZagButton.place(x=700, y=455) 

# Leaf
leafButton = tk.Button(window, width = 20, text = "Leaf2", command = initLeaf, activebackground=ACTIVE_BUTTON_COLOR)
leafButton.place(x=850, y=455) 

ifsLbl = tk.Label(window, text = "Iterated Function Systems", font=("Arial", 12))
ifsLbl.place(x=750, y=355)

window.mainloop()