import pygame, random, constante
from armas import *
pygame.init()
#Clase del jugador
class jugador():
    def __init__(self):
        self.ancho = 70
        self.alto = 70
        self.size=(self.ancho, self.alto)#Tamaño jugador
        self.imgnave = pygame.image.load("img/nave1_.png").convert_alpha()#Imagen de la nave(Jugador)
        self.imgnave = pygame.transform.scale(self.imgnave, self.size)#Escala la imagen a un tamaño especifico
        self.nave = pygame.Rect(80 - self.ancho -10, 
            constante.ALTO // 2 - self.alto // 2, self.ancho, self.alto)#Hitbox de la nave
        self.balas = []
        #Funcion de movimiento
    def movimiento(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.nave.left > 0:
            self.nave.x -=4
        if keys[pygame.K_RIGHT] and self.nave.right < constante.ANCHO:
            self.nave.x +=4
        if keys[pygame.K_DOWN] and self.nave.bottom < constante.ALTO:
            self.nave.y +=4
        if keys[pygame.K_UP] and self.nave.top > 0:
            self.nave.y -=4
            
    def disparar(self):
        # Coordenadas de los cañones
        offset_y = 34  # Separación vertical del centro
        izquierda_x = self.nave.left + 34
        derecha_x = self.nave.right - 34
        centro_y = self.nave.centery

        # Crear dos balas desde los laterales de la nave
        bala_izquierda = Balas(izquierda_x, centro_y - offset_y)
        bala_derecha = Balas(derecha_x, centro_y + offset_y)

        self.balas.append(bala_izquierda)
        self.balas.append(bala_derecha)
            
#Clase de los meteoritos
class meteoritos():
    def __init__(self):
        self.imgmeteorito = pygame.image.load("img/meteorito1.png").convert_alpha()#Imagen de los meteoritos
        self.imgmeteorito2= pygame.image.load("img/meteorito_2.png").convert_alpha()
        self.meteoros={
            "meteorobase":(60,60),
            "tamanios": {
                "grande":(100,100),
                "mediano": (60,60),
                "chico":(40,40)
            },
            "velocidades":{
                "lento": 0.5,
                "medio": 2,
                "rapido":3.5
            }
        }
        self.size_met1=(self.meteoros["meteorobase"][0], self.meteoros["meteorobase"][1])#Tamaño de los meteoritos
        self.imgmeteorito = pygame.transform.scale(self.imgmeteorito, self.size_met1)#Escala la imagen a un tamaño especifico
        self.meteoritosl =[]#Lista para almacenar los meteoritos
        #Funciones del meteorito
        
    def generar_meteorito1(self):
        #Generacion Meteoritos normales
        tamaño = self.meteoros["meteorobase"]
        velocidad = self.meteoros["velocidades"]["medio"]
        rect = pygame.Rect(950, random.randint(0, constante.ALTO - tamaño[1]), tamaño[0], tamaño[1])
        img = pygame.transform.scale(self.imgmeteorito, tamaño)
        meteor = {"rect": rect, "tipo": "normal", "velocidad": velocidad, "img": img}
        self.meteoritosl.append(meteor)
        
    def generar_meteoritos2(self):
        #generar meteoritos divisibles
        tamaño = self.meteoros["tamanios"]["grande"]
        velocidad = self.meteoros["velocidades"]["medio"]
        rect = pygame.Rect(950, random.randint(0, constante.ALTO - tamaño[1]), tamaño[0], tamaño[1])
        img = pygame.transform.scale(self.imgmeteorito2, tamaño)
        meteor = {"rect": rect, "tipo": "divisible", "size_key": "grande", "velocidad": velocidad, "img": img}
        self.meteoritosl.append(meteor)
    def funcionesmeteorito(self):
    # Generación de meteoritos
        if len(self.meteoritosl) < 7:
            if random.random() < 0.5:
                self.generar_meteorito1()
            else:
                self.generar_meteoritos2()

        # Movimiento y eliminación de meteoritos fuera de pantalla
        for meteorito in self.meteoritosl[:]:
            meteorito["rect"].x -= meteorito["velocidad"]
            if meteorito["rect"].right <= 0:
                self.meteoritosl.remove(meteorito)
                
    def dividir_meteoritos(self, meteorito):
        if meteorito["tipo"] != "divisible":
            return[]
        
        if meteorito["size_key"] == "grande":
            nuevo_tamaño_key = "mediano"
        elif meteorito["size_key"] == "mediano":
            nuevo_tamaño_key = "chico"
        else:
            return []  # "chico" no se divide
        
        nuevo_tamaño = self.meteoros["tamanios"][nuevo_tamaño_key]
        velocidad = meteorito["velocidad"]
        meteoritos_nuevos = []

        separacion = [
        (0, 0),
        (int(nuevo_tamaño[0] * 0.9), int(nuevo_tamaño[1] * 0.9))
        ]
        for off in separacion:
            x = meteorito["rect"].x + off[0]
            y = meteorito["rect"].y + off[1]
            rect = pygame.Rect(x, y, nuevo_tamaño[0], nuevo_tamaño[1])
            img = pygame.transform.scale(self.imgmeteorito2, nuevo_tamaño)
            nuevo_meteorito = {
                "rect": rect, 
                "tipo": "divisible", 
                "size_key": nuevo_tamaño_key, 
                "velocidad": velocidad, 
                "img": img
            }
            meteoritos_nuevos.append(nuevo_meteorito)
        return meteoritos_nuevos