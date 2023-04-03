# 3D cube projection project
## projeção de cubo 

<img src="3d_cube.gif" width=500>


### Introdução  
Este programa utiliza a biblioteca pygame e numpy para realizar uma rotação de cubo tridimensional e projetar para a tela.

### Equações implementadas  
Matrizes e equações em seu funcionamento:

Matriz de rotação:  
São utilizadas matrizes de rotação com 4 dimensões, para garantir a possibilidade de rotacionar o cubo nas 3 dimensões e a última dimensão permite translações, tópico da próxima seção. Como o cubo é criado na origem dos espaços (0,0,0), as operações de rotação foram aplicadas diretamente. Segue abaixo as matrizes usadas:

$$
R_x = \begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & \cos(\theta) & -\sin(\theta) & 0 \\
0 & \sin(\theta) & \cos(\theta) & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\hspace{0.5in}
R_y = \begin{bmatrix}
\cos(\theta) & 0 & \sin(\theta) & 0 \\
0 & 1 & 0 & 0 \\
-\sin(\theta) & 0 & \cos(\theta) & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\hspace{0.5in}
R_z = \begin{bmatrix}
\cos(\theta) & - \sin(\theta) & 0 & 0 \\
\sin(\theta) & \cos(\theta) & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

Matriz de translação:  
A matriz de translação permite movimentar o cubo no espaço, além de possibilitar o afastamento dele o suficiente para que esteja na frente da camêra. A matriz 

$$
T = \begin{bmatrix}
1 & 0 & 0 & dx \\
0 & 1 & 0 & dy \\
0 & 0 & 1 & dz \\
0 & 0 & 0 & 1
\end{bmatrix}  
\hspace{0.5in}
$$

Matriz de projeção (3D para 2D):  
Para realizar a projeção das coordenadas em 3D do cubo, foi utilizada uma matriz de projeção...
$$
P = \begin{bmatrix}
0 & 0 & 0 & -d \\
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & -1/d & 0
\end{bmatrix}  
\hspace{0.5in}
$$


### Como usar?
Para rodar o programa, execute o arquivo main.py. As teclas abaixo podem ser usadas para realizar as seguintes ações:

ESC: encerra o programa.  
a: translada o cubo para a direita (como se o "jogador" se movimentasse para esquerda).   
d: translada o cubo para a esquerda.  
w: decrementa a distância do cubo.  
s: incrementa a distância do cubo.  


### Como instalar?  
Para garantir o funcionamento da aplicação é recomedado a criação de um ambiente virtual (venv) para instalar as dependência, como apresentado em https://docs.python.org/3/library/venv.html. Após a criação do ambiente, realizar a instalação das bibliotecas numpy e pygame, com os seguintes comandos do terminal:  
pip install numpy  
pip install pygame

Protinho agora é só rodar o arquivo, através do comando python/python3 main.py ou sua IDE python de preferência.