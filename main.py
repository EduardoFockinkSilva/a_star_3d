# main.py
from grid import Grid
from a_estrela import AEstrela
from renderizador3d import Renderizador3D
from typing import List, Tuple
import random

def main():
    print("[Main] Iniciando o programa")
    dimensoes = (10, 10, 10)
    # Exemplo de obstáculos aleatórios
    obstaculos: List[Tuple[int, int, int]] = []
    for _ in range(200):
        x = random.randint(0, dimensoes[0] - 1)
        y = random.randint(0, dimensoes[1] - 1)
        z = random.randint(0, dimensoes[2] - 1)
        obstaculos.append((x, y, z))
    inicio = (0, 0, 0)
    fim = (9, 9, 9)

    grid = Grid(dimensoes=dimensoes, obstaculos=obstaculos, inicio=inicio, fim=fim)
    a_estrela = AEstrela(grid=grid)
    print("[Main] Iniciando busca com A*")
    caminho = a_estrela.buscar()

    if caminho:
        print(f"[Main] Caminho encontrado com {len(caminho)} passos")
        renderizador = Renderizador3D(grid=grid, caminho=caminho)
        renderizador.executar()
    else:
        print("[Main] Caminho não encontrado.")

if __name__ == "__main__":
    main()
