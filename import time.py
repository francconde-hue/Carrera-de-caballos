import time
import random
import tkinter as tk
from tkinter import PhotoImage

root = tk.Tk()
root.title("Win with Mariana")
root.geometry("1100 integrity=700") # Ajustado el tamaño de la ventana
root.geometry("1100x700")

canvas = tk.Canvas(root, width=1000, height=600, bg="gray20")
canvas.pack(fill=tk.BOTH, expand=True)

def dibujar_pista():
    # Se corrigió la línea de abajo añadiendo la lista de coordenadas Y
    for y in:
        canvas.create_line(50, y, 950, y, fill="white", dash=(10, 10), width=2)
    
    # Líneas de salida (amarilla) y meta (roja)
    canvas.create_line(90, 40, 90, 440, fill="yellow", width=4)
    canvas.create_line(850, 40, 850, 440, fill="red", width=4)

dibujar_pista()

# Crear los caballos cargando las imágenes de forma segura
caballos = []
for i in range(1, 11):
    try:
        img = PhotoImage(file=f"caballo{i}.png")
        # Guardar la referencia de la imagen para que no la borre el recolector de basura
        setattr(canvas, f"img{i}", img)
        
        # Calcular posición Y para cada caballo
        pos_y = 10 + (i * 40) 
        caballo = canvas.create_image(90, pos_y, image=img, anchor="nw")
        caballos.append(caballo)
    except Exception as e:
        # Si no encuentra la imagen, crea un rectángulo temporal para que no falle el programa
        print(f"No se pudo cargar caballo{i}.png, usando sustituto.")
        caballo = canvas.create_rectangle(90, 20 + (i * 40), 130, 40 + (i * 40), fill="orange")
        caballos.append(caballo)

carrera_terminada = False

# Función para mover los caballos de manera aleatoria
def mover_caballos():
    global carrera_terminada
    if carrera_terminada:
        return
        
    for i, caballo in enumerate(caballos):
        # Mover una cantidad aleatoria de píxeles hacia la derecha
        avance = random.randint(2, 8)
        canvas.move(caballo, avance, 0)
        
        # Obtener la posición actual del caballo
        pos = canvas.coords(caballo)
        coordenada_x = pos[0]
        
        # Ajustamos el límite a 810 para compensar el ancho del caballo antes de la línea roja
        if coordenada_x >= 810:
            carrera_terminada = True
            numero_ganador = i + 1
            canvas.create_text(
                500, 250, 
                text=f"¡El caballo {numero_ganador} ha ganado!", 
                font=("Arial", 28, "bold"), 
                fill="yellow"
            )
            break
            
    # Si la carrera sigue, repetir la función después de 30 milisegundos
    if not carrera_terminada:
        root.after(30, mover_caballos)

# Botón para iniciar la carrera
btn_iniciar = tk.Button(
    root, text="Iniciar Carrera", 
    font=("Arial", 14), 
    command=mover_caballos, 
    bg="green", fg="white"
)
btn_iniciar.pack(pady=10)

root.mainloop()
