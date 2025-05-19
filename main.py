import pygame, sys
import constante
pygame.init()

reloj = pygame.time.Clock()
colores = constante.color()#colores
pantalla = pygame.display.set_mode(constante.tamaño)#tamaño de pantalla
fondo = pygame.image.load("img/espacio.png").convert()

#coordenadas del circulo y variables de velocidad 
x=0
cordx = 50
cordy = 20
velx = 0
vely = 0
#Bucle donde se ejecuta el juego
while True:
    #cerrar el juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                velx = -3
            if event.key == pygame.K_RIGHT:
                velx = 3
            if event.key == pygame.K_UP:
                vely = -3
            if event.key == pygame.K_DOWN:
                vely = 3
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                velx = 0
            if event.key == pygame.K_RIGHT:
                velx = 0
            if event.key == pygame.K_UP:
                vely = 0
            if event.key == pygame.K_DOWN:
                vely = 0
            
    xrelativa = x % fondo.get_rect().width
    pantalla.blit(fondo,[xrelativa - fondo.get_rect().width , 0])#cambio fondo a una imagen
    if(xrelativa < 1000):
        pantalla.blit(fondo,[xrelativa, 0])
    
    
    x -= 1        
    cordx += velx
    cordy += vely
    pygame.draw.circle(pantalla, colores.RED, (cordx,cordy), 20)#dibijo un circulo
    
    pygame.display.flip()    
    reloj.tick(constante.FPS)