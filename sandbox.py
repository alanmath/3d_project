import pygame
import numpy as np


def rotation_matrix_x(angle):
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle), -np.sin(angle), 0],
        [0, np.sin(angle), np.cos(angle), 0], 
        [0, 0, 0, 1]
    ])

def rotation_matrix_y(angle):
    return np.array([
        [np.cos(angle), 0, np.sin(angle), 0],
        [0, 1, 0, 0],
        [-np.sin(angle), 0, np.cos(angle), 0], 
        [0, 0, 0, 1]
    ])

def rotation_matrix_z(angle):
    return np.array([
        [np.cos(angle), -np.sin(angle), 0, 0],
        [np.sin(angle), np.cos(angle), 0, 0],
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
    transformation_matrix = np.array([
        [focal_length, 0, 0, 0],
        [0, focal_length, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    matrix_wp = transformation_matrix @ points
    projected_points = []
    for point in matrix_wp.T:
        w = point[2]
        projected_points.append((point[0] / w, point[1] / w))

    return np.array(projected_points)



WIDTH, HEIGHT = 800, 600
focal_length = 100


vertices = np.array([
    [-1, -1, -1],
    [-1, -1, 1],
    [-1, 1, -1],
    [-1, 1, 1],
    [1, -1, -1],
    [1, -1, 1],
    [1, 1, -1],
    [1, 1, 1],
]) * 100
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

running = True
angle = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    angle += 0.001
    rotated_vertices = translation_matrix(700, 500, 0) @ rotation_matrix_z(angle) @ rotation_matrix_y(angle) @ rotation_matrix_x(angle) @ vertices

    projected_points = project_points(rotated_vertices, focal_length)
    # print(projected_points)
    screen.fill((0, 0, 0))

    for edge in edges:
        start = projected_points[edge[0]]
        end = projected_points[edge[1]]
        pygame.draw.line(screen, (255, 255, 255), start, end, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
