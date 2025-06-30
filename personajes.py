import pygame, random, constante, time
from armas import *
pygame.init()
#Clase del jugador

class jugador():
    def __init__(self):
        self.ancho = 65
        self.alto = 65
        self.size = (self.ancho, self.alto)

        # Imágenes
        self.img_normal = pygame.image.load(constante.resource_path("elementos/assets/player/nave1_.png")).convert_alpha()
        self.img_arma2 = pygame.image.load(constante.resource_path("elementos/assets/player/nave3.png")).convert_alpha()
        self.img_arma3 = pygame.image.load(constante.resource_path("elementos/assets/player/nave4.png")).convert_alpha()
        self.img_actual = self.img_normal
        self.img_actual = pygame.transform.scale(self.img_actual, self.size)

        self.nave = pygame.Rect(80 - self.ancho - 10,
                                constante.ALTO // 2 - self.alto // 2, self.ancho, self.alto).inflate(-10, -8)

        # Arma 1
        self.balas = []
        self.tiempo_ultimo_disparo = 0
        self.delay_disparo = 200
        self.max_balas = 12
        self.balas_restantes = self.max_balas
        self.tiempo_recarga = 1000
        self.esta_recargando = False
        self.tiempo_inicio_recarga = 0

        # Arma 2
        self.arma2_balas = 250
        self.arma = 1  
        
        #Arma 3
        self.arma3_balas = 60
        self.delay_disparo2 = 600
        # Transición / inmortalidad
        self.en_animacion = False
        self.inmortal = False
        self.tiempo_animacion = 0
        self.duracion_animacion = 1000
        self.duracion_inmortal = 1000

    def iniciar_cambio_arma(self, nueva_arma):
        self.en_animacion = True
        self.inmortal = True
        self.tiempo_animacion = pygame.time.get_ticks()
        self.arma = nueva_arma

    def actualizar_estado(self):
        tiempo_actual = pygame.time.get_ticks()

        # Finalizar animación
        if self.en_animacion and tiempo_actual - self.tiempo_animacion > self.duracion_animacion:
            self.en_animacion = False
            self.tiempo_animacion = tiempo_actual  # Para contar el tiempo extra de invulnerabilidad

            # Establecer imagen fija final
            if self.arma == 1:
                self.img_actual = pygame.transform.scale(self.img_normal, self.size)
            elif self.arma == 3:
                self.img_actual = pygame.transform.scale(self.img_arma3, self.size)
            else:
                self.img_actual = pygame.transform.scale(self.img_arma2, self.size)
        # Inmortalidad extra luego de la animación
        if not self.en_animacion and self.inmortal:
            if tiempo_actual - self.tiempo_animacion > self.duracion_inmortal:
                self.inmortal = False

        # Recarga arma 1
        if self.arma == 1 and self.esta_recargando:
            if tiempo_actual - self.tiempo_inicio_recarga >= self.tiempo_recarga:
                self.esta_recargando = False
                self.balas_restantes = self.max_balas

    def movimiento(self):
        if self.en_animacion:
            return  # Bloquea movimiento en animación
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.nave.left > 0:
            self.nave.x -= 4
        if keys[pygame.K_RIGHT] and self.nave.right < constante.ANCHO:
            self.nave.x += 4
        if keys[pygame.K_DOWN] and self.nave.bottom < constante.ALTO:
            self.nave.y += 4
        if keys[pygame.K_UP] and self.nave.top > 0:
            self.nave.y -= 4

    def disparar(self):
        tiempo_actual = pygame.time.get_ticks()

        if self.arma == 1:
            if self.esta_recargando:
                return
            if tiempo_actual - self.tiempo_ultimo_disparo < self.delay_disparo:
                return
            if self.balas_restantes > 0:
                offset_y = 34
                izquierda_x = self.nave.left + 34
                derecha_x = self.nave.right - 34
                centro_y = self.nave.centery

                bala_izquierda = Balas(izquierda_x, centro_y - offset_y)
                bala_derecha = Balas(derecha_x, centro_y + offset_y)

                self.balas.append(bala_izquierda)
                self.balas.append(bala_derecha)

                self.tiempo_ultimo_disparo = tiempo_actual
                self.balas_restantes -= 1

                if self.balas_restantes <= 0:
                    self.esta_recargando = True
                    self.tiempo_inicio_recarga = tiempo_actual

        elif self.arma == 2:
            if self.arma2_balas <= 0:
                self.iniciar_cambio_arma(1)
                return

            if tiempo_actual - self.tiempo_ultimo_disparo :
                centro_x = self.nave.centerx
                centro_y = self.nave.centery
                bala = Balas(centro_x, centro_y)
                self.balas.append(bala)
                self.tiempo_ultimo_disparo = tiempo_actual
                self.arma2_balas -= 1
                
        elif self.arma ==3:
            if self.arma3_balas <= 0:
                self.iniciar_cambio_arma(1)
                return

            if tiempo_actual - self.tiempo_ultimo_disparo > self.delay_disparo2:
                centro_x = self.nave.centerx
                centro_y = self.nave.centery
                offset = 10
                for i in range(-2,3):
                    desplazamiento_x = i * 20
                    desplazamiento_y = i * offset
                    bala = Balas(centro_x + desplazamiento_x, centro_y + desplazamiento_y)
                    bala.velocidad_x = 10
                    bala.velocidad_y = i * 3 # ángulo variable
                    self.balas.append(bala)    
                self.arma3_balas -= 1
                self.tiempo_ultimo_disparo = tiempo_actual        
                        
    def render(self, pantalla):
        """Mostrar la nave con animación parpadeante si está en transición."""
        tiempo_actual = pygame.time.get_ticks()
        mostrar = True
        if self.en_animacion:
            if (tiempo_actual // 150) % 2 == 0:
                mostrar = False  # Hace parpadear
        if mostrar:
            pantalla.blit(self.img_actual, self.nave)
            
#Clase de los meteoritos
class meteoritos():
    def __init__(self):
        self.imgmeteorito = pygame.image.load(constante.resource_path("elementos/assets/enemigos/meteorito1.png")).convert_alpha()#Imagen de los meteoritos
        self.imgmeteorito2= pygame.image.load(constante.resource_path("elementos/assets/enemigos/meteorito_2.png")).convert_alpha()
        self.meteoros={
            "meteorobase":(60,70),
            "tamanios": {
                "grande":(80,80),
                "mediano": (60,60),
                "chico":(40,40)
            },
            "velocidades":{
                "lento": 0.5,
                "medio": 2,
                "rapido":3.5
            }
        }
        self.size_met1=(self.meteoros["meteorobase"][0], self.meteoros["meteorobase"][1])#Tamaño de los meteoritos
        self.imgmeteorito = pygame.transform.scale(self.imgmeteorito, self.size_met1)#Escala la imagen a un tamaño especifico
        self.meteoritosl =[]#Lista para almacenar los meteoritos
        #Funciones del meteorito
        
    def generar_meteorito1(self):
        #Generacion Meteoritos normales
        tamaño = self.meteoros["meteorobase"]
        velocidad = self.meteoros["velocidades"]["medio"]
        rect = pygame.Rect(950, random.randint(0, constante.ALTO - tamaño[1]), tamaño[0], tamaño[1])
        rect = rect.inflate(-6, -8)
        img = pygame.transform.scale(self.imgmeteorito, tamaño)
        meteor = {"rect": rect, "tipo": "normal", "velocidad": velocidad, "img": img}
        self.meteoritosl.append(meteor)
        
    def generar_meteoritos2(self):
        #generar meteoritos divisibles
        tamaño = self.meteoros["tamanios"]["grande"]
        velocidad = self.meteoros["velocidades"]["medio"]
        rect = pygame.Rect(950, random.randint(0, constante.ALTO - tamaño[1]), tamaño[0], tamaño[1])
        rect = rect.inflate(-6, -8)
        img = pygame.transform.scale(self.imgmeteorito2, tamaño)
        meteor = {"rect": rect, "tipo": "divisible", "size_key": "grande", "velocidad": velocidad, "img": img}
        self.meteoritosl.append(meteor)
        
    def funcionesmeteorito(self, niveles_generacion, indice_dif):
    # Generación de meteoritos
        if len(self.meteoritosl) < niveles_generacion[indice_dif]:
            if random.random() < 0.5:
                self.generar_meteorito1()
            else:
                self.generar_meteoritos2()

        # Movimiento y eliminación de meteoritos fuera de pantalla
        for meteorito in self.meteoritosl[:]:
            meteorito["rect"].x -= meteorito["velocidad"]
            if meteorito["rect"].right <= 0:
                self.meteoritosl.remove(meteorito)
                
    def dividir_meteoritos(self, meteorito):
        if meteorito["tipo"] != "divisible":
            return[]
        
        if meteorito["size_key"] == "grande":
            nuevo_tamaño_key = "mediano"
        elif meteorito["size_key"] == "mediano":
            nuevo_tamaño_key = "chico"
        else:
            return []  # "chico" no se divide
        
        nuevo_tamaño = self.meteoros["tamanios"][nuevo_tamaño_key]
        velocidad = meteorito["velocidad"]
        meteoritos_nuevos = []
        #Pequeña separacion de los meteoritos al dividirse
        separacion = [
        (0, 0),
        (int(nuevo_tamaño[0] * 0.9), int(nuevo_tamaño[1] * 0.9))
        ]
        for off in separacion:
            x = meteorito["rect"].x + off[0]
            y = meteorito["rect"].y + off[1]
            rect = pygame.Rect(x, y, nuevo_tamaño[0], nuevo_tamaño[1])
            rect = rect.inflate(-7, -7)
            img = pygame.transform.scale(self.imgmeteorito2, nuevo_tamaño)
            nuevo_meteorito = {
                "rect": rect, 
                "tipo": "divisible", 
                "size_key": nuevo_tamaño_key, 
                "velocidad": velocidad, 
                "img": img
            }
            meteoritos_nuevos.append(nuevo_meteorito)
        return meteoritos_nuevos
    
class enemigo():
    def __init__(self):
        self.enemigo =pygame.image.load(constante.resource_path("elementos/assets/enemigos/enemigo1.png"))
        self.ancho_enemigo = 70
        self.alto_enemigo = 70
        self.size_enemigo = (self.alto_enemigo, self.ancho_enemigo)
        self.img_enemigo = pygame.transform.scale(self.enemigo, self.size_enemigo)
        self.lista_enemigos=[]
        self.lista_balas_enemigas=[]
        
    def crear_enemigos(self, niveles_generacion, indice_dif):
        cantidad = niveles_generacion[indice_dif]
        for _ in range(cantidad):
            y_random = random.randint(50, constante.ALTO - 100)
            enemigo_rect = pygame.Rect(constante.ANCHO, y_random, self.ancho_enemigo, self.alto_enemigo)
            self.lista_enemigos.append({
                "rect": enemigo_rect,
                "estado": "avanzando",
                "direccion_y": random.choice(["arriba", "abajo"]),
                "tiempo_ultimo_disparo": 0
            })
    
    def mover_y_disparar(self):
        tiempo_actual = pygame.time.get_ticks()

        for enemigo in self.lista_enemigos[:]:
            rect = enemigo["rect"]

            # Movimiento
            if enemigo["estado"] == "avanzando":
                rect.x -= 2
                if rect.x <= constante.ANCHO // 2:
                    enemigo["estado"] = "retrocediendo"
            elif enemigo["estado"] == "retrocediendo":
                rect.x += 1
                if rect.x >= constante.ANCHO - self.ancho_enemigo:
                    enemigo["estado"] = "saliendo"
            elif enemigo["estado"] == "saliendo":
                if enemigo["direccion_y"] == "arriba":
                    rect.y -= 2
                else:
                    rect.y += 2
            
            if rect.bottom < 0 or rect.top > constante.ALTO:
                self.lista_enemigos.remove(enemigo)
                continue
            
            if tiempo_actual - enemigo["tiempo_ultimo_disparo"] >= 1000:
                x1 = rect.centerx - 5
                x2 = rect.centerx + 5
                centro_y = rect.centery
                
                bala1 = BalaEnemiga(x1, centro_y)
                bala2 = BalaEnemiga(x2, centro_y)
                
                self.lista_balas_enemigas.append(bala1)
                self.lista_balas_enemigas.append(bala2)
                enemigo["tiempo_ultimo_disparo"] = tiempo_actual
                
        for bala in self.lista_balas_enemigas[:]:
            bala.mover()
            if bala.rect.right < 0:
                self.lista_balas_enemigas.remove(bala)
                
class jefe():
    def __init__(self):
        self.imgjefe = pygame.image.load(constante.resource_path("elementos/assets/enemigos/jefe.png")).convert_alpha()
        self.ancho = 350
        self.alto = 250
        self.vida = 2000
        
        self.size = (self.ancho,self.alto)
        self.imgjefe = pygame.transform.scale(self.imgjefe, self.size)
        self.rect = pygame.Rect(constante.ANCHO - self.ancho - 150, constante.ALTO // 2 - self.alto // 2, self.ancho, self.alto)

        
        self.velocidad_y = 1
        self.direccion = 1
        
        self.lista_balas = []
        self.delay_disparo = 1000  
        self.separacion_doble = 4  
        self.distancia_entre_cañones = 80
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()
    
    def mover(self):
        self.rect.y += self.velocidad_y * self.direccion
        if self.rect.top <= 0 or self.rect.bottom >= constante.ALTO:
            self.direccion *= -1
    
    def disparar(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_ultimo_disparo >= self.delay_disparo:
            cañones = [
                {"y": self.rect.top + 8, "x_offset": 118},   # cañón superior 
                {"y": self.rect.top + -10 + self.distancia_entre_cañones, "x_offset": 50},  # intermedio superior
                {"y": self.rect.top + 25 + self.distancia_entre_cañones * 2, "x_offset": 50},  # intermedio inferior
                {"y": self.rect.top + -2 + self.distancia_entre_cañones * 3, "x_offset": 120}   # cañón inferior 
            ]

            for cañon in cañones:
                x = self.rect.left + cañon["x_offset"] + 50  # +50 para compensar que el jefe es más ancho ahora
                y1 = cañon["y"] - self.separacion_doble
                y2 = cañon["y"] + self.separacion_doble
                self.lista_balas.append(BalaEnemiga(x, y1))
                self.lista_balas.append(BalaEnemiga(x, y2))

            self.tiempo_ultimo_disparo = tiempo_actual
            
    def render(self, pantalla):
        pantalla.blit(self.imgjefe, self.rect)
        pygame.draw.rect(pantalla, (255, 0, 0), self.rect, 2)
        