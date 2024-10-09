# main.py
from grid import Grid
from a_estrela import AEstrela
from renderizador3d import Renderizador3D
from typing import List, Tuple
import time

dimensao = 20

def main():
    print("[Main] Iniciando o programa")
    dimensoes = (dimensao, dimensao, dimensao)
    inicio = (0, 0, 0)
    fim = (dimensao -1, dimensao -1, dimensao -1)

    grid = Grid(dimensoes=dimensoes, inicio=inicio, fim=fim)
    permitir_diagonais = True  # Ativa o movimento diagonal
    a_estrela = AEstrela(grid=grid, permitir_diagonais=permitir_diagonais)
    print("[Main] Iniciando busca com A*")

    tempo_inicio = time.time()
    caminho = a_estrela.buscar()
    tempo_fim = time.time()
    tempo_execucao = tempo_fim - tempo_inicio

    if caminho:
        print(f"[Main] Caminho encontrado com {len(caminho)} passos")
        # Cálculo das estatísticas
        total_nos = dimensoes[0] * dimensoes[1] * dimensoes[2]
        total_obstaculos = len(grid.obstaculos)
        total_livre = total_nos - total_obstaculos
        nos_expandidos = len(a_estrela.nos_expandidos)
        percentual_explorado = (nos_expandidos / total_livre) * 100

        print(f"Tempo de execução: {tempo_execucao:.4f} segundos")
        print(f"Nós expandidos: {nos_expandidos}")
        print(f"Total de nós livres (sem obstáculos): {total_livre}")
        print(f"Percentual do espaço livre explorado: {percentual_explorado:.2f}%")
        print(f"Custo total do caminho: {a_estrela.custo_total}")

        renderizador = Renderizador3D(grid=grid, caminho=caminho, nos_expandidos=a_estrela.nos_expandidos)
        renderizador.executar()
    else:
        print("[Main] Caminho não encontrado.")

if __name__ == "__main__":
    main()
