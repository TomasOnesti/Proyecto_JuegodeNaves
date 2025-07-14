import pygame, json
import database
import sys
import os
ANCHO = 1000#Ancho de la pantalla
ALTO = 700#Alto de la pantalla
FPS = 300#Cantidad de Frame por Segundo 
tamaño =(ANCHO, ALTO) #Tamaño de la pantalla
efecto=0.4
musica =0.7

db=database.Ranking()

def fuente_escalada(tipo,porcentaje = 0.05):
    # Usa un porcentaje de la altura de pantalla para determinar el tamaño
    tamaño = int(ALTO * porcentaje)
    return pygame.font.Font(tipo, tamaño)

def resource_path(relative_path):
    try:
        # Si se ejecuta desde un .exe hecho con PyInstaller
        base_path = sys._MEIPASS
    except AttributeError:
        # Si se ejecuta como script normal
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def mostrar_ranking(pantalla, colores, fuente, fondo, db):
    with open(db.archivo, 'r') as f:
        datos = json.load(f)

    datos = sorted(datos, key=lambda x: x['puntaje'], reverse=True)[:10]

    salir = False
    while not salir:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    salir = True

        pantalla.blit(fondo, (0, 0))

        # Fondo negro transparente
        overlay = pygame.Surface((ANCHO * 0.8, ALTO * 0.8))
        overlay.set_alpha(180)
        overlay.fill(colores.BLACK)
        pantalla.blit(overlay, (ANCHO * 0.1, ALTO * 0.1))

        # Título
        fuente_titulo = fuente_escalada(None,0.06)
        titulo = fuente_titulo.render("Ranking", True, colores.YELLOW)
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO/2, ALTO * 0.15)))

        # Mostrar rankings
        fuente_ranking = fuente_escalada(None,0.045)
        for i, entrada in enumerate(datos):
            texto = f"{i+1}. {entrada['usuario']}: {entrada['puntaje']}"
            render = fuente_ranking.render(texto, True, colores.WHITE)
            pantalla.blit(render, (ANCHO * 0.15, ALTO * 0.22 + i * 40))

        # Instrucción para salir
        instruccion = fuente.render("Presiona ESC para volver", True, colores.YELLOW)
        pantalla.blit(instruccion, (ANCHO/2 - instruccion.get_width()/2, ALTO * 0.9))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

def mostrar_controles(pantalla, colores, fuente, fondo):
    import pygame
    from constante import ANCHO, ALTO

    ejecutando = True
    clock = pygame.time.Clock()

    while ejecutando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ejecutando = False

        # Fondo base
        pantalla.blit(fondo, (0, 0))

        # Overlay semitransparente
        overlay = pygame.Surface((ANCHO * 0.8, ALTO * 0.8))
        overlay.set_alpha(180)
        overlay.fill(colores.BLACK)
        pantalla.blit(overlay, (ANCHO * 0.1, ALTO * 0.1))

        # Título
        ruta_fuente = resource_path("DejaVuSans.ttf")
        fuente_titulo = pygame.font.Font(ruta_fuente,30)
        titulo = fuente_titulo.render("Controles", True, colores.YELLOW)
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO/2, ALTO * 0.15)))

        # Lista de controles
        fuente_texto = pygame.font.Font(ruta_fuente,20)
        controles = [
            "Movimiento: ↑ ↓ → ←",
            "Disparo: Z",
            "Cambiar arma: X",
            "Pausa: P",
            "Mute: M",
        ]

        for i, texto in enumerate(controles):
            render = fuente_texto.render(texto, True, colores.WHITE)
            pantalla.blit(render, (ANCHO * 0.15, ALTO * 0.30 + i * 45))

        # Instrucción para volver
        instruccion = fuente.render("Presiona ESC para volver", True, colores.YELLOW)
        pantalla.blit(instruccion, (ANCHO/2 - instruccion.get_width()/2, ALTO * 0.9))

        pygame.display.flip()
        clock.tick(30)

#Clase con colores para usar
class color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW=(255,255,0)