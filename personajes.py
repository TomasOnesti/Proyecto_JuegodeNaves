import pygame, random, constante
pygame.init()
#Clase del jugador
class jugador():
    def __init__(self):
        self.ancho = 80
        self.alto = 80
        self.size=(self.ancho, self.alto)#Tamaño jugador
        self.imgnave = pygame.image.load("img/nave1_.png").convert_alpha()#Imagen de la nave(Jugador)
        self.imgnave = pygame.transform.scale(self.imgnave, self.size)#Escala la imagen a un tamaño especifico
        self.nave = pygame.Rect(80 - self.ancho -10, 
            constante.ALTO // 2 - self.alto // 2, self.ancho, self.alto)#Hitbox de la nave
        #Funcion de movimiento
    def movimiento(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.nave.left > 0:
            self.nave.x -=5
        if keys[pygame.K_RIGHT] and self.nave.right < constante.ANCHO:
            self.nave.x +=5
        if keys[pygame.K_DOWN] and self.nave.bottom < constante.ALTO:
            self.nave.y +=5
        if keys[pygame.K_UP] and self.nave.top > 0:
            self.nave.y -=5
            
#Clase de los meteoritos
class meteoritos():
    def __init__(self):
        self.imgmeteorito = pygame.image.load("img/meteorito1.png").convert_alpha()#Imagen de los meteoritos
        self.ancho = 50
        self.alto = 50
        self.size=(self.ancho, self.alto)#Tamaño de los meteoritos
        self.imgmeteorito = pygame.transform.scale(self.imgmeteorito, self.size)#Escala la imagen a un tamaño especifico
        self.meteoritosl =[]#Lista para almacenar los meteoritos
        #Funciones del meteorito
    def funcionesmeteorito(self):
        #Generacion
        if len (self.meteoritosl) < 7:
            self.meteorito = pygame.Rect( 950, random.randint(0,constante.ALTO - self.alto), self.ancho, self.alto)
            self.meteoritosl.append(self.meteorito)
        #Movimiento
        for self.meteorito in self.meteoritosl:
         self.meteorito.x -= 2
        if self.meteorito.right > constante.ANCHO:
            self.meteoritosl.remove(self.meteorito) 
    
    