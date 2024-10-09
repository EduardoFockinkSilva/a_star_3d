# main.py
from grid import Grid
from a_estrela import AEstrela
from renderizador3d import Renderizador3D
from typing import List, Tuple

def main():
    print("[Main] Iniciando o programa")
    dimensoes = (10, 10, 10)
    inicio = (0, 0, 0)
    fim = (9, 9, 9)

    grid = Grid(dimensoes=dimensoes, inicio=inicio, fim=fim)
    a_estrela = AEstrela(grid=grid)
    print("[Main] Iniciando busca com A*")
    caminho = a_estrela.buscar()

    if caminho:
        print(f"[Main] Caminho encontrado com {len(caminho)} passos")
        renderizador = Renderizador3D(grid=grid, caminho=caminho, nos_expandidos=a_estrela.nos_expandidos)
        renderizador.executar()
    else:
        print("[Main] Caminho não encontrado.")

if __name__ == "__main__":
    main()
