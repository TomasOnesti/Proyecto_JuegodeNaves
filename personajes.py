import pygame
pygame.init()

class jugador():
    def __init__(self):
        self.sprite = pygame.image.load("img/nave1.png")
        self.cordx = 50
        self.cordy = 20
        self.rect = self.sprite.get_rect()
        
    def movimiento(self, velx, vely):
        self.cordx += velx#mov. lateral
        self.cordy += vely#mov. horizontal
        
    