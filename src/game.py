import pygame
import random

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
# ROJO (de la casilla de entrada a la meta)
home_rojo = [(250 + i * cell_size, 270) for i in range(1, 6)]
# VERDE
home_verde = [(470, 250 - i * cell_size) for i in range(1, 6)]
# AMARILLO
home_amarillo = [(250 - i * cell_size, 470) for i in range(1, 6)]
# AZUL
home_azul = [(270, 250 + i * cell_size) for i in range(1, 6)]

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

# Casillas de home (camino al centro) para cada color
home_paths = {
    ROJO: [(250 + cell_size, 230 - i * cell_size) for i in range(1, 6)],
    VERDE: [(350 + i * cell_size, 10 + cell_size) for i in range(1, 6)],
    AZUL: [(350 - cell_size, 450 + i * cell_size) for i in range(1, 6)],
    AMARILLO: [(130 - i * cell_size, 350 - cell_size) for i in range(1, 6)]
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
    else:
        pos = (inicio_camino[color] + idx) % len(camino)
        # Si la ficha está en home path
        if idx >= len(camino):
            home_idx = idx - len(camino)
            if home_idx < 5:
                return home_paths[color][home_idx]
            else:
                # Centro (meta)
                return (WIDTH // 2, HEIGHT // 2)
        return camino[pos]

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

running = True
while running:
    screen.fill(BLANCO)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dado_val = random.randint(1, 6)
                ficha_seleccionada = None  # Reset selección al tirar dado
            elif event.key == pygame.K_RETURN and ficha_seleccionada is not None and dado_val > 0:
                color = get_color_turno()
                idx = ficha_seleccionada
                # Si la ficha está en casa y saca 6, sale
                if estado_fichas[color][idx] == -1 and dado_val == 6:
                    estado_fichas[color][idx] = 0
                # Si la ficha está en el camino, avanza
                elif estado_fichas[color][idx] >= 0:
                    estado_fichas[color][idx] += dado_val
                    # Si llega a home path
                    if estado_fichas[color][idx] > len(camino) + 5:
                        estado_fichas[color][idx] = len(camino) + 5  # No pasa del centro
                # Cambiar turno si no sacó 6
                if dado_val != 6:
                    j_actual = (j_actual + 1) % 4
                dado_val = 0
                ficha_seleccionada = None
        elif event.type == pygame.MOUSEBUTTONDOWN and dado_val > 0:
            color = get_color_turno()
            ficha_seleccionada = seleccionar_ficha(event.pos, color)

    draw_board()

    # Dibujar fichas de cada jugador
    for color in COLORES:
        for idx in range(4):
            pos = pos_en_casa(color, idx) if estado_fichas[color][idx] == -1 else pos_en_camino(color, idx)
            pygame.draw.circle(screen, color, pos, 18)
            pygame.draw.circle(screen, NEGRO, pos, 18, 2)
            # Resalta la ficha seleccionada
            if color == get_color_turno() and idx == ficha_seleccionada:
                pygame.draw.circle(screen, NEGRO, pos, 22, 3)

    # Dibujar valor del dado y turno SIEMPRE centrado
    fuente = pygame.font.Font(None, 36)
    text = fuente.render(f"Dado: {dado_val}", True, NEGRO)
    turno_text = fuente.render(f"Turno: {['Rojo','Verde','Azul','Amarillo'][j_actual]}", True, COLORES[j_actual])

    # Obtener el rectángulo del texto para centrarlo
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    turno_rect = turno_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))

    screen.blit(text, text_rect)
    screen.blit(turno_text, turno_rect)

    pygame.display.flip()

pygame.quit()