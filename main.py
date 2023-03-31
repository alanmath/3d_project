import pygame
import numpy as np


def rotation_matrix_x(angle):
    angulo_em_radianos = np.radians(angle)
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(angulo_em_radianos), -np.sin(angulo_em_radianos), 0],
        [0, np.sin(angulo_em_radianos), np.cos(angulo_em_radianos), 0], 
        [0, 0, 0, 1]
    ])

def rotation_matrix_y(angle):
    angulo_em_radianos = np.radians(angle)
    return np.array([
        [np.cos(angulo_em_radianos), 0, np.sin(angulo_em_radianos), 0],
        [0, 1, 0, 0],
        [-np.sin(angulo_em_radianos), 0, np.cos(angulo_em_radianos), 0], 
        [0, 0, 0, 1]
    ])

def rotation_matrix_z(angle):
    angulo_em_radianos = np.radians(angle)
    return np.array([
        [np.cos(angulo_em_radianos), -np.sin(angulo_em_radianos), 0, 0],
        [np.sin(angulo_em_radianos), np.cos(angulo_em_radianos), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def translation_matrix(x, y, z):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])

def project_points(points, focal_length):
    transformation_matrix = np.array([[0,0,0,-focal_length], [1,0,0,0], [0,1,0,0], [0,0,-1/focal_length,0]])
    matrix_wp = transformation_matrix @ points
    projected_points = []
    for i,point in enumerate(matrix_wp.T):
        w = point[3]
        projected_points.append((point[1]/w, point[2]/w, points[2][i]))


    return np.array(projected_points)

# Define as coordenadas das paredes e chão do cenário


WIDTH, HEIGHT = 800, 600
focal_length = 250


vertices = np.array([
    [-1, -1, -1],
    [-1, -1, 1],
    [-1, 1, -1],
    [-1, 1, 1],
    [1, -1, -1],
    [1, -1, 1],
    [1, 1, -1],
    [1, 1, 1],
])*40
vertices = vertices.T
vertices = np.vstack((vertices, np.ones((1, vertices.shape[1]))))

edges = [
    (0, 1),
    (0, 2),
    (0, 4),
    (1, 3),
    (1, 5),
    (2, 3),
    (2, 6),
    (3, 7),
    (4, 5),
    (4, 6),
    (5, 7),
    (6, 7)
]
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cubo Girando")
clock = pygame.time.Clock()

# Define as constantes de movimentação do jogador
MOVE_SPEED = 3
ROT_SPEED = 2



running = True
angle = 0

# Define a posição inicial e orientação do jogador
player_pos = np.array([0, 0, 0, 1])
player_angle = 0

player_direction = np.array([0, 0, 1, 1])
prev_mouse_pos = None
keys_pressed = {}
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Captura as teclas pressionadas pelo usuário
        if event.type == pygame.KEYDOWN:
            keys_pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            keys_pressed[event.key] = False

    # Atualiza a posição do jogador de acordo com o estado das teclas
    if keys_pressed.get(pygame.K_w):
        if player_direction[2] > -100:
            print(player_direction[2])
            player_direction[2] -= MOVE_SPEED
    elif keys_pressed.get(pygame.K_s):
        player_direction[2] += MOVE_SPEED

    if keys_pressed.get(pygame.K_a):
        player_direction = translation_matrix(-ROT_SPEED,0,0) @ player_direction
    elif keys_pressed.get(pygame.K_d):
        player_direction = translation_matrix(ROT_SPEED,0,0) @ player_direction

        # Captura os movimentos do mouse
    if event.type == pygame.MOUSEMOTION:
        if prev_mouse_pos is not None:
            # Calcula a diferença entre a posição atual e a posição anterior do mouse
            mouse_diff = np.array(pygame.mouse.get_pos()) - prev_mouse_pos
            # Rotaciona o vetor player_direction em torno do eixo y
            player_direction = rotation_matrix_y(-mouse_diff[0]/5) @ player_direction
            # Rotaciona o vetor player_direction em torno do eixo x
            player_direction = rotation_matrix_x(mouse_diff[1]/5) @ player_direction
        prev_mouse_pos = np.array(pygame.mouse.get_pos())

    angle += 1

    rotated_vertices = translation_matrix(player_direction[0], player_direction[1], player_direction[2] + 200) @ rotation_matrix_x(angle) @ rotation_matrix_y(angle + player_angle) @ rotation_matrix_z(angle) @ vertices

    projected_points = project_points(rotated_vertices, focal_length)
    screen.fill((0, 0, 0))

    for point in projected_points:
        pygame.draw.circle(screen, (255, 255, 255), (int(point[0] + WIDTH/2), int(point[1] + HEIGHT/2)), 5)

    for edge in edges:
        start = (projected_points[edge[0]][0] + WIDTH/2, projected_points[edge[0]][1] + HEIGHT/2)
        end = (projected_points[edge[1]][0] + WIDTH/2, projected_points[edge[1]][1] + HEIGHT/2)

        start_z_distance = projected_points[edge[0]][2]
        end_z_distance = projected_points[edge[1]][2]

        grossura_linha = 1/(start_z_distance/1400 + end_z_distance/1400)

        if projected_points[edge[0]][2] > 0 and projected_points[edge[1]][2] > 0:
            pygame.draw.line(screen, (255, 255, 255), start, end, grossura_linha.astype(int))


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
