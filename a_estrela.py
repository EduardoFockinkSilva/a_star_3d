# a_estrela.py
from typing import List, Tuple, Set
import heapq
import math
from no import No
from grid import Grid

class AEstrela:
    def __init__(self, grid: Grid, permitir_diagonais: bool = False):
        self.grid = grid
        self.permitir_diagonais = permitir_diagonais
        self.nos_expandidos: Set[Tuple[int, int, int]] = set()  # Para armazenar os nós visitados
        self.custo_total: float = 0.0  # Custo total do caminho encontrado

    def heuristica(self, posicao_atual: Tuple[int, int, int], posicao_fim: Tuple[int, int, int]) -> float:
        x1, y1, z1 = posicao_atual
        x2, y2, z2 = posicao_fim
        if self.permitir_diagonais:
            # Distância Chebyshev
            return max(abs(x1 - x2), abs(y1 - y2), abs(z1 - z2))
        else:
            # Distância Manhattan
            return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

    def obter_vizinhos(self, no_atual: No) -> List[No]:
        vizinhos = []
        x, y, z = no_atual.posicao
        movimentos = [(-1, 0, 0), (1, 0, 0),
                      (0, -1, 0), (0, 1, 0),
                      (0, 0, -1), (0, 0, 1)]
        if self.permitir_diagonais:
            movimentos_diagonais = [
                (-1, -1, 0), (-1, 1, 0), (1, -1, 0), (1, 1, 0),
                (-1, 0, -1), (-1, 0, 1), (1, 0, -1), (1, 0, 1),
                (0, -1, -1), (0, -1, 1), (0, 1, -1), (0, 1, 1),
                (-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (-1, 1, 1),
                (1, -1, -1), (1, -1, 1), (1, 1, -1), (1, 1, 1)
            ]
            movimentos.extend(movimentos_diagonais)

        for dx, dy, dz in movimentos:
            nx, ny, nz = x + dx, y + dy, z + dz
            if (0 <= nx < self.grid.dimensoes[0] and
                0 <= ny < self.grid.dimensoes[1] and
                0 <= nz < self.grid.dimensoes[2]):
                if (nx, ny, nz) not in self.grid.obstaculos:
                    vizinhos.append(No(posicao=(nx, ny, nz)))
        return vizinhos

    def custo_movimento(self, posicao_atual: Tuple[int, int, int], posicao_vizinho: Tuple[int, int, int]) -> float:
        dx = abs(posicao_atual[0] - posicao_vizinho[0])
        dy = abs(posicao_atual[1] - posicao_vizinho[1])
        dz = abs(posicao_atual[2] - posicao_vizinho[2])
        if self.permitir_diagonais:
            # Custo Euclidiano para movimentos diagonais
            return math.sqrt(dx * dx + dy * dy + dz * dz)
        else:
            return 1  # Custo de 1 para movimentos ortogonais

    def buscar(self) -> List[Tuple[int, int, int]]:
        print("[AEstrela] Iniciando busca...")
        no_inicio = No(posicao=self.grid.inicio)
        no_fim = No(posicao=self.grid.fim)

        lista_aberta: List[No] = []
        conjunto_fechado: Set[Tuple[int, int, int]] = set()
        heapq.heappush(lista_aberta, no_inicio)

        while lista_aberta:
            no_atual = heapq.heappop(lista_aberta)
            conjunto_fechado.add(no_atual.posicao)
            self.nos_expandidos.add(no_atual.posicao)

            if no_atual == no_fim:
                print("[AEstrela] Caminho encontrado!")
                self.custo_total = no_atual.g
                return self.reconstruir_caminho(no_atual)

            vizinhos = self.obter_vizinhos(no_atual)
            for vizinho in vizinhos:
                if vizinho.posicao in conjunto_fechado:
                    continue

                custo_mov = self.custo_movimento(no_atual.posicao, vizinho.posicao)
                vizinho.g = no_atual.g + custo_mov
                vizinho.h = self.heuristica(vizinho.posicao, no_fim.posicao)
                vizinho.f = vizinho.g + vizinho.h
                vizinho.pai = no_atual

                # Verifica se o vizinho já está na lista aberta com um custo menor
                na_lista_aberta = False
                for no_aberto in lista_aberta:
                    if vizinho == no_aberto and vizinho.g >= no_aberto.g:
                        na_lista_aberta = True
                        break

                if not na_lista_aberta:
                    heapq.heappush(lista_aberta, vizinho)

        print("[AEstrela] Caminho não encontrado.")
        return []  # Caminho não encontrado

    def reconstruir_caminho(self, no_atual: No) -> List[Tuple[int, int, int]]:
        caminho = []
        while no_atual:
            caminho.append(no_atual.posicao)
            no_atual = no_atual.pai
        caminho_invertido = caminho[::-1]  # Inverte o caminho
        print(f"[AEstrela] Caminho reconstruído: {caminho_invertido}")
        return caminho_invertido
