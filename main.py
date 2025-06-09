import pygame, database
import constante, personajes
from armas import *
pygame.init()

#Variables importantes
reloj = pygame.time.Clock()#FPS
fuente= pygame.font.Font(None, 40)#Letra
colores = constante.color()#colores
pantalla = pygame.display.set_mode(constante.tamaño)#tamaño de pantalla
fondo = pygame.image.load("img/espacio3.png").convert()#Fondo
jugador = personajes.jugador()#Jugador(Variable que almacena la clase jugador)
meteorito = personajes.meteoritos()#Meteoritos
db= database.ranking()
x=0#coordenada del fondo
puntos=0 #Puntuacion inicial en 0

#Bucle donde se ejecuta el juego
running = True
while running:
    pantalla.fill(constante.color().BLACK)
    #cerrar el juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        #Definiendo boton de disparo
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
    for met in meteorito.meteoritosl:
        if jugador.nave.colliderect(met["rect"]):
            running = False
    #Muestra los meteoritos por pantalla
    for met in meteorito.meteoritosl:
        pantalla.blit(met["img"], met["rect"])
    #Mover y mostrar las balas del jugador
    for bala in jugador.balas[:]:
        bala.mover()
        pygame.draw.rect(pantalla, bala.color, bala.rect)
        if bala.rect.left > constante.ANCHO:
            jugador.balas.remove(bala)
    #Coliciones meteoritos con balas
    for bala in jugador.balas[:]:
        for met in meteorito.meteoritosl[:]:
            if bala.rect.colliderect(met["rect"]):
                jugador.balas.remove(bala)
                meteorito.meteoritosl.remove(met)
                if met["tipo"] == "divisible":
                    nuevos_meteoritos = meteorito.dividir_meteoritos(met)
                    meteorito.meteoritosl.extend(nuevos_meteoritos)
                    if met["size_key"] == "grande":
                        puntos +=3
                    elif met["size_key"]=="chico":
                        puntos +=1
                puntos += 2
                break
    #Pequeña muestra de puntaje en la esquina superior izquierda de la pantalla
    score = fuente.render(str(puntos), True, colores.WHITE) 
    pantalla.blit(score, (0, 0))
    pantalla.blit(jugador.imgnave, jugador.nave)#Muestra al jugador por pantalla

    pygame.display.flip()    
    reloj.tick(constante.FPS)
#Base de datos: insercion de datos(pedir nombre)
nombre = input("escribe tu nombre")
db.insertar(nombre, puntos)
print("Tu puntuacion final es de: ", puntos)
