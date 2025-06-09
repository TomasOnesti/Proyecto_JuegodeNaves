import pygame, constante

class Balas():
    def __init__(self, x, y):
        self.ancho = 10 #ancho de bala
        self.alto = 5#alto de bala
        self.rect = pygame.Rect(x, y, self.ancho, self.alto) #definiendo una bala
        self.color = constante.color.RED #color de bala 

    def mover(self):
        self.rect.x += 5 #velocidad
