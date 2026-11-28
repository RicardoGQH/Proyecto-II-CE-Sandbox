'''
Archivo destinado a el sistema de guardado del proyecto
introducción a la Programción
segundo semestre del 2026
Ricardo Gómez Quesada
Jesus Guerrero Zamora
'''

#Librerias importadas============================================================================================================
import tkinter as tk
from tkinter import filedialog
from Elementos import *
import random
import json

#Funciones=======================================================================================================================
#Funcion que carga una matriz seleccionada
#entradas: la funcion como tal no tiene, pero se debe ingresar un archivo
#salidas: retorna el archivo que se debe de cargar
#efectos: La matriz guardada pasa a ser la matriz cargada
def cargar_matriz():
    global matriz_guardada
    ventana = tk.Tk()
    ventana.withdraw()
    ventana.attributes("-topmost", True)
    ruta = filedialog.askopenfilename(title="Selecciona una matriz", filetypes=[("JSON", "*.json"), ("Todos", "*.*")])

    ventana.destroy()

    if not ruta:            # el usuario canceló
        return None

    with open(ruta, encoding="utf-8") as f:
        return json.load(f)
    
#funcion que guarda una matriz
#entradas: la matriz que se quiere guardar
#salidas: no tine salidas
#efectos: se crea un archivo json con la matriz para ser cargada posteriormente

def guardar_matriz(matriz):
    ventana = tk.Tk()
    ventana.withdraw()
    ventana.attributes("-topmost", True)
    ruta = filedialog.asksaveasfilename(title="Guardar matriz como",defaultextension=".json", filetypes=[("JSON", "*.json")])
    ventana.destroy()

    if not ruta:            # el usuario canceló
        return False

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(matriz, f)
    return True