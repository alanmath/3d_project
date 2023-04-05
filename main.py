import pygame
import numpy as np

# This function returns a 4x4 rotation matrix around the x-axis given an angle in degrees.
def rotation_matrix_x(angle):
    """
    :param angle: Rotation angle in degrees.
    :return: A 4x4 rotation matrix around the x-axis.
    """
    angulo_em_radianos = np.radians(angle)
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(angulo_em_radianos), -np.sin(angulo_em_radianos), 0],
        [0, np.sin(angulo_em_radianos), np.cos(angulo_em_radianos), 0], 
        [0, 0, 0, 1]
    ])

# This function returns a 4x4 rotation matrix around the y-axis given an angle in degrees.
def rotation_matrix_y(angle):
    """
    :param angle: Rotation angle in degrees.
    :return: A 4x4 rotation matrix around the y-axis.
    """
    angulo_em_radianos = np.radians(angle)
    return np.array([
        [np.cos(angulo_em_radianos), 0, np.sin(angulo_em_radianos), 0],
        [0, 1, 0, 0],
        [-np.sin(angulo_em_radianos), 0, np.cos(angulo_em_radianos), 0], 
        [0, 0, 0, 1]
    ])

# This function returns a 4x4 rotation matrix around the z-axis given an angle in degrees.
def rotation_matrix_z(angle):
    """
    :param angle: Rotation angle in degrees.
    :return: A 4x4 rotation matrix around the z-axis.
    """
    angulo_em_radianos = np.radians(angle)
    return np.array([
        [np.cos(angulo_em_radianos), -np.sin(angulo_em_radianos), 0, 0],
        [np.sin(angulo_em_radianos), np.cos(angulo_em_radianos), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

# This function returns a 4x4 translation matrix given x, y, and z coordinates.
def translation_matrix(x, y, z):
    """
    :param x: Translation in the x-axis.
    :param y: Translation in the y-axis.
    :param z: Translation in the z-axis.
    :return: A 4x4 translation matrix.
    """
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])


def project_points(points, focal_length):
    """
    :param points: A 3xN array of 3D points.
    :param focal_length: The focal length of the camera.
    :return: A Nx3 array of 2D projected points.
    """
    transformation_matrix = np.array([[0,0,0,-focal_length], [1,0,0,0], [0,1,0,0], [0,0,-1/focal_length,0]])
    matrix_wp = transformation_matrix @ points
    projected_points = []
    for i,point in enumerate(matrix_wp.T):
        w = point[3]
        if points[2][i] > 0:

            projected_points.append((point[1]/w, point[2]/w, points[2][i]))
        else:
            projected_points.append((0, 0, 0))


    return np.array(projected_points)

# Define as coordenadas das paredes e chão do cenário
WIDTH, HEIGHT = 800, 600
focal_length = 250

# Define as coordenadas dos vértices do cubo de aresta 2*40 centrado na origem.
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

# Define as arestas do cubo (cada aresta é definida por dois indices de vértices)
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
# Initialize pygame and create a window with dimensions WIDTH x HEIGHT.
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the title of the window.
pygame.display.set_caption("Cubo Girando")

# Create a clock object to control the framerate of the game.
clock = pygame.time.Clock()

# Define the movement speed and rotation speed of the player.
MOVE_SPEED = 3
ROT_SPEED = 2

# Set running to True to start the game loop.
running = True

# Initialize the angle variable to 0.
angle = 0

# Define the initial position and orientation of the player.
player_pos = np.array([0, 0, 0, 1])
player_angle = 0

# Define the initial direction of the player.
player_position = np.array([0, 0, 1, 1])
player_direction = np.array([0, 0, 1, 1])

# Initialize prev_mouse_pos to None.
prev_mouse_pos = None

# Initialize the keys_pressed dictionary to an empty dictionary.
keys_pressed = {}

actual_angle_rotation = 0

# Start the game loop.
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Captura as teclas pressionadas pelo usuário
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            keys_pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            keys_pressed[event.key] = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: 
                focal_length += 10
               
            elif event.button == 5:
                if focal_length > 10:
                    focal_length -= 10


    # Atualiza a posição do jogador de acordo com o estado das teclas
    if keys_pressed.get(pygame.K_w):
         ## verfica se o cubo já está muito próximo da "câmera"
        player_position[2] -= MOVE_SPEED
    elif keys_pressed.get(pygame.K_s):
        player_position[2] += MOVE_SPEED

    if keys_pressed.get(pygame.K_a):
        player_position[0] -= MOVE_SPEED
    elif keys_pressed.get(pygame.K_d):
        player_position[0] += MOVE_SPEED
    
    if keys_pressed.get(pygame.K_e):
        actual_angle_rotation += 0.2
    elif keys_pressed.get(pygame.K_q):
        actual_angle_rotation -= 0.2


        # Captura os movimentos do mouse
    if event.type == pygame.MOUSEMOTION:
        if prev_mouse_pos is not None:
            # Calcula a diferença entre a posição atual e a posição anterior do mouse
            
            mouse_diff = np.array(pygame.mouse.get_pos()) - prev_mouse_pos
            # Rotaciona o vetor player_position em torno do eixo y
            player_direction[1] += mouse_diff[0]/3
            # Rotaciona o vetor player_position em torno do eixo x
            player_direction[0] -= mouse_diff[1]/3
        prev_mouse_pos = np.array(pygame.mouse.get_pos())

    # Incrementa o angulo de rotação do cubo
    angle += actual_angle_rotation



    # Apply rotations and translations to the vertices of the cube to simulate its movement.
    rotate =   (rotation_matrix_x(player_direction[0]) @ rotation_matrix_y(player_direction[1]) )


    rotated_vertices = rotate @ translation_matrix(player_position[0],0, player_position[2]) @ translation_matrix(0, 0, 200) @ rotation_matrix_x(angle) @ rotation_matrix_y(angle) @ rotation_matrix_z(angle) @ vertices
    

    # Project the vertices onto a 2D plane using the pinhole camera model.
    projected_points = project_points(rotated_vertices, focal_length)

    # Fill the screen with black.
    screen.fill((0, 0, 0))

    # Draw lines between the projected points to create the wireframe of the cube.
    for edge in edges:
        # Get the start and end points of the edge in 2D space.
        start = (projected_points[edge[0]][0] + WIDTH/2, projected_points[edge[0]][1] + HEIGHT/2)
        end = (projected_points[edge[1]][0] + WIDTH/2, projected_points[edge[1]][1] + HEIGHT/2)

        # Calculate the distance of the start and end points from the camera (along the z-axis).
        start_z_distance = projected_points[edge[0]][2]
        end_z_distance = projected_points[edge[1]][2]

        # Calculate the thickness of the line based on the distance of the start and end points from the camera.
        grossura_linha = 1/(start_z_distance/1400 + end_z_distance/1400)

        # Only draw the line if both the start and end points are in front of the camera.
        if projected_points[edge[0]][2] > 0 and projected_points[edge[1]][2] > 0 and grossura_linha <30:
            pygame.draw.line(screen, (255, 255, 255), start, end, grossura_linha.astype(int))
        
    # Update the display and limit the framerate to 60 FPS.
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
