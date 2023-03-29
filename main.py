import pygame
import numpy as np


def rotation_matrix_x(angle):
    return np.array([
        [1, 0, 0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle), np.cos(angle)]
    ])

def rotation_matrix_y(angle):
    return np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])

def rotation_matrix_z(angle):
    return np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])

def project_points(points, focal_length):
    transformation_matrix = np.array([[0,0,0,-focal_length], [1,0,0,0], [0,1,0,0], [0,0,-1/focal_length,0]])
    
    

    projected_points = np.zeros((points.shape[0], 2))
    for i, point in enumerate(points):
        projected_point_x = (point[i].T@transformation_matrix)[1][0]
        projected_point_y = (point[i].T@transformation_matrix)[2][0]



    return projected_points


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

    angle += 0.00
    rotated_vertices = vertices.dot(rotation_matrix_x(angle)).dot(rotation_matrix_y(angle)).dot(rotation_matrix_z(angle))

    projected_points = project_points(rotated_vertices, focal_length)

    screen.fill((0, 0, 0))

    for edge in edges:
        start = projected_points[edge[0]]
        end = projected_points[edge[1]]
        pygame.draw.line(screen, (255, 255, 255), start, end, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
