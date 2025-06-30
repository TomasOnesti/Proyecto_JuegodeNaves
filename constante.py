import pygame
ANCHO = 1000#Ancho de la pantalla
ALTO = 700#Alto de la pantalla
FPS = 300#Cantidad de Frame por Segundo 
tamaño =(ANCHO, ALTO) #Tamaño de la pantalla
efecto=0.4
musica =0.7

def fuente_escalada(porcentaje=0.05):
    # Usa un porcentaje de la altura de pantalla para determinar el tamaño
    tamaño = int(ALTO * porcentaje)
    return pygame.font.Font(None, tamaño)

#Clase con colores para usar
class color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW=(255,255,0)