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
        self.ancho = 60
        self.alto = 60
        self.size=(self.ancho, self.alto)#Tamaño de los meteoritos
        self.imgmeteorito = pygame.transform.scale(self.imgmeteorito, self.size)#Escala la imagen a un tamaño especifico
        self.meteoritosl =[]#Lista para almacenar los meteoritos
        #Funciones del meteorito
    def funcionesmeteorito(self):
    # Generación de meteoritos
        if len(self.meteoritosl) < 12:
            nuevo_meteorito = pygame.Rect(950, random.randint(0, constante.ALTO - self.alto), self.ancho, self.alto)
            self.meteoritosl.append(nuevo_meteorito)

        # Movimiento y eliminación de meteoritos fuera de pantalla
        for meteorito in self.meteoritosl[:]:  
            meteorito.x -= 2
            if meteorito.right <= 0:
                self.meteoritosl.remove(meteorito)
            

    