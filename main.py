import time
import random
import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox

root = tk.Tk()
root.title("Win with Mariana")
root.geometry("1100x855")

# --- CONTROLES ---
panel_controles = tk.Frame(root, bg="gray10", padx=10, pady=10)
panel_controles.pack(fill=tk.X, side=tk.TOP)

# Rondas
tk.Label(panel_controles, text="Rondas:", fg="white", bg="gray10", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
entry_rondas = tk.Entry(panel_controles, width=5, font=("Arial", 11))
entry_rondas.insert(0, "1")
entry_rondas.pack(side=tk.LEFT, padx=5)

# Apuesta
tk.Label(panel_controles, text="Apuesta:", fg="white", bg="gray10", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
combo_apuesta = ttk.Combobox(panel_controles, values=[str(i) for i in range(1, 11)], width=5, state="readonly", font=("Arial", 11))
combo_apuesta.current(0)
combo_apuesta.pack(side=tk.LEFT, padx=5)

# Velocidad
tk.Label(panel_controles, text="Velocidad:", fg="white", bg="gray10", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
slider_tiempo = tk.Scale(panel_controles, from_=10, to=100, orient=tk.HORIZONTAL, bg="gray10", fg="white", highlightthickness=0)
slider_tiempo.set(30)
slider_tiempo.pack(side=tk.LEFT, padx=5)


# --- CREACIÓN DE LA PISTA ---
canvas = tk.Canvas(root, width=1000, height=500, bg="forest green")
canvas.pack(fill=tk.BOTH, expand=True)

def dibujar_pista():
    for y in range(40, 480, 40):
        canvas.create_line(50, y, 950, y, fill="white", dash=(10, 10), width=2)
    canvas.create_line(90, 40, 90, 440, fill="yellow", width=4)
    canvas.create_line(850, 40, 850, 440, fill="red", width=4)

dibujar_pista()


# --- CREACIÓN DE LOS CABALLOS ---
img1 = PhotoImage(file="caballo1.png")
caballo1 = canvas.create_image(90, 40, image=img1, anchor="nw")
canvas.img1 = img1
img2 = PhotoImage(file="caballo2.png")
caballo2 = canvas.create_image(90, 80, image=img2, anchor="nw")
canvas.img2 = img2
img3 = PhotoImage(file="caballo3.png")
caballo3 = canvas.create_image(90, 120, image=img3, anchor="nw")
canvas.img3 = img3
img4 = PhotoImage(file="caballo4.png")
caballo4 = canvas.create_image(90, 160, image=img4, anchor="nw")
canvas.img4 = img4
img5 = PhotoImage(file="caballo5.png")
caballo5 = canvas.create_image(90, 200, image=img5, anchor="nw")
canvas.img5 = img5
img6 = PhotoImage(file="caballo6.png")
caballo6 = canvas.create_image(90, 240, image=img6, anchor="nw")
canvas.img6 = img6
img7 = PhotoImage(file="caballo7.png")
caballo7 = canvas.create_image(90, 280, image=img7, anchor="nw")
canvas.img7 = img7
img8 = PhotoImage(file="caballo8.png")
caballo8 = canvas.create_image(90, 320, image=img8, anchor="nw")
canvas.img8 = img8
img9 = PhotoImage(file="caballo9.png")
caballo9 = canvas.create_image(90, 360, image=img9, anchor="nw")
canvas.img9 = img9
img10 = PhotoImage(file="caballo10.png")
caballo10 = canvas.create_image(90, 400, image=img10, anchor="nw")
canvas.img10 = img10

caballos = [caballo1, caballo2, caballo3, caballo4, caballo5, caballo6, caballo7, caballo8, caballo9, caballo10]


# --- LÓGICA DE CONTROL ---
carrera_terminada = False
carrera_iniciada = False
tiempos_finales = {}
tiempo_inicio = 0

direcciones = [1] * 10
velocidades = [random.randint(2, 8) for _ in range(10)]
rondas_actuales = [0] * 10
rondas_totales_objetivo = 1


# --- TIMERS INDEPENDIENTES ---
def mover_caballo_individual(index):
    global carrera_terminada, tiempos_finales
    
    if carrera_terminada or rondas_actuales[index] >= rondas_totales_objetivo:
        return

    caballo = caballos[index]
    direccion = direcciones[index]
    velocidad = velocidades[index]

    canvas.move(caballo, velocidad * direccion, 0)
    pos = canvas.coords(caballo)
    coordenada_x = pos[0]

    # Rebotes y giros
    if direccion == 1 and coordenada_x >= 810:
        direcciones[index] = -1
        velocidades[index] = random.randint(2, 8)
    elif direccion == -1 and coordenada_x <= 90:
        direcciones[index] = 1
        velocidades[index] = random.randint(2, 8)
        rondas_actuales[index] += 1

        # Fin de rondas
        if rondas_actuales[index] == rondas_totales_objetivo:
            tiempos_finales[index + 1] = time.time() - tiempo_inicio
            if not carrera_terminada:
                carrera_terminada = True
                evaluar_ganador(index + 1)
            return

    if not carrera_terminada:
        root.after(slider_tiempo.get(), lambda: mover_caballo_individual(index))


# --- FUNCIONES DE CARRERA ---
def iniciar_carrera():
    global carrera_iniciada, tiempo_inicio, rondas_totales_objetivo, carrera_terminada, tiempos_finales
    if carrera_iniciada:
        return
        
    try:
        rondas_totales_objetivo = int(entry_rondas.get())
    except ValueError:
        messagebox.showerror("Error", "Ingresa un número válido.")
        return

    carrera_iniciada = True
    carrera_terminada = False
    tiempos_finales.clear()
    tiempo_inicio = time.time()
    
    # Se limpia el cartel de la carrera anterior si existiera
    canvas.delete("texto_ganador")
    
    for i in range(10):
        mover_caballo_individual(i)

def evaluar_ganador(numero_ganador):
    apuesta = int(combo_apuesta.get())
    if apuesta == numero_ganador:
        res = f"¡Ganó el caballo {numero_ganador}!\n\n¡Felicidades! Acertaste. 🥇"
    else:
        res = f"¡Ganó el caballo {numero_ganador}!\n\nPerdiste. Apostaste por el {apuesta}. ❌"
        
    # Agregamos la etiqueta "texto_ganador" para borrar solo este texto al reiniciar
    canvas.create_text(500, 250, text=res, font=("Arial", 22, "bold"), fill="yellow", justify=tk.CENTER, tag="texto_ganador")
    root.after(1500, mostrar_tabla)

def mostrar_tabla():
    ventana_tabla = tk.Toplevel(root)
    ventana_tabla.title("Tiempos")
    ventana_tabla.geometry("350x400")
    ventana_tabla.config(bg="gray15")
    
    tk.Label(ventana_tabla, text="Puesto | Caballo | Tiempo", fg="cyan", bg="gray15", font=("Arial", 12, "bold")).pack(pady=10)
    
    posiciones_ordenadas = sorted(tiempos_finales.items(), key=lambda item: item[1])
    for idx, (num, t) in enumerate(posiciones_ordenadas):
        fila = f"  N° {idx+1}   |   Caballo {num}   |   {t:.2f}s"
        tk.Label(ventana_tabla, text=fila, fg="white", bg="gray15", font=("Arial", 11)).pack(pady=4)

def reiniciar_carrera():
    global carrera_terminada, carrera_iniciada, direcciones, velocidades, rondas_actuales
    carrera_terminada = True
    carrera_iniciada = False
    
    # Quitamos canvas.delete("all") para evitar que borre tus caballos.
    # Ahora solo eliminamos el letrero amarillo del ganador.
    canvas.delete("texto_ganador")
    
    # Reubicar de forma segura las imágenes de los caballos en la salida
    for i, caballo in enumerate(caballos):
        canvas.coords(caballo, 90, 40 + (i * 40))
        
    direcciones = [1] * 10
    velocidades = [random.randint(2, 8) for _ in range(10)]
    rondas_actuales = [0] * 10
    messagebox.showinfo("Reiniciar", "¡Pista reiniciada!")


# --- BOTONES ---
btn_iniciar = tk.Button(panel_controles, text="Iniciar", font=("Arial", 11, "bold"), command=iniciar_carrera, bg="green", fg="white")
btn_iniciar.pack(side=tk.LEFT, padx=15)

btn_reiniciar = tk.Button(panel_controles, text="Reiniciar", font=("Arial", 11, "bold"), command=reiniciar_carrera, bg="orange", fg="black")
btn_reiniciar.pack(side=tk.LEFT, padx=5)

root.mainloop()
