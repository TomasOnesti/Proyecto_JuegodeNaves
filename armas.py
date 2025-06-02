import pygame, constante

class Balas():
    def __init__(self, x, y):
        self.ancho = 10
        self.alto = 5
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        self.color = constante.color.RED  

    def mover(self):
        self.rect.x += 5  
