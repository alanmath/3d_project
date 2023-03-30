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
    transformation_matrix = np.array([[0,0,0,-focal_length], [1,0,0,0], [0,1,0,0], [0,0,-1/focal_length,0]])
    matrix_wp = transformation_matrix @ points
    print(matrix_wp)
    projected_points = []
    for point in matrix_wp.T:
        w = point[3]
        projected_points.append((point[1]/w, point[2]/w))


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
])*100
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

    angle += 0.005
    rotated_vertices = translation_matrix(0, 0, 200) @ rotation_matrix_x(angle)  @ rotation_matrix_y(angle) @ rotation_matrix_z(angle) @ vertices

    projected_points = project_points(rotated_vertices, focal_length)
    # print(projected_points)
    screen.fill((0, 0, 0))

    for edge in edges:
        start = (projected_points[edge[0]][0] + WIDTH/2, projected_points[edge[0]][1] + HEIGHT/2)
        end = (projected_points[edge[1]][0] + WIDTH/2, projected_points[edge[1]][1] + HEIGHT/2)
        pygame.draw.line(screen, (255, 255, 255), start, end, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
