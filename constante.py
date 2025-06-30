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

def pedir_codigo(pantalla, colores, fuente, fondo):
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
            mensaje = fuente.render("Ingresá el código secreto:", True, colores.WHITE)
            input_texto = fuente.render(texto, True, colores.YELLOW)
            rect_mensaje = mensaje.get_rect(center=(ANCHO/2, ALTO * 0.3))
            rect_input = input_texto.get_rect(center=(ANCHO/2, ALTO * 0.5))

            pantalla.blit(mensaje, rect_mensaje)
            pantalla.blit(input_texto, rect_input)

            pygame.display.flip()
            pygame.time.Clock().tick(30)

        return texto


#Clase con colores para usar
class color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW=(255,255,0)