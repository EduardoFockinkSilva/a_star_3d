# vertices.py
import numpy as np

vertices_cubo = np.array([
    # Posição dos vértices
    # Frente
    [-0.5, -0.5,  0.5],
    [ 0.5, -0.5,  0.5],
    [ 0.5,  0.5,  0.5],
    [-0.5,  0.5,  0.5],
    # Traseira
    [-0.5, -0.5, -0.5],
    [-0.5,  0.5, -0.5],
    [ 0.5,  0.5, -0.5],
    [ 0.5, -0.5, -0.5],
], dtype=np.float32)

indices_cubo = np.array([
    # Frente
    0, 1, 2, 2, 3, 0,
    # Traseira
    4, 5, 6, 6, 7, 4,
    # Lado esquerdo
    4, 0, 3, 3, 5, 4,
    # Lado direito
    1, 7, 6, 6, 2, 1,
    # Superior
    3, 2, 6, 6, 5, 3,
    # Inferior
    4, 7, 1, 1, 0, 4,
], dtype=np.uint32)
