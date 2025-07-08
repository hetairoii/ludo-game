import pygame
import random
import time

# Inicializar juego
pygame.init()

# Definir display
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LUDO")

# Colores
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)

# Definición de variables
COLORES = [ROJO, VERDE, AZUL, AMARILLO]
CASAS = {
    ROJO: (75, 75),
    VERDE: (WIDTH - 175, 75),
    AZUL: (WIDTH - 175, HEIGHT - 175),
    AMARILLO: (75, HEIGHT - 175)
}

cell_size = 40

# Definir el camino principal (72 casillas: 52 comunes + 5 home por color + 1 meta por color)
camino = []

# --- Camino común (52 casillas) ---
# Arriba (de izquierda a derecha)
for x in range(10, 250, cell_size):  # 6 casillas horizontales
    camino.append((x, 270))
# Bajada derecha (de arriba a abajo)
for y in range(230, 10, -cell_size):  # 5 casillas verticales
    camino.append((270, y))

camino.append((300, 15)) #entrada a home path verde

# Derecha (de arriba a abajo)
for y in range(15, 230, cell_size):  # 6 casillas verticales
    camino.append((340, y))
# Arriba (de izquierda a derecha)
for x in range(380, 600, cell_size):  # 6 casillas horizontales
    camino.append((x, 270))

camino.append((580, 300)) #entrada a home path azul

# Bajada abajo (de derecha a izquierda)
for x in range(580, 340, -cell_size):  # 6 casillas horizontales
    camino.append((x, 340))
# Izquierda (de abajo a arriba)
for y in range(380, 600, cell_size):  # 6 casillas verticales
    camino.append((340, y))

camino.append((300, 580)) #entrada a home path amarillo

# Arriba izquierda (de abajo a arriba)
for y in range(580, 340, -cell_size):  # 6 casillas verticales
    camino.append((270, y))
# Subida izquierda (de derecha a izquierda)
for x in range(230, 10, -cell_size):  # 4 casillas horizontales
    camino.append((x, 340))

camino.append((10, 300)) #entrada a home path rojo

# --- Home paths (5 casillas por color) ---
# ROJO: home path horizontal, cada ficha en una fila diferente (desplazamiento en Y)
home_rojo = [
    [(250 + i * cell_size, 230 + 0 * 30) for i in range(1, 6)],  # Ficha 0
    [(250 + i * cell_size, 230 + 1 * 30) for i in range(1, 6)],  # Ficha 1
    [(250 + i * cell_size, 230 + 2 * 30) for i in range(1, 6)],  # Ficha 2
    [(250 + i * cell_size, 230 + 3 * 30) for i in range(1, 6)],  # Ficha 3
]

# VERDE: home path vertical, cada ficha en una columna diferente (desplazamiento en X)
home_verde = [
    [(470 + 0 * 30, 250 - i * cell_size) for i in range(1, 6)],  # Ficha 0
    [(470 + 1 * 30, 250 - i * cell_size) for i in range(1, 6)],  # Ficha 1
    [(470 + 2 * 30, 250 - i * cell_size) for i in range(1, 6)],  # Ficha 2
    [(470 + 3 * 30, 250 - i * cell_size) for i in range(1, 6)],  # Ficha 3
]

# AMARILLO: home path horizontal, cada ficha en una fila diferente (desplazamiento en Y)
home_amarillo = [
    [(250 - i * cell_size, 470 + 0 * 30) for i in range(1, 6)],  # Ficha 0
    [(250 - i * cell_size, 470 + 1 * 30) for i in range(1, 6)],  # Ficha 1
    [(250 - i * cell_size, 470 + 2 * 30) for i in range(1, 6)],  # Ficha 2
    [(250 - i * cell_size, 470 + 3 * 30) for i in range(1, 6)],  # Ficha 3
]

# AZUL: home path vertical, cada ficha en una columna diferente (desplazamiento en X)
home_azul = [
    [(270 - 0 * 30, 250 + i * cell_size) for i in range(1, 6)],  # Ficha 0
    [(270 - 1 * 30, 250 + i * cell_size) for i in range(1, 6)],  # Ficha 1
    [(270 - 2 * 30, 250 + i * cell_size) for i in range(1, 6)],  # Ficha 2
    [(270 - 3 * 30, 250 + i * cell_size) for i in range(1, 6)],  # Ficha 3
]

# Añadir home paths al camino (en orden ROJO, VERDE, AMARILLO, AZUL)
camino += home_rojo + home_verde + home_amarillo + home_azul

# --- Meta (centro) ---
meta = (WIDTH // 2, HEIGHT // 2)
camino += [meta] * 4  # Una meta para cada color

# Posiciones iniciales de las fichas (4 por jugador)
fichas = {
    ROJO: [(100, 100), (170, 100), (100, 170), (170, 170)],
    VERDE: [(WIDTH - 200, 100), (WIDTH - 130, 100), (WIDTH - 200, 170), (WIDTH - 130, 170)],
    AMARILLO: [(100, HEIGHT - 200), (170, HEIGHT - 200), (100, HEIGHT - 130), (170, HEIGHT - 130)],
    AZUL: [(WIDTH - 200, HEIGHT - 200), (WIDTH - 130, HEIGHT - 200), (WIDTH - 200, HEIGHT - 130), (WIDTH - 130, HEIGHT - 130)]
}

# Estado de fichas: -1 = en casa, >=0 = en camino (índice del camino)
estado_fichas = {
    ROJO: [-1, -1, -1, -1],
    VERDE: [-1, -1, -1, -1],
    AZUL: [-1, -1, -1, -1],
    AMARILLO: [-1, -1, -1, -1]
}

# Índice de inicio para cada color en el camino
inicio_camino = {
    ROJO: 0,
    VERDE: 13,
    AZUL: 26,
    AMARILLO: 39
}

# Diccionario para acceder fácil por color y ficha
home_paths = {
    ROJO: home_rojo,
    VERDE: home_verde,
    AMARILLO: home_amarillo,
    AZUL: home_azul
}

j_actual = 0
dado_val = 0
ficha_seleccionada = None

def get_color_turno():
    return COLORES[j_actual]

def pos_en_casa(color, idx):
    return fichas[color][idx]

def pos_en_camino(color, idx_ficha):
    idx = estado_fichas[color][idx_ficha]
    if idx == -1:
        return fichas[color][idx_ficha]
    # El índice de entrada a home para cada color
    entrada_home = (inicio_camino[color] + 51) % 52
    if idx <= 51:
        # Camino común
        pos = (inicio_camino[color] + idx) % 52
        return camino[pos]
    elif 52 <= idx <= 57:
        # Home path propio de la ficha
        home_idx = idx - 52
        return home_paths[color][idx_ficha][home_idx]
    else:
        # Meta (centro)
        return (WIDTH // 2, HEIGHT // 2)

def mover_ficha(color, idx, dado_val):
    """Mueve la ficha y gestiona comer y entrada a home path."""
    global estado_fichas

    pos_actual = estado_fichas[color][idx]
    if pos_actual == -1 and dado_val == 6:
        # Sale de casa
        estado_fichas[color][idx] = 0
        return True

    if pos_actual >= 0:
        nuevo_idx = pos_actual + dado_val
        # ¿Está en el camino común y va a entrar a home path?
        if pos_actual <= 51 and nuevo_idx > 51:
            # Solo entra a home path si está en la entrada de su color
            if ((inicio_camino[color] + pos_actual) % 52) == ((inicio_camino[color] + 51) % 52):
                # Entra a home path propio
                estado_fichas[color][idx] = 52 + (nuevo_idx - 52)
                if estado_fichas[color][idx] > 57:
                    estado_fichas[color][idx] = 57  # No pasa del centro
            else:
                # Si no es su entrada a home, sigue el camino común
                estado_fichas[color][idx] = (inicio_camino[color] + nuevo_idx) % 52
        else:
            # Si ya está en home path o camino común normal
            if nuevo_idx > 57:
                estado_fichas[color][idx] = 57  # No pasa del centro
            else:
                estado_fichas[color][idx] = nuevo_idx

        # --- COMER FICHAS ---
        # Solo se puede comer en el camino común (idx <= 51)
        if estado_fichas[color][idx] <= 51:
            pos_ficha = (inicio_camino[color] + estado_fichas[color][idx]) % 52
            for otro_color in COLORES:
                if otro_color == color:
                    continue
                for j in range(4):
                    # Solo fichas en camino común
                    if estado_fichas[otro_color][j] >= 0 and estado_fichas[otro_color][j] <= 51:
                        pos_otro = (inicio_camino[otro_color] + estado_fichas[otro_color][j]) % 52
                        if pos_ficha == pos_otro:
                            # Comer: regresa la ficha comida a casa
                            estado_fichas[otro_color][j] = -1

    return True

def seleccionar_ficha(mouse_pos, color):
    for idx, pos in enumerate([pos_en_casa(color, i) if estado_fichas[color][i] == -1 else pos_en_camino(color, i) for i in range(4)]):
        dist = ((mouse_pos[0] - pos[0]) ** 2 + (mouse_pos[1] - pos[1]) ** 2) ** 0.5
        if dist < 25:
            return idx
    return None

def draw_board():
    # Casas de colores
    pygame.draw.rect(screen, ROJO, (0, 0, 250, 250))
    pygame.draw.rect(screen, VERDE, (350, 0, 250, 250))
    pygame.draw.rect(screen, AMARILLO, (0, 350, 250, 250))
    pygame.draw.rect(screen, AZUL, (350, 350, 250, 250))
    pygame.draw.rect(screen, BLANCO, (250, 250, 100, 100))  # Centro

    #Caminos de cada lado (con casillas)
    #Verde-Azul
    for i in range(6):
        rect = pygame.Rect(360 + i * cell_size, 250, cell_size, cell_size)
        pygame.draw.rect(screen, GRIS, rect)
        pygame.draw.rect(screen, NEGRO, rect, 2)
    
    #Rojo-Verde
    for i in range(6):
        rect = pygame.Rect(250, i * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, GRIS, rect)
        pygame.draw.rect(screen, NEGRO, rect, 2)
    
    #Azul-Verde
    for i in range(6):
        rect = pygame.Rect(560 - i * cell_size, 310, cell_size, cell_size)
        pygame.draw.rect(screen, GRIS, rect)
        pygame.draw.rect(screen, NEGRO, rect, 2)
    
    # Amarillo-Azul
    for i in range(6):
        rect = pygame.Rect(250, 560 - i * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, GRIS, rect)
        pygame.draw.rect(screen, NEGRO, rect, 2)

    # Azul-Amarillo
    for i in range(6):
        rect = pygame.Rect(310, 560 - i * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, GRIS, rect)
        pygame.draw.rect(screen, NEGRO, rect, 2)

    # Amarillo-Rojo
    for i in range(6):
        rect = pygame.Rect(200 - i * cell_size, 310, cell_size, cell_size)
        pygame.draw.rect(screen, GRIS, rect)
        pygame.draw.rect(screen, NEGRO, rect, 2)

    # Rojo-amarillo
    for i in range(6):
        rect = pygame.Rect(200 - i * cell_size, 250, cell_size, cell_size)
        pygame.draw.rect(screen, GRIS, rect)
        pygame.draw.rect(screen, NEGRO, rect, 2)

    #Verde-Rojo
    for i in range(6):
        rect = pygame.Rect(310, i * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, GRIS, rect)
        pygame.draw.rect(screen, NEGRO, rect, 2)
    
    #Verde-centro
    for i in range(6):
        rect = pygame.Rect(280, i * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, VERDE, rect)
        pygame.draw.rect(screen, NEGRO, rect, 2)

    #Amarillo-centro
    for i in range(6):
        rect = pygame.Rect(280, 560 - i * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, AMARILLO, rect)
        pygame.draw.rect(screen, NEGRO, rect, 2)

    #Azul-centro
    for i in range(6):
        rect = pygame.Rect(360 + i * cell_size, 280, cell_size, cell_size)
        pygame.draw.rect(screen, AZUL, rect)
        pygame.draw.rect(screen, NEGRO, rect, 2)

    #Rojo-centro
    for i in range(6):
        rect = pygame.Rect(0 + i * cell_size, 280, cell_size, cell_size)
        pygame.draw.rect(screen, ROJO, rect)
        pygame.draw.rect(screen, NEGRO, rect, 2)

    #home rojo
    pygame.draw.circle(screen, ROJO, (WIDTH - 350, HEIGHT // 2), 20)
    pygame.draw.circle(screen, NEGRO, (WIDTH - 350, HEIGHT // 2), 20, 2)

    #home azul
    pygame.draw.circle(screen, AZUL, (WIDTH - 250, HEIGHT // 2), 20)
    pygame.draw.circle(screen, NEGRO, (WIDTH - 250, HEIGHT // 2), 20, 2)

    #home amarillo
    pygame.draw.circle(screen, AMARILLO, (WIDTH // 2, HEIGHT - 250), 20)
    pygame.draw.circle(screen, NEGRO, (WIDTH // 2, HEIGHT - 250), 20, 2)

    #home verde
    pygame.draw.circle(screen, VERDE, (WIDTH // 2, HEIGHT - 350), 20)
    pygame.draw.circle(screen, NEGRO, (WIDTH // 2, HEIGHT - 350), 20, 2)

    # Centro (dado)
    pygame.draw.circle(screen, BLANCO, (WIDTH // 2, HEIGHT // 2), 30)
    pygame.draw.circle(screen, NEGRO, (WIDTH // 2, HEIGHT // 2), 30, 2)

# Variables para controlar los lanzamientos de dado por turno
lanzamientos_seguidos = 0
ultimo_seis = False

# NUEVO: Variables para mostrar mensaje de penalización
mensaje_penalizacion = ""
mostrar_mensaje_hasta = 0

running = True
while running:
    screen.fill(BLANCO)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and dado_val == 0 and not mensaje_penalizacion:
                # Solo permite tirar si no hay dado pendiente ni mensaje de penalización activo
                dado_val = random.randint(1, 6)
                if dado_val == 6:
                    lanzamientos_seguidos += 1
                    ultimo_seis = True
                    if lanzamientos_seguidos == 3:
                        # Pierde el turno si saca tres seises seguidos
                        mensaje_penalizacion = f"¡{['Rojo','Verde','Azul','Amarillo'][j_actual]} pierde turno por 3 seises!"
                        mostrar_mensaje_hasta = pygame.time.get_ticks() + 1500  # 1.5 segundos
                        dado_val = 0
                        lanzamientos_seguidos = 0
                        ultimo_seis = False
                        # NO cambiar turno aquí, lo haremos después de mostrar el mensaje
                else:
                    ultimo_seis = False

                # Validar si no tiene fichas en el tablero y no sacó 6
                color = get_color_turno()
                fichas_fuera = any(f >= 0 for f in estado_fichas[color])
                if not fichas_fuera and dado_val != 6:
                    # Mostrar el dado por un momento antes de pasar turno
                    draw_board()
                    for color_draw in COLORES:
                        for idx in range(4):
                            pos = pos_en_casa(color_draw, idx) if estado_fichas[color_draw][idx] == -1 else pos_en_camino(color_draw, idx)
                            pygame.draw.circle(screen, color_draw, pos, 18)
                            pygame.draw.circle(screen, NEGRO, pos, 18, 2)
                            if color_draw == get_color_turno() and idx == ficha_seleccionada:
                                pygame.draw.circle(screen, NEGRO, pos, 22, 3)
                    fuente = pygame.font.Font(None, 36)
                    text = fuente.render(f"Dado: {dado_val}", True, NEGRO)
                    turno_text = fuente.render(f"Turno: {['Rojo','Verde','Azul','Amarillo'][j_actual]}", True, COLORES[j_actual])

                    # Fondo y posiciones para la esquina inferior izquierda
                    padding = 10
                    ancho_minimo = 220
                    ancho = max(ancho_minimo, text.get_width(), turno_text.get_width()) + 2 * padding
                    alto = text.get_height() + turno_text.get_height() + 3 * padding
                    fondo_rect = pygame.Rect(0, HEIGHT - alto, ancho, alto)
                    pygame.draw.rect(screen, (220, 220, 220), fondo_rect)
                    pygame.draw.rect(screen, NEGRO, fondo_rect, 2)
                    text_pos = (padding, HEIGHT - alto + padding)
                    turno_pos = (padding, HEIGHT - alto + text.get_height() + 2 * padding)
                    screen.blit(text, text_pos)
                    screen.blit(turno_text, turno_pos)

                    pygame.display.flip()
                    pygame.time.wait(1200)
                    dado_val = 0
                    lanzamientos_seguidos = 0
                    ultimo_seis = False
                    j_actual = (j_actual + 1) % 4

            elif event.key == pygame.K_RETURN and ficha_seleccionada is not None and dado_val > 0 and not mensaje_penalizacion:
                color = get_color_turno()
                idx = ficha_seleccionada
                mover_ficha(color, idx, dado_val)

                # Control de turnos y lanzamientos
                if dado_val == 6 and lanzamientos_seguidos < 3:
                    dado_val = 0
                    ficha_seleccionada = None
                else:
                    j_actual = (j_actual + 1) % 4
                    dado_val = 0
                    lanzamientos_seguidos = 0
                    ultimo_seis = False
                    ficha_seleccionada = None

        elif event.type == pygame.MOUSEBUTTONDOWN and dado_val > 0 and not mensaje_penalizacion:
            color = get_color_turno()
            ficha_seleccionada = seleccionar_ficha(event.pos, color)

    # --- Penalización por tres seises seguidos ---
    if mensaje_penalizacion and pygame.time.get_ticks() >= mostrar_mensaje_hasta:
        # Pasó el tiempo de mostrar el mensaje, cambia turno y limpia mensaje
        j_actual = (j_actual + 1) % 4
        mensaje_penalizacion = ""
        dado_val = 0
        lanzamientos_seguidos = 0
        ultimo_seis = False
        ficha_seleccionada = None

    draw_board()

    # Dibujar fichas de cada jugador
    for color in COLORES:
        for idx in range(4):
            pos = pos_en_casa(color, idx) if estado_fichas[color][idx] == -1 else pos_en_camino(color, idx)
            pygame.draw.circle(screen, color, pos, 18)
            pygame.draw.circle(screen, NEGRO, pos, 18, 2)
            if color == get_color_turno() and idx == ficha_seleccionada:
                pygame.draw.circle(screen, NEGRO, pos, 22, 3)

    # --- Dado, turno y mensaje en la esquina inferior izquierda con fondo ---
    fuente = pygame.font.Font(None, 36)
    text = fuente.render(f"Dado: {dado_val}", True, NEGRO)
    turno_text = fuente.render(f"Turno: {['Rojo','Verde','Azul','Amarillo'][j_actual]}", True, COLORES[j_actual])
    mensaje_text = None
    if mensaje_penalizacion:
        fuente_mensaje = pygame.font.Font(None, 20)
        mensaje_text = fuente_mensaje.render(mensaje_penalizacion, True, (200, 0, 0))

    # El área de las fichas amarillas es de 250x250 px (ver draw_board), así que el ancho fijo debe ser 250
    padding = 10
    ancho_fijo = 250  # Igual al ancho de la caja de las fichas amarillas
    alto = text.get_height() + turno_text.get_height() + (mensaje_text.get_height() if mensaje_text else 0) + 4 * padding

    fondo_rect = pygame.Rect(0, HEIGHT - alto, ancho_fijo, alto)
    pygame.draw.rect(screen, (220, 220, 220), fondo_rect)
    pygame.draw.rect(screen, NEGRO, fondo_rect, 2)

    y_actual = HEIGHT - alto + padding
    screen.blit(text, (padding, y_actual))
    y_actual += text.get_height() + padding
    screen.blit(turno_text, (padding, y_actual))
    y_actual += turno_text.get_height() + padding
    if mensaje_text:
        screen.blit(mensaje_text, (padding, y_actual))

    pygame.display.flip()

pygame.quit()