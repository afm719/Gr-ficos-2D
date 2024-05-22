# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 09:27:01 2023

@author: ARAHI FERNANDEZ MONAGAS
"""

import tkinter as tk
import math
from tkinter import colorchooser
from tkinter import filedialog
from PIL import Image, ImageDraw
from tkinter import messagebox


# Variables globales para almacenar las coordenadas de los puntos de inicio y fin
x0, y0, x1, y1 = None, None, None, None
global LINE_COLOR
LINE_COLOR = '#000000'
global LINE_WIDTH
LINE_WIDTH = 1  # Grosor de línea predeterminado
buffer = []
current_scale = 1.0


# Número máximo de puntos a mostrar en la lista
MAX_POINTS_TO_DISPLAY = 100
##########################################################################################################################################
#DIBUJAR LAS LINEAS
##########################################################################################################################################

# Function to plot a point
def draw_plot_point(canvas, x, y, color):
    canvas.create_rectangle(x, y, x+1, y+1, fill=color, outline = color, tags="line", width=LINE_WIDTH)
    store_points(x, y)
    
##########################################################################################################################################
##########################################################################################################################################

#Función para dibujar una línea en el lienzo usando el algoritmo de Bresenham
#Resumen general: hay dos algoritmos de bresenham para que sea mas eficiente, para pendiente inferior a 45 grados y para 
#superior, en ambos, se recibe como parametros los puntos de inicio y los del final, y va comprobando hasta que los de inicio coincidan con los 
#del final, es decir vamos a ir actualizando el valor de lo inicial de forma que a medida que se actualiza ese nuevo valor se va dibujando en el
#cuadrante un punto y así hasta llegar al punto final donde se termina ya de dibujar. Estos valores se almacenaran en variables globales y su valor
#se restablecera cuando ya se haya dibujado la linea

"""
Algorithm 3: Bresenham's Algorithm
"""
def bresenham_line(x1, y1, x2, y2):
    # Greater displacement in X
    if abs(y2 - y1) < abs(x2 - x1):
        if x1 > x2:
            tempX, tempY = x1, y1
            x1, y1 = x2, y2
            x2, y2 = tempX, tempY
        L = bresenham_line_low(x1, y1, x2, y2)
   
    # Greater displacement in Y 
    else:
        if y1 > y2:
            tempX, tempY = x1, y1
            x1, y1 = x2, y2
            x2, y2 = tempX, tempY
        L = bresenham_line_high(x1, y1, x2, y2)

    for pixel in L:
        draw_plot_point(canvas, pixel[0], pixel[1], LINE_COLOR)

# Función para dibujar una línea en el lienzo usando el algoritmo de Bresenham para pendiente baja
def bresenham_line_low(x1, y1, x2, y2):
    L = []
    dx = x2 - x1
    dy = y2 - y1
    yi = 1
    
    if dy < 0:
        yi = -1
        dy = -dy
    
    ne = (2 * dy) - dx
    x, y = x1, y1

    while (x < x2):
        L.append([x, y])
        if ne > 0:
            y += yi
            ne += (2 * (dy - dx))
        else:
            ne += 2*dy
        x += 1
    return L

# Función para dibujar una línea en el lienzo usando el algoritmo de Bresenham para pendiente alta
def bresenham_line_high(x1, y1, x2, y2):
    L = []
    dx = x2 - x1
    dy = y2 - y1
    xi = 1
    
    if dx < 0:
        xi = -1
        dx = -dx
        
    ne = (2 * dx) - dy
    x, y = x1, y1

    while (y < y2):
        L.append([x, y])
        if ne > 0:
            x += xi
            ne += (2 * (dx - dy))
        else:
            ne += 2*dx
        y += 1
    return L
"""
Algorithm 2: DDA (Digital DIfferential Analyzer
"""
#Función para dibujar una línea en el lienzo usando el algoritmo DDA
def dda_line(x0, y0, x1, y1):

    dx = x1-x0
    dy = y1-y0

    if (abs(dx) >= abs(dy)):
        steps = abs(dx)
    else:
        steps = abs(dy)

    xi = dx / steps
    yi = dy / steps

    x = x0 + 0.5
    y = y0 + 0.5 #inicializacion de los valores con los puntos iniciales
    
    i = 0  # Set i to 0
    while i <= steps:
        # Plot the point (x, y)
        draw_plot_point(canvas, math.floor(x), math.floor(y), LINE_COLOR)
        x = x + xi
        y = y + yi
        i = i + 1

"""
Algorithm 1:  SLOPE INTERCEPT
"""

def slopeIntercept_base(x0, y0, x1, y1):

    # If lines goes from right to left, then swap
    if (x1 < x0):
        tempX, tempY = x0, y0
        x0, y0 = x1, y1
        x1, y1 = tempX, tempY

    L = []
    x = x0 #initial x
    y = y0 #initial y

    dx = x1 - x0
    dy = y1 - y0

    # Calcular la pendiente de la línea (slope)
    m = dy / dx  # pendiente de la línea
    b = y0 - m * x0  # altura de la línea en x=0

    while (x <= x1) :
        L.append([x,y])
        x += 1
        y = round(m * x + b)

    for pixel in L:
        draw_plot_point(canvas, pixel[0], pixel[1], LINE_COLOR)

def slopeIntercept_AllCases(x1, y1, x2, y2):

    # If lines goes from right to left, then swap
    if (x2 < x1):
        tempX, tempY = x1, y1
        x1, y1 = x2, y2
        x2, y2 = tempX, tempY

    x, y = x1, y1               # Initial points
    L = []                      # List of points to be drawn
    
    # m = inf
    if (x1 == x2):
        while(y != y2):
            L.append([x, y])
            y += 1
    
    # m != inf        
    else:
        
        dx, dy= x2- x1, y2 - y1     # Distance
        m = dy / dx             # Slope
        b = y1 - m * x1
    
        if (m > 1 or m < -1):                 
            m = 1 / m
            b = x1 - m * y1         
            #swap
            x, y = y, x                     
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            
            if (x1 > x2):
                 while (x > x2):           
                    L.append([y, x])   
                    x -= 1
                    y = round(m * x + b)
            else:
                while (x < x2):            
                    L.append([y, x])     
                    x += 1
                    y = round(m * x + b)
           
        else:
            while (x < x2):
                L.append([x, y])
                x += 1
                y = round(m * x + b)
                    
      
    for pixel in L:             
        draw_plot_point(canvas, pixel[0], pixel[1],LINE_COLOR)

# Función para dibujar la linea segun el algoritmo que queramos
def on_canvas_click(event):
    global x0, y0, x1, y1
    selected_algorithm = algorithm_var.get()
    if x0 is None or y0 is None:
        x0, y0 = event.x, event.y
    else:
        x1, y1 = event.x, event.y
        # Dibujar la línea entre los puntos de inicio y fin
        if selected_algorithm == "DDA":
            dda_line(x0, y0, x1, y1)
        elif selected_algorithm == "Bresenham":
            bresenham_line(x0, y0, x1, y1)
        elif selected_algorithm == "SlopeIntercept":
            slopeIntercept_base(x0, y0, x1, y1)
        elif selected_algorithm == "SlopeIntercept_AllCases":
            slopeIntercept_AllCases(x0, y0, x1, y1)
        # Reiniciar las coordenadas para la próxima línea
        x0, y0, x1, y1 = None, None, None, None

##########################################################################################################################################



##########################################################################################################################################

#Aesthetic functions
# Function to change the selected color
def change_line_color():
    global LINE_COLOR
    color_code = colorchooser.askcolor(initialcolor=LINE_COLOR)[1]
    if color_code:
        LINE_COLOR = color_code
    canvas.update()
        
def close_window():
    window.destroy()

# Function to clear the canvas
def clear_canvas():
    canvas.delete("line")

# Función para cambiar el grosor de la línea a "Delgada"
def set_line_thickness():
    global LINE_WIDTH
    selected_thickness = selected_thickness_var.get()
    if selected_thickness == "Delgada (1)":
        LINE_WIDTH = 1
    elif selected_thickness == "Mediana (3)":
        LINE_WIDTH = 3
    elif selected_thickness == "Gruesa (5)":
        LINE_WIDTH = 5

def zoom_in():
    global current_scale, current_x_offset, current_y_offset
    current_scale *= 1.2
    canvas.scale("all", canvas_width / 2, canvas_height / 2, 1.2, 1.2)
    current_x_offset = (1 - 1.2) * canvas_width / 2
    current_y_offset = (1 - 1.2) * canvas_height / 2

def zoom_out():
    global current_scale, current_x_offset, current_y_offset
    if current_scale > 1.0:
        current_scale /= 1.2
        canvas.scale("all", canvas_width / 2, canvas_height / 2, 1 / 1.2, 1 / 1.2)
        current_x_offset = (1 - 1 / 1.2) * canvas_width / 2
        current_y_offset = (1 - 1 / 1.2) * canvas_height / 2


# Función para exportar el dibujo como PNG
def export_to_png():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if file_path:
        image = Image.new("RGB", (canvas_width, canvas_height), "white")
        draw = ImageDraw.Draw(image)
        for line in canvas.find_withtag("line"):
            x0, y0, x1, y1 = canvas.coords(line)
            draw.line([(x0, y0), (x1, y1)], fill=LINE_COLOR, width=LINE_WIDTH)
        image.save(file_path, "PNG")

#Función que se usa como tutorial para explicar cada boton
def show_help_popup():
    help_text = """
    Bienvenido a la aplicación de dibujo.

    Para comenzar a dibujar, siga estos pasos:
    1. Seleccione el color de la línea haciendo clic en 'Cambiar Color'.
    2. Elija el grosor de la línea (Delgada, Mediana o Gruesa).
    3. Seleccione un algoritmo de dibujo en el menú desplegable.
    4. Haga clic en el lienzo para comenzar a dibujar.

    Para borrar el dibujo, haga clic en 'Borrar'.

    Puede exportar su dibujo como PNG haciendo clic en 'Exportar a PNG'.

    ¡Disfrute dibujando!
    """
    messagebox.showinfo("Ayuda", help_text)

def store_points(x, y):
    x_adjusted = x
    y_adjusted = -y  # Invertir el eje Y
    buffer.append((x_adjusted, y_adjusted))
    if len(buffer) >= MAX_POINTS_TO_DISPLAY:
        update_points_label()
        buffer.clear()

# Función para actualizar la etiqueta de puntos con coordenadas ajustadas
def update_points_label():
    adjusted_points = []
    for i, point in enumerate(buffer, start=2):
        x, y = point
        adjusted_x = x
        adjusted_y = -y  # Invertir el eje Y
        adjusted_points.append(f"[{adjusted_x}, {adjusted_y}]")
    points_label.delete(2, 'end')  # Borra todas las entradas existentes en points_label
    for point in adjusted_points:
        points_label.insert('end', point)  # Agrega las coordenadas ajustadas

def on_canvas_mouse_move(event):
    x = event.x - canvas_width / 2
    y = canvas_height / 2 - event.y
    status_label.config(text=f'Coordenadas: ({x}, {y})')
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################





##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
"""
Create Window and components 
"""

"CANVAS CREATION"

# Create main window 
window = tk.Tk()
window.title("Gráficos por computador y Realidad Virtual")
window.geometry("1200x600")


# Canvas dimensions
canvas_width = 600  # Width in pixels
canvas_height = 400  # Height in pixels
# Create a Canvas object with specific dimensions
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="white")


# Position the canvas to the left
canvas_x = 10
canvas_y = 10
canvas.place(x=canvas_x, y=canvas_y)


# Dibujar ejes X e Y y almacenar sus IDs
x_axis = canvas.create_line(0, canvas_height / 2, canvas_width, canvas_height / 2, fill="black", width=1)
y_axis = canvas.create_line(canvas_width / 2, 0, canvas_width / 2, canvas_height, fill="black", width=1)

#Personalizacion del canvas
canvas.create_text(canvas_width / 2 + 20, canvas_height / 2 +10, text="(0, 0)", font=("Arial", 8), fill="red")
point_radius = 3 
canvas.create_oval(
    canvas_width/2 - point_radius, canvas_height/2 - point_radius,
    canvas_width/2 + point_radius, canvas_height/2 + point_radius,
    fill="red"
)

##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################



##########################################################################################################################################
                                                    #B  O   T   O   N   E   S#
##########################################################################################################################################

# Etiqueta para el menú de edición
label = tk.Label(window, text="Menú de Edición", font=("Helvetica", 24))
label.place(x=800, y=10)

# Botón de Cambiar Color
color_button = tk.Button(window, text="Cambiar Color", command=change_line_color)
color_button.place(x=390, y=460)

# Selector de algoritmo
algorithm_var = tk.StringVar(window)
algorithm_var.set("Selector algoritmo")
algorithm_menu = tk.OptionMenu(window, algorithm_var, "DDA", "Bresenham", "SlopeIntercept", "SlopeIntercept_AllCases")
algorithm_menu.place(x=150, y=425)
canvas.bind("<Button-1>", on_canvas_click)

# Botón Borrar
clear_button = tk.Button(window, text="Borrar", command=clear_canvas)
clear_button.place(x=150, y=460)

# Botón Salir
exit_button = tk.Button(window, text="Salir", command=close_window)
exit_button.place(x=25, y=530)

# Opciones de grosor de línea
thickness_options = ["Delgada (1)", "Mediana (3)", "Gruesa (5)"]
selected_thickness_var = tk.StringVar()
selected_thickness_var.set(thickness_options[0])  # Establecer el valor predeterminado

# Menú de selección de grosor de línea con opciones predeterminadas
thickness_menu = tk.OptionMenu(window, selected_thickness_var, *thickness_options)
thickness_menu.configure(text="Grosor línea")
thickness_menu.place(x= 25, y=425)
# Botón para aplicar el grosor de línea seleccionado
apply_button = tk.Button(window, text="Aplicar Grosor", command=set_line_thickness)
apply_button.place(x= 25, y=460)

# Botones de Zoom
zoom_in_button = tk.Button(window, text="Zoom In", command=zoom_in)
zoom_in_button.place(x=225, y=460)

zoom_out_button = tk.Button(window, text="Zoom Out", command=zoom_out)
zoom_out_button.place(x=300, y=460)

# Botón Exportar a PNG
export_button = tk.Button(window, text="Exportar a PNG", command=export_to_png)
export_button.place(x=25, y=495)

# Botón de Video Tutorial o Ayuda
help_button = tk.Button(window, text="Tutorial", command=show_help_popup)
help_button.place(x=150, y=495)


# Crear una etiqueta para mostrar los puntos
points_label = tk.Listbox(window, width = 30, height = 20)
points_label.insert(0, "List of points:")
points_label.insert(1, "")
points_label.place(x=750, y=75)


#show coordinates
canvas.bind('<Motion>', on_canvas_mouse_move)
status_label = tk.Label(window, text='', bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.pack(side=tk.BOTTOM, fill=tk.X)



# Iniciar el bucle principal de Tkinter
window.mainloop()