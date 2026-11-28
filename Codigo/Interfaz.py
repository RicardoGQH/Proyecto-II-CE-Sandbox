# INFORMACIÓN DEL ARCHIVO
'''
Archivo destinado a la interfaz grafica del proyecto
Introducción a la Programción
segundo semestre del 2026
Ricardo Gómez Quesada
Jesus Guerrero Zamora
'''

#Librerias importadas============================================================================================================
import pygame
import sys
from Carga_y_guardado import *

#INICIALIZACIÓN DE PYGAME =======================================================================================================
pygame.init()
Ventana_principal= pygame.display.set_mode(tamaño_ventana)
pygame.display.set_caption("Sandbox")
rect_inicio = None 

#RECURSOS GRÁFICOS==============================================================================================================

#Texturas
textura = pygame.image.load("recursos\Imagenes\Textura aire.png").convert()
textura_arena = pygame.image.load("recursos\Imagenes\Textura arena.png").convert()
textura_agua= pygame.image.load("recursos\Imagenes\Textura agua.png").convert()
textura_piedra= pygame.image.load("recursos\Imagenes\Textura piedra.png").convert()
textura_tierra= pygame.image.load("recursos\Imagenes\Textura tierra.png").convert()
textura_fuego= pygame.image.load("recursos\Imagenes\Textura fuego.png").convert()
textura_semillas= pygame.image.load("recursos\Imagenes\Textura semillas.png").convert()
textura_pasto= pygame.image.load("recursos\Imagenes\Textura pasto.png").convert()
textura_planta1=pygame.image.load("recursos\Imagenes\Textura planta 1.png").convert()
textura_planta2=pygame.image.load("recursos\Imagenes\Textura planta 2.png").convert()
textura_planta3=pygame.image.load("recursos\Imagenes\Textura planta 3.png").convert()
textura_animal= pygame.image.load("recursos\Imagenes\Textura animal.png").convert()

#fuentes
fuente_titulo= pygame.font.SysFont("Times New Roman",40)
fuente_botones=pygame.font.SysFont("Times New Roman",20)

#FONDO PANTALLA INICIAL
fondo_menu = pygame.image.load("recursos/Imagenes/fondo menu.png")
fondo_menu=pygame.transform.scale(fondo_menu,(800,500))
fondo_color=GRIS

#Audio y musica==================================================================================================================
pygame.mixer.init()
Sonido_pulsado_botones= pygame.mixer.Sound("recursos\Audio\sound10.wav")
Sonido_pulsado_botones.set_volume(0.15)
sonido_vaca=pygame.mixer.Sound("recursos\Audio\sonido vaca.wav")

#FUNCIONES=======================================================================================================================
#Descripción: Carga un archivo de audio en el mixer de pygame y lo reproduce en bucle infinito.
#Entradas: Ruta (str): ruta del archivo de música que se desea reproducir.
#Salidas: Ninguna. 
#Efecto: la canción indicada empieza a sonar y se repite.
def cambiar_musica(Ruta):#
    pygame.mixer.music.load(Ruta)
    pygame.mixer.music.play(-1,0.0)#de esta manera la cancion se repite

# Descripción: Cambia de la ventana del menú a la ventana principal del sandbox y ejecuta su bucle de interacción.
# Entradas: Ninguna.
# Salidas: Ninguna.
# Efectos: Cambia las dimensiones y el título de la ventana, crea el grupo de sprites, genera la matriz del juego, procesa eventos y restaura la ventana del menú al salir.
def pasar_ventana():
    
    global sprites
    global fondo_color, Ventana_principal, run, rect_inicio
    fondo_color=NEGRO
    rect_inicio=None
    Ventana_principal=pygame.display.set_mode((1280,720))
    pygame.display.set_caption("ESTAS JUGANDO")
    en_ventana=True
    sprites=pygame.sprite.Group()
    matriz_juego()

    while en_ventana:
        timer.tick(fps)
        eventos=pygame.event.get()
        for evento in eventos:
            if evento.type==pygame.QUIT:
                en_ventana=False
                run=False
            if evento.type==pygame.KEYDOWN and evento.key==pygame.K_ESCAPE:
                en_ventana=False

        Ventana_principal.fill((30,30,60))
        dibujar_texto("ESC para volver ",fuente_botones,BLANCO,0,0)

        boton_borrar.dibujar_boton(eventos)
        boton_arena.dibujar_boton(eventos)
        boton_agua.dibujar_boton(eventos) 
        boton_piedra.dibujar_boton(eventos)
        boton_tierra.dibujar_boton(eventos)
        boton_fuego.dibujar_boton(eventos)
        boton_semillas.dibujar_boton(eventos)
        boton_pasto.dibujar_boton(eventos)
        boton_animal.dibujar_boton(eventos)
        boton_reiniciar.dibujar_boton(eventos)
        boton_pincel1.dibujar_boton(eventos)
        boton_pincel2.dibujar_boton(eventos)
        boton_pincel3.dibujar_boton(eventos)
        boton_guardar.dibujar_boton(eventos)
        
        aplicar_pincel()
        seleccionar_rectangulo(eventos)
        sprites.update()
        sprites.draw(Ventana_principal)
        pygame.display.flip()

    if run:
        Ventana_principal=pygame.display.set_mode(tamaño_ventana)
        pygame.display.set_caption("Sandbox")

# Descripción: Crea una matriz inicializada con ceros.
# Entradas: filas (cantidad de filas) y columnas (cantidad de columnas).
# Salidas: Una matriz de dimensiones filas × columnas cuyos elementos iniciales son 0.
# Efectos: Ninguno sobre el estado global.
def crear_matrices(filas, columnas):
    matriz=[]
    while filas>0:
        matriz.append([])
        filas-=1
    
    filas=len(matriz)
    for elemento in range(filas):
        for valor in range(columnas):
            matriz[elemento].append(0)
        
    return matriz

# Descripción: Inicializa la matriz del sandbox y crea los sprites que representan sus celdas.
# Entradas: Ninguna; utiliza la variable global dimensiones y el grupo global sprites.
# Salidas: Ninguna.
# Efectos: Actualiza matriz_guardada y tamaño_cuadricula, y agrega objetos cuadriculas al grupo de sprites.
def matriz_juego():
    global sprites, matriz_guardada,tamaño_cuadricula
    global centrar_x,centrar_y
    
    if not matriz_guardada:
        matriz_guardada = crear_matrices(int(dimensiones), int(dimensiones))

    tamaño_cuadricula = min(1280 // int(dimensiones), 720 // int(dimensiones))
    centrar_x= (1280 - tamaño_cuadricula * int(dimensiones)) // 2
    centrar_y= (720 - tamaño_cuadricula * int(dimensiones)) // 2

    for i in range(len(matriz_guardada)):
        for j in range(len(matriz_guardada[i])):
            valor = matriz_guardada[i][j]
            pos = (centrar_x + j * tamaño_cuadricula, centrar_y + i * tamaño_cuadricula)
            cuadriculas(pos, sprites, i, j, tamaño_cuadricula)

# Descripción: Comprueba que la dimensión ingresada sea un número dentro del intervalo permitido.
# Entradas: Ninguna; consulta la variable global dimensiones.
# Salidas: Ninguna.
# Efectos: Dibuja un mensaje si el valor no es válido o inicia la ventana del juego si es válido.
def verificador():
    global filas,columnas,dimensiones,texto_error
    Sonido_pulsado_botones.play()
    if dimensiones.isdigit():
        if len(dimensiones)<=0 or int(dimensiones)<20  or int(dimensiones)>100:
            texto_error="SE DEBE SELECCIONAR UN VALOR ENTRE 20 Y 100"
        else:
            pasar_ventana()
    else:
        texto_error="TIENE QUE RELLENAR EL CUADRO"

# Descripción: Establece el elemento que se utilizará al interactuar con las celdas de la matriz.
# Entradas: numero (identificador del elemento seleccionado).
# Salidas: El valor de numero.
# Efectos: Modifica la variable global elemento.
def elemento_seleccionado(numero):
    global elemento 
    elemento=numero
    return elemento

# Descripción: Renderiza y dibuja un texto en la ventana principal.
# Entradas: texto (contenido), fuente (fuente tipográfica), color (color del texto), x e y (coordenadas).
# Salidas: Ninguna.
# Efectos: Dibuja la superficie de texto en Ventana_principal.
def dibujar_texto(texto, fuente, color, x, y):
    img= fuente.render(texto, True, color)
    Ventana_principal.blit(img,(x,y))

#Descripción: Reinicia todos los valores de la matriz a 0
#Entradas:Ninguna
#Salidas: Ninguna
#Efectos: todos los valores de la matruz, pasan a ser 0 por lo que se limpia la matriz
def limpiar_matriz():
    matriz= matriz_guardada
    filas= len(matriz)
    columnas= len(matriz[0])
    for i in range(filas):
        for j in range(columnas):
            matriz[i][j]=0

# Descripción: Establece el pincel que se utilizará al pintar en la matriz.
# Entradas: pincel (objeto de la clase Pincel).
# Salidas: Ninguna.
# Efectos: Modifica la variable global pincel_actual.
def seleccionar_pincel(pincel):
    global pincel_actual
    pincel_actual = pincel

#Descripción:es una verificacion de que el boton derecho del mouse fue pulsado
#Entradas:no tiene
#Salidas:True, o False
#Efectos:Le dice al codigo si se esta preionando el click derecho o no    
def aplicar_pincel():
    if not pygame.mouse.get_pressed()[0]:
        return

    x, y = pygame.mouse.get_pos()
    filas= (x - centrar_x) // tamaño_cuadricula
    columnas= (y - centrar_y) // tamaño_cuadricula
    valores= len(matriz_guardada)#n

    if 0 <= columnas < valores and 0 <= filas< valores:
        pincel_actual.aplicar(columnas, filas, elemento)
        
# Descripción: Rellena un rectángulo de celdas con el elemento actual usando el click derecho (presionar, arrastrar y soltar).
# Entradas: eventos (lista de eventos de Pygame).
# Salidas: Ninguna.
# Efectos: Modifica rect_inicio y los valores de matriz_guardada dentro del rectángulo.
def seleccionar_rectangulo(eventos):
    global rect_inicio
    n = len(matriz_guardada)

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 3:
            rect_inicio = ((evento.pos[1] - centrar_y) // tamaño_cuadricula, (evento.pos[0] - centrar_x) // tamaño_cuadricula)

        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 3 and rect_inicio is not None:
            fila = (evento.pos[1] - centrar_y) // tamaño_cuadricula
            columna = (evento.pos[0] - centrar_x) // tamaño_cuadricula

            fila_inicial, fila_final = sorted((rect_inicio[0], fila))
            columna_inicial, columna_final = sorted((rect_inicio[1], columna))

            for f in range(max(0, fila_inicial), min(n - 1, fila_final) + 1):
                for c in range(max(0, columna_inicial), min(n - 1, columna_final) + 1):
                    matriz_guardada[f][c] = elemento
            rect_inicio = None

#Descripción:Establece a  una matriz como la matriz cargada
#entradas:la matriz utilizada
#salidas:no tiene
#efectos:la matriz guardada para a ser la variable matriz_guardada y las dimenciones las mismas            
def cargar_matriz_interfaz():
    global matriz_guardada, dimensiones

    matriz = cargar_matriz()

    if matriz is None:#esto corta la funcion si no se cargo una matriz
        return

    matriz_guardada = matriz
    dimensiones = str(len(matriz))
    caja_x.texto = dimensiones
    
#CLASES==========================================================================================================================
class Boton:

    # Descripción: Inicializa un botón con su texto, posición, disponibilidad y función asociada.
    # Entradas: texto, posicion_x, posicion_y, disponibilidad y funcion.
    # Salidas: Ninguna.
    # Efectos: Inicializa los atributos del objeto y crea el rectángulo que define el área del botón.
    def __init__(self, texto, posicion_x, posicion_y, disponibilidad,funcion):
        self.texto=texto
        self.posicion_x=posicion_x
        self.posicion_y=posicion_y
        self.disponibilidad=disponibilidad
        self.funcion=funcion
        self.forma=pygame.rect.Rect((self.posicion_x,self.posicion_y),(150,25))

    # Descripción: Dibuja el botón y cambia su apariencia según la posición del cursor y la interacción.
    # Entradas: eventos (lista de eventos de Pygame).
    # Salidas: Ninguna.
    # Efectos: Dibuja el rectángulo y el texto del botón en Ventana_principal; puede ejecutar la función asociada mediante presionado.
    def dibujar_boton(self,eventos):
        texto_boton= fuente_botones.render(self.texto, True, "black")
        
        if self.forma.collidepoint(pygame.mouse.get_pos()):
            texto_boton= fuente_botones.render(self.texto, True, "yellow")
        
        if self.presionado(eventos):
            pygame.draw.rect(Ventana_principal,"dark grey", self.forma, 0, 5)
            Sonido_pulsado_botones.play()
        else:
            pygame.draw.rect(Ventana_principal,"grey", self.forma, 0, 5)
            
        pygame.draw.rect(Ventana_principal,"black", self.forma, 2, 5)
        Ventana_principal.blit(texto_boton,(self.posicion_x+3,self.posicion_y+3))

    # Descripción: Determina si el usuario presionó el botón izquierdo del mouse sobre el botón.
    # Entradas: eventos (lista de eventos de Pygame).
    # Salidas: True si el botón fue presionado estando disponible; False en caso contrario.
    # Efectos: Puede ejecutar la función almacenada en self.funcion.
    def presionado(self,eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1 and self.forma.collidepoint(evento.pos) and self.disponibilidad:
                 self.funcion()
                 return True
        return False

class CajaTexto:

    # Descripción: Inicializa una caja de texto con su posición, contenido y estado visual.
    # Entradas: posicion_x y posicion_y (coordenadas de la caja).
    # Salidas: Ninguna.
    # Efectos: Inicializa los atributos del objeto y crea el rectángulo de la caja de texto.
    def __init__(self, posicion_x, posicion_y):
        self.posicion_x=posicion_x
        self.posicion_y=posicion_y
        self.texto=""
        self.escribiendo=False
        self.forma=pygame.Rect(posicion_x, posicion_y, 100, 45)
        self.color=GRIS
        self.color_fondo=BLANCO

    # Descripción: Gestiona la escritura del usuario y actualiza la apariencia de la caja de texto.
    # Entradas: eventos (lista de eventos de Pygame).
    # Salidas: Ninguna.
    # Efectos: Modifica el texto, el estado de escritura y el color de fondo; dibuja la caja de texto.
    def escribir(self,eventos):
        global texto_error
        for evento in eventos:
            if evento.type==pygame.MOUSEBUTTONDOWN:
                self.escribiendo=self.forma.collidepoint(evento.pos)
            if evento.type== pygame.KEYDOWN and self.escribiendo:
                if evento.key== pygame.K_BACKSPACE:
                    self.texto=self.texto[:-1]
                    self.color=BLANCO
                    texto_error=""
                elif evento.unicode.isdigit():
                    if len(self.texto)<=2:
                        self.color_fondo=BLANCO
                        self.texto+=evento.unicode
                        texto_error=""
                    else:
                        texto_error="solo se pueden ingresar 3 digitos"
                else:
                    self.color_fondo=ROJO 
                    texto_error="SOLO SE PUEDEN INGRESAR NUMEROS"
        self.dibujar_caja()

    # Descripción: Dibuja la caja de texto, su borde y el contenido actual.
    # Entradas: Ninguna.
    # Salidas: Ninguna.
    # Efectos: Dibuja elementos en Ventana_principal y actualiza la pantalla mediante pygame.display.flip().
    def dibujar_caja(self):
        if self.escribiendo:
            self.color=CELESTE
        pygame.draw.rect(Ventana_principal, self.color_fondo, self.forma)
        pygame.draw.rect(Ventana_principal,self.color,self.forma,2)
        superficie_texto = fuente_botones.render(self.texto, True, NEGRO)
        Ventana_principal.blit(superficie_texto,(self.forma.x+5, self.forma.y+8))
        pygame.display.flip()

class cuadriculas(pygame.sprite.Sprite):

    # Descripción: Inicializa una celda del sandbox como un sprite y prepara sus texturas.
    # Entradas: pos (posición), groups (grupo de sprites), fila y columna (índices de la matriz), tamaño (dimensión de la celda).
    # Salidas: Ninguna.
    # Efectos: Agrega el sprite al grupo indicado, escala las texturas y establece sus atributos.
    def __init__(self,pos, groups,fila,columna,tamaño):
        super().__init__(groups)

        self.textura = pygame.transform.scale(textura, (tamaño, tamaño))
        self.textura_arena=pygame.transform.scale(textura_arena, (tamaño, tamaño))
        self.textura_agua=pygame.transform.scale(textura_agua, ((tamaño,tamaño)))
        self.textua_piedra=pygame.transform.scale(textura_piedra,((tamaño,tamaño)))
        self.textua_tierra= pygame.transform.scale(textura_tierra,((tamaño,tamaño)))
        self.textura_fuego= pygame.transform.scale(textura_fuego,((tamaño,tamaño)))
        self.textura_semillas= pygame.transform.scale(textura_semillas,((tamaño,tamaño)))
        self.textura_pasto= pygame.transform.scale(textura_pasto,((tamaño,tamaño)))
        self.textura_planta1=pygame.transform.scale(textura_planta1,((tamaño,tamaño)))
        self.textura_planta2=pygame.transform.scale(textura_planta2,((tamaño,tamaño)))
        self.textura_planta3=pygame.transform.scale(textura_planta3,((tamaño,tamaño)))
        self.textura_animal=pygame.transform.scale(textura_animal,((tamaño,tamaño)))
        self.image=self.textura.copy()
        
        self.rect=self.image.get_frect(topleft=pos)
        self.fila=fila
        self.columna=columna


    # Descripción: Selecciona la textura que corresponde al valor almacenado en la matriz para esta celda.
    # Entradas: Ninguna; consulta matriz_guardada mediante los índices de la celda.
    # Salidas: Ninguna.
    # Efectos: Cambia self.image por una copia de la textura correspondiente.
    def actualizar_color(self):
        if matriz_guardada[self.fila][self.columna] == 1:
            self.image=self.textura_arena.copy()
        elif matriz_guardada[self.fila][self.columna]==2:
            self.image=self.textura_agua.copy()
        elif matriz_guardada[self.fila][self.columna]==3:
            self.image=self.textua_piedra.copy()
        elif matriz_guardada[self.fila][self.columna]==4:
            self.image=self.textua_tierra.copy()
        elif matriz_guardada[self.fila][self.columna]==5:
            self.image=self.textura_fuego.copy()
        elif matriz_guardada[self.fila][self.columna]==6:
            self.image=self.textura_semillas.copy()
        elif matriz_guardada[self.fila][self.columna]==7:
            self.image=self.textura_pasto.copy()
        elif matriz_guardada[self.fila][self.columna]==8:
            self.image=self.textura_planta1.copy()
        elif matriz_guardada[self.fila][self.columna]==9:
            self.image=self.textura_planta2.copy()
        elif matriz_guardada[self.fila][self.columna]==10:
            self.image=self.textura_planta3.copy()
        elif matriz_guardada[self.fila][self.columna]==11:
            self.image=self.textura_animal.copy()
        else:
            self.image=self.textura.copy()

    # Descripción: Ejecuta la actualización de interacción y apariencia de la celda.
    # Entradas: Ninguna.
    # Salidas: Ninguna.
    # Efectos: Llama a cuadricula_pulsada y actualizar_color.
    def update(self):
        self.actualizar_color()

class Pincel:

    # Descripción: Inicializa un pincel que abarca un cuadrado de celdas alrededor del cursor.
    # Entradas: nombre (texto del pincel) y radio (0 = 1 celda, 1 = 3x3, 2 = 5x5).
    # Salidas: Ninguna.
    # Efectos: Guarda los atributos y calcula los desplazamientos que cubre el pincel.
    def __init__(self, nombre, radio):
        self.nombre = nombre
        self.radio = radio
        self.desplazamientos = []
        for di in range(-radio, radio + 1):
            for dj in range(-radio, radio + 1):
                self.desplazamientos.append((di, dj))

    # Descripción: Escribe un elemento en todas las celdas que cubre el pincel.
    # Entradas: fila y columna (celda central), valor (elemento a escribir).
    # Salidas: Ninguna.
    # Efectos: Modifica varios valores de matriz_guardada, ignorando los que se salgan de la matriz.
    def aplicar(self, fila, columna, valor):
        n = len(matriz_guardada)
        for i in range(len(self.desplazamientos)):
            desplazamiento_fila = self.desplazamientos[i][0]
            desplazamiento_columnas = self.desplazamientos[i][1]
            filas = fila + desplazamiento_fila
            columnas = columna + desplazamiento_columnas
            if 0 <= filas < n and 0 <= columnas < n:
                matriz_guardada[filas][columnas] = valor
    
#OBJETOS========================================================================================

#objetos de tipo BOTON
boton_iniciar= Boton("INICIAR JUEGO",200,380,True, verificador)
boton_arena=Boton("ARENA",0,100,True,lambda:elemento_seleccionado(1))
boton_agua=Boton("AGUA",0,150,True,lambda:elemento_seleccionado(2))
boton_piedra= Boton("PIEDRA",0,200,True,lambda:elemento_seleccionado(3))
boton_tierra= Boton("TIERRA",0,250,True,lambda:elemento_seleccionado(4))
boton_fuego=Boton("FUEGO",0,300,True,lambda:elemento_seleccionado(5))
boton_semillas= Boton("SEMILLAS",0,350,True,lambda:elemento_seleccionado(6))
boton_pasto= Boton("PLANTAS",0,400,True,lambda:elemento_seleccionado(8))
boton_animal= Boton("ANIMALES",0, 450,True,lambda:elemento_seleccionado(11))
boton_borrar=Boton("BORRAR",0,500,True,lambda:elemento_seleccionado(0))
boton_reiniciar= Boton("REINICIAR",0,600,True,lambda:limpiar_matriz())
boton_cargar= Boton("CARGAR",380,380,True,cargar_matriz_interfaz)
boton_guardar= Boton("Guardar",1130,400,True,lambda:guardar_matriz(matriz_guardada))

boton_pincel1 = Boton("PINCEL 1", 1130, 100, True, lambda: seleccionar_pincel(pincel_1))
boton_pincel2 = Boton("PINCEL 2", 1130, 150, True, lambda: seleccionar_pincel(pincel_2))
boton_pincel3 = Boton("PINCEL 3", 1130, 200, True, lambda: seleccionar_pincel(pincel_3))

#Objetos de tipo Pincel
pincel_1 = Pincel("PINCEL 1", 0)   
pincel_2 = Pincel("PINCEL 2", 1)   
pincel_3 = Pincel("PINCEL 3", 2)   
pincel_actual = pincel_1

#objetos de tipo CajaTexto
caja_x= CajaTexto(320,300)
cambiar_musica("recursos\Audio\Audio pantalla de incio.mp3")

# BUCLE PRINCIPAL==================================================================================================================
run=True
while run: 
    Ventana_principal.fill(fondo_color)
    Ventana_principal.blit(fondo_menu,(0,0))    
    dibujar_texto("SANDOX",fuente_titulo, NEGRO,280,10)
    dibujar_texto(texto_error,fuente_botones,NEGRO,210,420)
    dibujar_texto("ESCRIBE LAS DIMENSIONES DEL MUNDO",fuente_botones,NEGRO,210,250)
    timer.tick(fps)
    eventos=pygame.event.get()
    
    for evento in eventos:
        if evento.type==pygame.QUIT:
            run=False   
    caja_x.escribir(eventos)
    boton_iniciar.dibujar_boton(eventos)
    boton_cargar.dibujar_boton(eventos)
    dimensiones=caja_x.texto
    pygame.display.flip()

pygame.quit()
