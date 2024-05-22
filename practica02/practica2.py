# -*- coding: utf-8 -*-
"""
@author: ARAHI FERNANDEZ MONAGAS
"""

import tkinter as tk
import math
import numpy as np
from tkinter import colorchooser
from tkinter import filedialog
from PIL import Image, ImageDraw
from tkinter import messagebox


# Variables globales para almacenar las coordenadas de los puntos de inicio y fin
x0, y0, x1, y1 = None, None, None, None
global LINE_COLOR
global LINE_WIDTH

LINE_COLOR = '#000000'
LINE_WIDTH = 1  # Grosor de línea predeterminado

buffer = []
drawn_lines = [] # Lista para mantener un registro de las líneas dibujadas
transformed_lines = []  # Lista para mantener las líneas transformadas

current_scale = 1.0


MAX_POINTS_TO_DISPLAY = 100 # Número máximo de puntos a mostrar en la lista

tx = ty = 0
sx = sy = 1.0
angle_degrees = 0
shx = shy = 0
rx = ry = 0
##########################################################################################################################################

#                                                           DIBUJAR LAS LINEAS

##########################################################################################################################################

# Function to plot a point
def draw_plot_point(canvas, x, y, color):
    x_adjusted = x + canvas_width / 2
    y_adjusted = canvas_height / 2 - y
    canvas.create_rectangle(x_adjusted, y_adjusted, x_adjusted + 1, y_adjusted + 1, fill=color, outline=color, tags="line", width=LINE_WIDTH)
    store_points(x, y)
    
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
        x0, y0 = event.x - canvas_width / 2, canvas_height / 2 - event.y
    else:
        x1, y1 = event.x - canvas_width / 2, canvas_height / 2 - event.y
        # Dibujar la línea entre los puntos de inicio y fin
        if selected_algorithm == "DDA":
            dda_line(x0, y0, x1, y1)
        elif selected_algorithm == "Bresenham":
            bresenham_line(x0, y0, x1, y1)
        elif selected_algorithm == "SlopeIntercept":
            slopeIntercept_base(x0, y0, x1, y1)
        elif selected_algorithm == "SlopeIntercept_AllCases":
            slopeIntercept_AllCases(x0, y0, x1, y1)

        drawn_lines.append([x0, y0, x1, y1])
        # Reiniciar las coordenadas para la próxima línea
        x0, y0, x1, y1 = None, None, None, None

##########################################################################################################################################

#                                                              TRANSFORMATIONS 

##########################################################################################################################################

# Function to apply transformations to all lines 
def translation_redraw():
    global drawn_lines, tx, ty, sx, sy, angle_degrees
    new_transformed_lines = [] #almacenar las lineas con sus coordenadas iniciales
    
    for line in drawn_lines:
        x0, y0, x1, y1 = line
        x0_trasladado, y0_trasladado = traslation(x0, y0, tx, ty)
        x1_trasladado, y1_trasladado = traslation(x1, y1, tx, ty)
        new_transformed_lines.append([x0_trasladado, y0_trasladado, x1_trasladado, y1_trasladado])
    
    transformed_lines = new_transformed_lines  # Actualizar las líneas transformadas
    canvas.delete("line")

    # Redibujar las líneas con las coordenadas actualizadas
    redraw(transformed_lines)

def redraw_scale():
    global drawn_lines, sx, sy
    new_transformed_lines = [] #almacenar las lineas con sus coordenadas iniciales
    
    for line in drawn_lines:
        x0, y0, x1, y1 = line
        x0_escalado, y0_escalado = scale(x0, y0, sx, sy)
        x1_escalado, y1_escalado= scale(x1, y1, sx, sy)
    
        new_transformed_lines.append([x0_escalado, y0_escalado, x1_escalado, y1_escalado])
    
    transformed_lines = new_transformed_lines  # Actualizar las líneas transformadas
    canvas.delete("line")
    #redibuja las lineas
    redraw(transformed_lines)

def redraw_rotation():
    global drawn_lines, angle_degrees
    new_transformed_lines = [] #almacenar las lineas con sus coordenadas iniciales

    for line in drawn_lines:
        x0, y0, x1, y1 = line
        x0_rotado, y0_rotado = rotate(x0, y0, angle_degrees)
        x1_rotado, y1_rotado = rotate(x1, y1, angle_degrees)
        new_transformed_lines.append([x0_rotado, y0_rotado, x1_rotado, y1_rotado])
    
    transformed_lines = new_transformed_lines  # Actualizar las líneas transformadas
    canvas.delete("line")

    #redibuja las lineas
    redraw(transformed_lines)

def redraw_reflexion_x():
    global drawn_lines
    new_transformed_lines = []  # Almacenar las líneas con sus coordenadas iniciales
    
    for line in drawn_lines:
        x0, y0, x1, y1 = line
        x0_reflejado, y0_reflejado = reflexion_x(x0, y0)
        x1_reflejado, y1_reflejado = reflexion_x(x1, y1)
        new_transformed_lines.append([x0_reflejado, y0_reflejado, x1_reflejado, y1_reflejado])
    
    transformed_lines = new_transformed_lines  # Actualizar las líneas transformadas
    canvas.delete("line")
    
    # Redibujar las líneas con las coordenadas actualizadas
    redraw(transformed_lines)

def redraw_reflexion_y():
    global drawn_lines
    new_transformed_lines = []  # Almacenar las líneas con sus coordenadas iniciales
    
    for line in drawn_lines:
        x0, y0, x1, y1 = line
        x0_reflejado, y0_reflejado = reflexion_y(x0, y0)
        x1_reflejado, y1_reflejado = reflexion_y(x1, y1)
        new_transformed_lines.append([x0_reflejado, y0_reflejado, x1_reflejado, y1_reflejado])
    
    transformed_lines = new_transformed_lines  # Actualizar las líneas transformadas
    canvas.delete("line")
    
    # Redibujar las líneas con las coordenadas actualizadas
    redraw(transformed_lines)

def shear_redraw():
    global drawn_lines
    new_transformed_lines = []
    
    for line in drawn_lines:
        x0, y0, x1, y1 = line
        x0_sheared, y0_sheared = shearing(x0, y0, shx, shy)
        x1_sheared, y1_sheared = shearing(x1, y1, shx, shy)
        new_transformed_lines.append([x0_sheared, y0_sheared, x1_sheared, y1_sheared])
    
    transformed_lines = new_transformed_lines
    canvas.delete("line")
    redraw(transformed_lines)
#Esta funcion recibe como parametro la lista con las lineas transformadas y las redibuja
def redraw(transformed_lines):
    global drawn_lines
    drawn_lines = []
    for line in transformed_lines:
        x0, y0, x1, y1 = line
        if algorithm_var.get() == "DDA":
            dda_line(x0, y0, x1, y1)
        elif algorithm_var.get() == "Bresenham":
            bresenham_line(x0, y0, x1, y1)
        elif algorithm_var.get() == "SlopeIntercept":
            slopeIntercept_base(x0, y0, x1, y1)
        elif algorithm_var.get() == "SlopeIntercept_AllCases":
            slopeIntercept_AllCases(x0, y0, x1, y1)
        drawn_lines.append([x0, y0, x1, y1])
        x0, y0, x1, y1 = None, None, None, None

def traslation(x, y, tx, ty):

    matriz_transformacion = np.array([[1, 0, tx],
                              [0, 1, ty],
                              [0, 0, 1]])
    
    vector_original = np.array([x, y, 1])

    transformacion = np.dot(matriz_transformacion, vector_original)

    x_transformada = transformacion[0]
    y_transformada = transformacion[1]

    return x_transformada, y_transformada

def scale(x, y, sx, sy):
    matriz_transformacion = np.array([[sx, 0, 0],
                              [0, sy, 0],
                              [0, 0, 1]])
    
    vector_original = np.array([x, y, 1])

    transformacion = np.dot(matriz_transformacion, vector_original)

    x_transformada = transformacion[0]
    y_transformada = transformacion[1]

    return x_transformada, y_transformada

def rotate(x, y, angle_degrees):
    angle_radians = math.radians(angle_degrees)
    cos_theta = math.cos(angle_radians)
    sin_theta = math.sin(angle_radians)

    matriz_transformacion = np.array([[cos_theta, -sin_theta, 0],
                              [sin_theta, cos_theta, 0],
                              [0, 0, 1]])
    
    vector_original = np.array([x, y, 1])

    transformacion = np.dot(matriz_transformacion, vector_original)

    x_transformada = transformacion[0]
    y_transformada = transformacion[1]

    return x_transformada, y_transformada

def reflexion_x(x, y,):

    matriz_transformacion = np.array([[1, 0, 0],
                                   [0, -1, 0],
                                   [0, 0, 1]])
    
    vector_original = np.array([x, y, 1])
    transformacion = np.dot(matriz_transformacion, vector_original)
    
    x_transformada = transformacion[0]
    y_transformada = transformacion[1]
    
    return x_transformada, y_transformada

def reflexion_y(x, y):
    matriz_reflexion_y = np.array([[-1, 0, 0],
                                   [0, 1, 0],
                                   [0, 0, 1]])
    
    vector_original = np.array([x, y, 1])
    transformacion = np.dot(matriz_reflexion_y, vector_original)
    
    x_transformada = transformacion[0]
    y_transformada = transformacion[1]
    
    return x_transformada, y_transformada

def reflect_over_arbitrary_origin(x, y):
    reflectionMatrix = np.matrix([[-1, 0, 0],
                                  [0, -1, 0],
                                  [0, 0, 1]]).astype('float64')

    # Convert coordinates to homogeneous coordinates
    point = np.matrix([x, y, 1]).astype('float64')

    # Apply reflection matrix
    reflected_point = reflectionMatrix * point.T
    reflected_point = reflected_point.T.tolist()[0][:2]

    return reflected_point[0], reflected_point[1]

def reflect_over_arbitrary_line(x, y, m_arbitrary, b_arbitrary):
    reflectionMatrix = np.matrix([[1 - m_arbitrary * m_arbitrary, 2 * m_arbitrary, -2 * m_arbitrary * b_arbitrary],
                                  [2 * m_arbitrary, m_arbitrary * m_arbitrary - 1, 2 * b_arbitrary],
                                  [0, 0, 1]]).astype('float64')
    reflectionMatrix = (1 / (1 + m_arbitrary * m_arbitrary)) * reflectionMatrix

    # Convert coordinates to homogeneous coordinates
    point = np.matrix([x, y, 1]).astype('float64')

    # Apply reflection matrix
    reflected_point = reflectionMatrix * point.T
    reflected_point = reflected_point.T.tolist()[0][:2]

    return reflected_point[0], reflected_point[1]
    
def shearing(x, y, shx, shy):

    shear_matrix = np.array([[1, shx, 0],
                            [shy, 1, 0],
                            [0, 0, 1]])
    
    # Punto original
    original_point = np.array([x, y, 1])
    
    # Aplicar la transformación de cizalla
    transformed_point = np.dot(shear_matrix, original_point)
    
    # Coordenadas transformadas
    x_transformed = transformed_point[0]
    y_transformed = transformed_point[1]
    
    return x_transformed, y_transformed

def apply_translation():
    global tx, ty, sx, sy, angle_degrees
    tx = float(translation_x_entry.get())
    ty = float(translation_y_entry.get())
    translation_redraw()
    
def apply_scale():
    global sx, sy
    sx = float(scaling_x_entry.get())
    sy = float(scaling_y_entry.get())
    redraw_scale()

def apply_rotation():
    global angle_degrees
    angle_degrees = float(rotation_angle_entry.get())
    rotation_direction = rotation_direction_var.get()

    if rotation_direction == "Sentido Horario":
        angle_degrees = -angle_degrees  # Cambiar el signo para rotación antihoraria

    redraw_rotation()

def apply_shearing():
    global shx, shy
    shx = float(shear_x_entry.get())
    shy = float(shear_y_entry.get())

    shear_redraw()
# Función para cambiar la dirección de rotación
def change_rotation_direction():
    selected_direction = rotation_direction_var.get()
    rotation_direction_display.config(text=selected_direction)

def apply_reflection_origin():
    global drawn_lines
    new_transformed_lines = []

    for line in drawn_lines:
        x0, y0, x1, y1 = line
        x0_reflected, y0_reflected = reflect_over_arbitrary_origin(x0, y0)
        x1_reflected, y1_reflected = reflect_over_arbitrary_origin(x1, y1)
        new_transformed_lines.append([x0_reflected, y0_reflected, x1_reflected, y1_reflected])

    transformed_lines = new_transformed_lines
    canvas.delete("line")
    redraw(transformed_lines)

def apply_reflection_arbitrary_line():
    global drawn_lines
    new_transformed_lines = []

    for line in drawn_lines:
        x0, y0, x1, y1 = line
        m_arbitrary = float(m_arbitrary_entry.get())
        b_arbitrary = float(b_arbitrary_entry.get())
        x0_reflected, y0_reflected = reflect_over_arbitrary_line(x0, y0, m_arbitrary, b_arbitrary)
        x1_reflected, y1_reflected = reflect_over_arbitrary_line(x1, y1, m_arbitrary, b_arbitrary)
        new_transformed_lines.append([x0_reflected, y0_reflected, x1_reflected, y1_reflected])

    transformed_lines = new_transformed_lines
    canvas.delete("line")
    redraw(transformed_lines)
##########################################################################################################################################

#                                                              Aesthetic functions 

##########################################################################################################################################
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
    drawn_lines.clear()
    transformed_lines.clear()

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
        adjusted_points.append(f"[{int(adjusted_x)}, {int(adjusted_y)}]")
    points_label.delete(1, 'end')  # Borra todas las entradas existentes en points_label
    for point in adjusted_points:
        points_label.insert('end', point)  # Agrega las coordenadas ajustadas

def on_canvas_mouse_move(event):
    x = event.x - canvas_width / 2
    y = canvas_height / 2 - event.y
    status_label.config(text=f'Coordenadas: ({x}, {y})')

##########################################################################################################################################
                                                        
                                                        #Create Window and components 
                                                        
##########################################################################################################################################


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

                                                    #   B  O   T   O   N   E   S    #

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
points_label = tk.Listbox(window, width = 30, height = 10)
points_label.insert(0, "List of points:")
points_label.insert(1, "")
points_label.place(x=750, y=75)


#show coordinates
canvas.bind('<Motion>', on_canvas_mouse_move)
status_label = tk.Label(window, text='', bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.pack(side=tk.BOTTOM, fill=tk.X)



############################### T R A N S F O R M A T I O N S #############################################


# Campo de entrada para la traslación en X
translation_x_label = tk.Label(window, text="Traslación en X:")
translation_x_label.place(x=650, y=250)
translation_x_entry = tk.Entry(window, width=5)
translation_x_entry.place(x=770, y=250)
translation_x_entry.insert(0, "0")  # Valor predeterminado

# Campo de entrada para la traslación en Y
translation_y_label = tk.Label(window, text="Traslación en Y:")
translation_y_label.place(x=650, y=300)
translation_y_entry = tk.Entry(window, width=5)
translation_y_entry.place(x=770, y=300)
translation_y_entry.insert(0, "0")  # Valor predeterminado

# Botón para aplicar la traslación
apply_translation_button = tk.Button(window, text="Aplicar", command=apply_translation)
apply_translation_button.place(x=770, y=350)

# Campo de entrada para la escala en X
scaling_x_label = tk.Label(window, text="Escala en X:")
scaling_x_label.place(x=850, y=250)
scaling_x_entry = tk.Entry(window, width=5)
scaling_x_entry.place(x=925, y=250)
scaling_x_entry.insert(0, "1")  # Valor predeterminado

# Campo de entrada para la escala en Y
scaling_y_label = tk.Label(window, text="Escala en Y:")
scaling_y_label.place(x=850, y=300)
scaling_y_entry = tk.Entry(window, width=5)
scaling_y_entry.place(x=925, y=300)
scaling_y_entry.insert(0, "1")  # Valor predeterminado

# Botón para aplicar el escalado
apply_scaling_button = tk.Button(window, text="Aplicar", command=apply_scale)
apply_scaling_button.place(x=925, y=350)

# Campo de entrada para el ángulo de rotación
rotation_angle_label = tk.Label(window, text="Ángulo de Rotación:")
rotation_angle_label.place(x=650, y=400)
rotation_angle_entry = tk.Entry(window, width=5)
rotation_angle_entry.place(x=770, y=400)
rotation_angle_entry.insert(0, "0")  # Valor predeterminado

# Variable para rastrear la dirección de la rotación
rotation_direction_var = tk.StringVar()
rotation_direction_var.set("Sentido Horario")

# Radio buttons para seleccionar la dirección de rotación
radio_button_horario = tk.Radiobutton(window, text="Sentido Horario", variable=rotation_direction_var, value="Sentido Horario", command=change_rotation_direction)
radio_button_antihorario = tk.Radiobutton(window, text="Sentido Antihorario", variable=rotation_direction_var, value="Sentido Antihorario", command=change_rotation_direction)

# Etiqueta para mostrar la dirección actual de la rotación
rotation_direction_label = tk.Label(window, text="Dirección de Rotación:")
rotation_direction_label.place(x=650, y=475)

# Agregar los radio buttons
radio_button_horario.place(x=650, y=520)
radio_button_antihorario.place(x=775, y=520)

# Etiqueta dinámica que muestra la dirección de rotación seleccionada
rotation_direction_display = tk.Label(window, textvariable=rotation_direction_var)
rotation_direction_display.place(x=650, y=500)

# Botón para aplicar la rotación
apply_rotation_button = tk.Button(window, text="Aplicar", command=apply_rotation)
apply_rotation_button.place(x=770, y=450)

# Botón para aplicar reflexión en el eje X
apply_reflection_x_button = tk.Button(window, text="Aplicar Reflexión X", command=redraw_reflexion_x)
apply_reflection_x_button.place(x=850, y=400)

# Botón para aplicar reflexión en el eje Y
apply_reflection_y_button = tk.Button(window, text="Aplicar Reflexión Y", command=redraw_reflexion_y)
apply_reflection_y_button.place(x=850, y=450)

# Etiqueta y campo de entrada para la cizalla en X
shear_x_label = tk.Label(window, text="Cizalla en X:")
shear_x_label.place(x=1000, y=250)
shear_x_entry = tk.Entry(window, width=5)
shear_x_entry.place(x=1075, y=250)
shear_x_entry.insert(0, "0")  # Valor predeterminado

# Etiqueta y campo de entrada para la cizalla en Y
shear_y_label = tk.Label(window, text="Cizalla en Y:")
shear_y_label.place(x=1000, y=300)
shear_y_entry = tk.Entry(window, width=5)
shear_y_entry.place(x=1075, y=300)
shear_y_entry.insert(0, "0")  # Valor predeterminado
# Botón para aplicar la cizalla en X
apply_shear_button = tk.Button(window, text="Aplicar Cizalla", command=apply_shearing)
apply_shear_button.place(x=1000, y=350)


apply_button_origin = tk.Button(window, text="Reflect Over Origin", command=apply_reflection_origin)
apply_button_origin.place(x=850, y=485)

m_arbitrary_label = tk.Label(window, text="y = ")
m_arbitrary_label.place(x=650, y=575)
m_arbitrary_entry = tk.Entry(window, width=5)
m_arbitrary_entry.place(x=675, y=575)
m_arbitrary_entry.insert(0, "1")  # Valor predeterminado

b_arbitrary_label = tk.Label(window, text="*x  +  ")
b_arbitrary_label.place(x=725, y=575)
b_arbitrary_entry = tk.Entry(window, width=5)
b_arbitrary_entry.place(x=760, y=575)
b_arbitrary_entry.insert(0, "0")  # Valor predeterminado

apply_button_arbitrary_line = tk.Button(window, text="Reflect Over Arbitrary Line", command=apply_reflection_arbitrary_line)
apply_button_arbitrary_line.place(x=800, y=575)

# Iniciar el bucle principal de Tkinter
window.mainloop()