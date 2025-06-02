import pygame
import constante, personajes
from armas import *
pygame.init()

reloj = pygame.time.Clock()#FPS
colores = constante.color()#colores
pantalla = pygame.display.set_mode(constante.tamaño)#tamaño de pantalla
fondo = pygame.image.load("img/espacio3.png").convert()#Fondo
jugador = personajes.jugador()#Jugador(Variable que almacena la clase jugador)
meteorito = personajes.meteoritos()#Meteoritos
x=0#coordenada del fondo

#Bucle donde se ejecuta el juego
running = True
while running:
    pantalla.fill(constante.colorbg)
    #cerrar el juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                jugador.disparar()
                
    jugador.movimiento()#Funcion de movimiento del jugador
    
    #Fondo y mov. del Fondo
    xrelativa = x % fondo.get_rect().width
    pantalla.blit(fondo,[xrelativa - fondo.get_rect().width , 0])#cambio fondo a una imagen
    if(xrelativa < constante.ANCHO):
        pantalla.blit(fondo,[xrelativa, 0])
    x -= 1        
    meteorito.funcionesmeteorito() #Movimiento y generacion de los meteoritos
    
    #Colicion con los meteoritos
    for meteorito.meteorito in meteorito.meteoritosl:
        if jugador.nave.colliderect(meteorito.meteorito):
            running = False
    #Muestra los meteoritos por pantalla
    for meteorito.meteorito in meteorito.meteoritosl:
        pantalla.blit(meteorito.imgmeteorito, meteorito.meteorito)
    
    for bala in jugador.balas[:]:
        bala.mover()
        pygame.draw.rect(pantalla, bala.color, bala.rect)
        
        if bala.rect.left > constante.ANCHO:
            jugador.balas.remove(bala)
            
    for bala in jugador.balas[:]:
        for meteor in meteorito.meteoritosl[:]:
            if bala.rect.colliderect(meteor):
                jugador.balas.remove(bala)
                meteorito.meteoritosl.remove(meteor)
                break
    
    pantalla.blit(jugador.imgnave, jugador.nave)#Muestra al jugador por pantañña
    
    pygame.display.flip()    
    reloj.tick(constante.FPS)