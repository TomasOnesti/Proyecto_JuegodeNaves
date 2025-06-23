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

#Bucle de pantalla de inicio
inicio =True
while inicio: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inicio = False
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                inicio = False
                running = True

    pantalla.blit(fondo,(0,0))
    #Texto de inicio del juego
    fuente_inicio = pygame.font.Font(None,60)
    texto_inicial= fuente_inicio.render("Iniciar Juego", True, colores.YELLOW)
    espacio = texto_inicial.get_rect(center=(constante.ANCHO/2, constante.ALTO/3))
    pantalla.blit(texto_inicial, espacio)
    #Texto instructivo
    text_ins= fuente.render("Presione espacio para iniciar",True, colores.YELLOW)
    pantalla.blit(text_ins, (constante.ANCHO/2 - text_ins.get_width()/2,constante.ALTO-450))

    text_op= fuente_inicio.render("Opciones", True, colores.YELLOW)
    espacio_op = (constante.ANCHO/2 - text_op.get_width()/2, constante.ALTO-380)
    pantalla.blit(text_op, espacio_op)

    text_ins_op= fuente.render("Presione E para entrar en las opciones", True, colores.YELLOW)
    pantalla.blit(text_ins_op, (constante.ANCHO/3 - text_op.get_width()/2, constante.ALTO-330)) 
    pygame.display.flip()    
    reloj.tick(constante.FPS)
    
#Bucle donde se ejecuta el juego

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
            gameover = True
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
nombre = input(" escribe tu nombre ")
db.insertar(nombre, puntos)
print("Tu puntuacion final es de: ", puntos)


#Pantalla de gameover
while gameover:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                gameover = False
    
    
    
    pantalla.blit(fondo,(0,0))#Fondo estatico en la pantalla del fin del juego
    
    #Letra y posicion del texto de gameover
    fuente_fin = pygame.font.Font(None, 60)
    texto_fin = fuente_fin.render("GameOver", True, colores.RED)
    espacio_fin = texto_fin.get_rect(center=(constante.ANCHO/2, constante.ALTO/3))
    pantalla.blit(texto_fin,espacio_fin)
    #Letra y posicion del texto de puntuación
    puntuacion_final = fuente.render(f"Tu puntuacion final es de: {puntos}", True, colores.WHITE )
    pantalla.blit(puntuacion_final, (constante.ANCHO/2 - puntuacion_final.get_width()/2,constante.ALTO/2))
    #Letra y posición del texto instructivo para salir
    instruccion = fuente.render("Presionar enter para salir", True, colores.WHITE)
    espacio_ins = instruccion.get_rect(center =(constante.ANCHO/2, constante.ALTO - 200))
    pantalla.blit(instruccion, espacio_ins)
    pygame.display.flip()    
    reloj.tick(constante.FPS)
    
pygame.quit()