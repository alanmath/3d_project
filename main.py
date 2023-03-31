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
    for point in matrix_wp.T:
        w = point[3]
        projected_points.append((point[1]/w, point[2]/w))


    return np.array(projected_points)


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
MOVE_SPEED = 5
ROT_SPEED = 2

# Define a posição inicial e orientação do jogador
player_pos = np.array([0, 0, 0])
player_angle = 0

running = True
angle = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Captura as teclas pressionadas pelo usuário
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                # Move o jogador para frente
                focal_length += 10
            elif event.key == pygame.K_s:
                # Move o jogador para trás
                focal_length -= 10

            elif event.key == pygame.K_a:
                # Rotaciona o jogador para a esquerda
                player_angle += ROT_SPEED
            elif event.key == pygame.K_d:
                # Rotaciona o jogador para a direita
                player_angle -= ROT_SPEED

    angle += 0.0
    rotated_vertices = translation_matrix(player_pos[0], player_pos[1], player_pos[2] + 200) @ rotation_matrix_x(angle) @ rotation_matrix_y(angle + player_angle) @ rotation_matrix_z(angle) @ vertices

    projected_points = project_points(rotated_vertices, focal_length)
    screen.fill((0, 0, 0))

    for point in projected_points:
        pygame.draw.circle(screen, (255, 255, 255), (int(point[0] + WIDTH/2), int(point[1] + HEIGHT/2)), 5)

    for edge in edges:
        start = (projected_points[edge[0]][0] + WIDTH/2, projected_points[edge[0]][1] + HEIGHT/2)
        end = (projected_points[edge[1]][0] + WIDTH/2, projected_points[edge[1]][1] + HEIGHT/2)
        pygame.draw.line(screen, (255, 255, 255), start, end, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()