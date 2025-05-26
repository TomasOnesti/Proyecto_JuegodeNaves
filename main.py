import pygame, sys
import constante, personajes
pygame.init()

reloj = pygame.time.Clock()#FPS
colores = constante.color()#colores
pantalla = pygame.display.set_mode(constante.tamaño)#tamaño de pantalla
fondo = pygame.image.load("img/espacio3.png").convert()#Fondo
jugador = personajes.jugador()#Jugador
 
x=0#coordenada del fondo
#Variables Velocidad de movimiento
velx = 0
vely = 0

#Bucle donde se ejecuta el juego
while True:
    #cerrar el juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #Evento del teclado para mov. jugador
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
    jugador.movimiento(velx, vely)
    
    #Fondo y mov. del Fondo
    xrelativa = x % fondo.get_rect().width
    pantalla.blit(fondo,[xrelativa - fondo.get_rect().width , 0])#cambio fondo a una imagen
    if(xrelativa < constante.ANCHO):
        pantalla.blit(fondo,[xrelativa, 0])
    x -= 1        
    
    pantalla.blit(jugador.sprite,[jugador.cordx,jugador.cordy])#Muestro al jugador
    
    pygame.display.flip()    
    reloj.tick(constante.FPS)