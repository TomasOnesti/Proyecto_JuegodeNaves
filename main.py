import pygame, database
import constante, personajes
from armas import *

pygame.init()



while True:
    #Variables importantes#
    reloj = pygame.time.Clock()#FPS
    fuente = constante.fuente_escalada(0.045)#Letra
    
    #Sonidos#
    pygame.mixer.music.load(constante.resource_path("elementos/audios/musica/musicadejuego.mp3"))
    gameover_sound= pygame.mixer.Sound(constante.resource_path("elementos/audios/efectos/juego_terminado.mp3"))
    muerte = pygame.mixer.Sound(constante.resource_path("elementos/audios/efectos/muerte.mp3"))
    muerte.set_volume(constante.efecto)
    disparo1_sound= pygame.mixer.Sound(constante.resource_path("elementos/audios/efectos/disparoefecto1.mp3"))
    disparo1_sound.set_volume(constante.efecto)
    disparo2_sound = pygame.mixer.Sound(constante.resource_path("elementos/audios/efectos/disparoefecto2.mp3"))
    disparo2_sound.set_volume(constante.efecto)
    disparo3_sound = pygame.mixer.Sound(constante.resource_path("elementos/audios/efectos/disparoefecto3.mp3"))
    disparo3_sound.set_volume(constante.efecto)
    disparo_enemigo= pygame.mixer.Sound(constante.resource_path("elementos/audios/efectos/disparoenemigo.mp3"))
    disparo_enemigo.set_volume(constante.efecto)
    gameover_sound.set_volume(constante.musica)
    pygame.mixer.music.set_volume(constante.musica)

    colores = constante.color()
    pantalla = pygame.display.set_mode(constante.tamaño)
    fondo = pygame.image.load(constante.resource_path("elementos/assets/background/espacio3.png")).convert()
    #Personajes#
    jugador = personajes.jugador()
    meteorito = personajes.meteoritos()
    jefe = personajes.jefe()
    jefe_activo = False
    tiempo_muerte_jefe = None
    
    db= database.Ranking()
    enemigos = personajes.enemigo()
    dificultades = ["Fácil", "Normal", "Difícil"]
    niveles_generacion = [2, 4, 6]  
    indice_dificultad = 1  
    #Control de bucles
    running = False
    gameover = False
    inicio = True

    arma2_disparadores = set()
    activar_arma = [300, 500] + [800 * i for i in range(1, 100)]
    arma3_disparador= set()
    activar_arma3=[600, 1100] + [1400 * i for i in range(1,100)]

    tamaños_pantalla = [(800, 600), (1000, 700), (1200, 800)]
    indice_tamaño = 1  # Por defecto tamaño medio
    nivel_mute = 0

    balas_a_remover = []
    meteoritos_a_remover = []
    enemigos_a_remover = []
    balas_enemigas_a_remover = []

    x=0#coordenada del fondo
    puntos=0 #Puntuacion inicial en 0

    #Bucle de pantalla de inicio
    while inicio: 
        pantalla.blit(fondo,(0,0))

        fuente_inicio = constante.fuente_escalada(0.08)
        texto_inicial= fuente_inicio.render("Iniciar Juego", True, colores.YELLOW)
        espacio = texto_inicial.get_rect(center=(constante.ANCHO/2, constante.ALTO * 0.25))
        pantalla.blit(texto_inicial, espacio)

        text_ins= fuente.render("Presione espacio para iniciar",True, colores.YELLOW)
        pantalla.blit(text_ins, (constante.ANCHO/2 - text_ins.get_width()/2, constante.ALTO * 0.35))

        # Botones de opciones
        ancho_boton = constante.ANCHO * 0.25
        alto_boton = constante.ALTO * 0.06
        x_boton = (constante.ANCHO - ancho_boton) / 2
        
        boton_mute = pygame.Rect(x_boton, constante.ALTO * 0.45, ancho_boton, alto_boton)
        boton_dificultad = pygame.Rect(x_boton, constante.ALTO * 0.55, ancho_boton, alto_boton)
        boton_tamaño = pygame.Rect(x_boton, constante.ALTO * 0.65, ancho_boton, alto_boton)
        boton_ranking = pygame.Rect(constante.ANCHO/2 - 100, constante.ALTO/2 + 200, 200, 40)
        pygame.draw.rect(pantalla, colores.WHITE, boton_mute, border_radius=8)
        pygame.draw.rect(pantalla, colores.WHITE, boton_dificultad, border_radius=8)
        pygame.draw.rect(pantalla, colores.WHITE, boton_tamaño, border_radius=8)
        pygame.draw.rect(pantalla, colores.WHITE, boton_ranking, border_radius=8)
        
        estados_mute = ["No", "Música", "Todo"]
        mute_text = fuente.render(f"Mute: {estados_mute[nivel_mute]}", True, colores.BLACK)
        dificultad_text = fuente.render(f"Dificultad: {dificultades[indice_dificultad]}", True, colores.BLACK)
        tamaño_text = fuente.render(f"Pantalla: {tamaños_pantalla[indice_tamaño][0]}x{tamaños_pantalla[indice_tamaño][1]}", True, colores.BLACK)
        ranking_text = fuente.render("Ver Ranking", True, colores.BLACK)
        
        pantalla.blit(mute_text, (boton_mute.x + 10, boton_mute.y + 5))
        pantalla.blit(dificultad_text, (boton_dificultad.x + 10, boton_dificultad.y + 5))
        pantalla.blit(tamaño_text, (boton_tamaño.x + 10, boton_tamaño.y + 5))
        pantalla.blit(ranking_text, (boton_ranking.x + 40, boton_ranking.y + 5))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    inicio = False
                    running = True
                    pygame.mixer.music.play(-1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_mute.collidepoint(event.pos):
                    nivel_mute = (nivel_mute + 1) % 3  # rota entre 0,1,2

                    if nivel_mute == 0:
                        pygame.mixer.music.set_volume(constante.musica)
                        gameover_sound.set_volume(constante.musica)
                        disparo1_sound.set_volume(constante.efecto)
                        disparo2_sound.set_volume(constante.efecto)
                        disparo3_sound.set_volume(constante.efecto)
                        disparo_enemigo.set_volume(constante.efecto)
                        muerte.set_volume(constante.efecto)
                    elif nivel_mute == 1:
                        pygame.mixer.music.set_volume(0)  # solo música
                        gameover_sound.set_volume(constante.musica)
                        disparo1_sound.set_volume(constante.efecto)
                        disparo2_sound.set_volume(constante.efecto)
                        disparo3_sound.set_volume(constante.efecto)
                        disparo_enemigo.set_volume(constante.efecto)
                        muerte.set_volume(constante.efecto)
                    elif nivel_mute == 2:
                        pygame.mixer.music.set_volume(0)
                        gameover_sound.set_volume(0)
                        disparo1_sound.set_volume(0)
                        disparo2_sound.set_volume(0)
                        disparo3_sound.set_volume(0)
                        disparo_enemigo.set_volume(0)
                        muerte.set_volume(0)
                if boton_dificultad.collidepoint(event.pos):
                    indice_dificultad = (indice_dificultad + 1) % len(dificultades)
                if boton_tamaño.collidepoint(event.pos):
                    indice_tamaño = (indice_tamaño + 1) % len(tamaños_pantalla)
                    constante.ANCHO, constante.ALTO = tamaños_pantalla[indice_tamaño]
                    constante.tamaño = tamaños_pantalla[indice_tamaño]
                    pantalla = pygame.display.set_mode(constante.tamaño)
                    fuente = constante.fuente_escalada(0.045)
                if boton_ranking.collidepoint(event.pos):
                    constante.mostrar_ranking(pantalla, colores, fuente, fondo, db)
        pygame.display.flip()
        reloj.tick(constante.FPS)
        
    #Bucle donde se ejecuta el juego
    while running:
        pantalla.fill(constante.color().BLACK)
        #cerrar el juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            #Definiendo boton de disparo
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if jugador.arma == 1:
                        if jugador.max_balas > 0:
                            disparo1_sound.play()
                        else:
                            disparo1_sound.stop()
                    elif jugador.arma == 2:
                        disparo2_sound.play()
                    else:
                        disparo3_sound.play()
                    jugador.disparar()
                    
        jugador.movimiento()#Funcion de movimiento del jugador
        jugador.actualizar_estado()
        #Fondo y mov. del Fondo
        xrelativa = x % fondo.get_rect().width
        pantalla.blit(fondo,[xrelativa - fondo.get_rect().width , 0])#cambio fondo a una imagen
        if(xrelativa < constante.ANCHO):
            pantalla.blit(fondo,[xrelativa, 0])
        x -= 1        
        meteorito.funcionesmeteorito(niveles_generacion, indice_dificultad) #Movimiento y generacion de los meteoritos
        
        #Colicion con los meteoritos
        for met in meteorito.meteoritosl:
            if not jugador.inmortal and jugador.nave.colliderect(met["rect"]):
                gameover_sound.play()
                running = False
                gameover = True
        #Muestra los meteoritos por pantalla
        for met in meteorito.meteoritosl:
            pantalla.blit(met["img"], met["rect"])
            pygame.draw.rect(pantalla, colores.RED, met["rect"], 2)#Muestra hitbox
        #Mover y mostrar las balas del jugador
        for bala in jugador.balas[:]:
            bala.mover()
            pygame.draw.rect(pantalla, bala.color, bala.rect)
            if bala.rect.left > constante.ANCHO:
                jugador.balas.remove(bala)
        #Coliciones meteoritos con balas
        for bala in jugador.balas:
            for met in meteorito.meteoritosl:
                if bala.rect.colliderect(met["rect"]):
                    if bala not in balas_a_remover:
                        balas_a_remover.append(bala)
                    if met not in meteoritos_a_remover:
                        meteoritos_a_remover.append(met)
                    
                    
                    if met["tipo"] == "divisible":
                        nuevos_meteoritos = meteorito.dividir_meteoritos(met)
                        meteorito.meteoritosl.extend(nuevos_meteoritos)
                        if met["size_key"] == "grande":
                            puntos += 5
                        elif met["size_key"] == "chico":
                            puntos += 2
                    puntos += 3
                    
                    for activar in activar_arma:
                        if puntos >= activar and activar not in arma2_disparadores:
                            if jugador.arma != 2 and not jugador.en_animacion and jugador.arma2_balas > 0:
                                jugador.iniciar_cambio_arma(2)
                                arma2_disparadores.add(activar)
                            
                            if jugador.arma == 2 and jugador.arma2_balas > 0:
                                jugador.arma2_balas = 250
                            break
                    
                    for activar in activar_arma3:
                        if puntos >= activar and activar not in arma3_disparador:
                            if  jugador.en_animacion and jugador.arma3_balas > 0:
                                jugador.iniciar_cambio_arma(3)
                                arma3_disparador.add(activar)
                                
                            if jugador.arma == 3 and jugador.arma3_balas > 0:
                                jugador.arma3_balas = 60
                            break
        for bala in balas_a_remover:
            if bala in jugador.balas:
                jugador.balas.remove(bala)
        for met in meteoritos_a_remover:
            if met in meteorito.meteoritosl:
                muerte.play()
                meteorito.meteoritosl.remove(met)    
            
        if puntos >= 2000 and not jefe_activo and indice_dificultad != 0:
            jefe_activo = True
            if indice_dificultad == 2:  # Difícil
                jefe.vida = 4000
            meteorito.meteoritosl.clear()
        if jefe_activo and jefe:
            jefe.mover()
            disparo2_sound.play()
            jefe.disparar()

            for bala in jugador.balas[:]:
                if bala.rect.colliderect(jefe.rect):
                    jefe.vida -= 10
                    jugador.balas.remove(bala)

            if jefe.vida <= 0:
                puntos += 1000
                jefe_activo = False
                jefe = None
                tiempo_muerte_jefe = pygame.time.get_ticks()
                meteorito.meteoritosl.clear()
            else:
                for bala in jefe.lista_balas:
                    pygame.draw.rect(pantalla, bala.color, bala.rect)
                    bala.mover()
                    if not jugador.inmortal and bala.rect.colliderect(jugador.nave):
                        gameover_sound.play()
                        running = False
                        gameover = True
                jefe.render(pantalla)
    #Enemigos    
        enemigos.mover_y_disparar()
        
        for ene in enemigos.lista_enemigos:
            pantalla.blit(enemigos.img_enemigo, ene["rect"])
            pygame.draw.rect(pantalla, colores.RED, ene["rect"], 2)  # hitbox opcional

        for bala in enemigos.lista_balas_enemigas:
            pygame.draw.rect(pantalla, bala.color, bala.rect)
        
        for bala in enemigos.lista_balas_enemigas[:]:
            if not jugador.inmortal and bala.rect.colliderect(jugador.nave):
                gameover_sound.play()
                running = False
                gameover = True
                
        for bala in jugador.balas:
            for ene in enemigos.lista_enemigos:
                if bala.rect.colliderect(ene["rect"]):
                    if bala not in balas_a_remover:
                        balas_a_remover.append(bala)
                    if ene not in enemigos_a_remover:
                        enemigos_a_remover.append(ene)
                    puntos +=4
    
        for ene in enemigos_a_remover:
            if ene in enemigos.lista_enemigos:
                muerte.play()
                enemigos.lista_enemigos.remove(ene)
        
        if len(enemigos.lista_enemigos) == 0:
            enemigos.lista_balas_enemigas.clear()
            enemigos.crear_enemigos(niveles_generacion, indice_dificultad)
        
        if len(enemigos.lista_enemigos) == 0:
            enemigos.crear_enemigos(niveles_generacion, indice_dificultad)
        #Putaje
        score = fuente.render(str(puntos), True, colores.WHITE) 
        pantalla.blit(score, (constante.ANCHO * 0.01, constante.ALTO * 0.01))
        jugador.render(pantalla)#Muestra al jugador por pantalla
        pygame.draw.rect(pantalla, colores.GREEN, jugador.nave, 2)
        if jugador.arma == 1:
            municion = fuente.render(f"Munición: {jugador.balas_restantes}", True, colores.WHITE)
        elif jugador.arma == 2:
            municion = fuente.render(f"Ametralladora: {jugador.arma2_balas}/250", True, colores.WHITE)
        else:
            municion = fuente.render(f"Escopeta: {jugador.arma3_balas}/60", True, colores.WHITE)
        pantalla.blit(municion, (constante.ANCHO * 0.01, constante.ALTO * 0.06))
        pygame.display.flip()    
        reloj.tick(constante.FPS)

    if not running and gameover:
        pygame.mixer.music.stop()
    
    def pedir_nombre(pantalla, colores, fuente):
        texto = ""
        escribiendo = True
        while escribiendo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        escribiendo = False
                    elif event.key == pygame.K_BACKSPACE:
                        texto = texto[:-1]
                    else:
                        if len(texto) < 12:
                            texto += event.unicode

            pantalla.blit(fondo,(0,0))

            fuente_nombre = constante.fuente_escalada(0.055)
            mensaje = fuente_nombre.render("Escribe tu nombre y presiona ENTER:", True, colores.WHITE)
            input_texto = fuente_nombre.render(texto, True, colores.YELLOW)
            rect_mensaje = mensaje.get_rect(center=(constante.ANCHO/2, constante.ALTO * 0.3))
            rect_input = input_texto.get_rect(center=(constante.ANCHO/2, constante.ALTO * 0.5))

            pantalla.blit(mensaje, rect_mensaje)
            pantalla.blit(input_texto, rect_input)

            pygame.display.flip()
            pygame.time.Clock().tick(30)

        return texto
        
    #Base de datos: insercion de datos(pedir nombre)
    if gameover:
        nombre = pedir_nombre(pantalla,colores,fuente)
        db.insertar(nombre, puntos)


    #Pantalla de gameover
    while gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_r:
                    gameover = False
        
        
        pantalla.blit(fondo,(0,0))#Fondo estatico en la pantalla del fin del juego
        
        #Letra y posicion del texto de gameover
        fuente_fin = constante.fuente_escalada(0.08)
        texto_fin = fuente_fin.render("GameOver", True, colores.RED)
        espacio_fin = texto_fin.get_rect(center=(constante.ANCHO/2, constante.ALTO * 0.3))
        pantalla.blit(texto_fin,espacio_fin)
        #Letra y posicion del texto de puntuación
        fuente_puntaje = constante.fuente_escalada(0.05)
        puntuacion_final = fuente_puntaje.render(f"Tu puntuacion final es de: {puntos}", True, colores.WHITE)
        pantalla.blit(puntuacion_final, puntuacion_final.get_rect(center=(constante.ANCHO/2, constante.ALTO * 0.5)))
        nombre_texto = fuente_puntaje.render(f"Nombre: {nombre}", True, colores.WHITE)
        pantalla.blit(nombre_texto, nombre_texto.get_rect(center=(constante.ANCHO/2, constante.ALTO * 0.55)))
        #Letra y posición del texto instructivo para salir
        instruccion = fuente_puntaje.render("Presionar enter para salir", True, colores.WHITE)
        instruccion2 = fuente_puntaje.render("Presionar R para ir al inicio", True, colores.WHITE)
        espacio_ins = instruccion.get_rect(center=(constante.ANCHO/2, constante.ALTO * 0.85))
        espacio_ins2 = instruccion2.get_rect(center=(constante.ANCHO/2, constante.ALTO * 0.8))
        pantalla.blit(instruccion, espacio_ins)
        pantalla.blit(instruccion2,espacio_ins2)
        pygame.display.flip()    
        reloj.tick(constante.FPS)
        
