# a_estrela.py
from typing import List, Tuple, Set, Dict
import heapq
from no import No
from grid import Grid

class AEstrela:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.nos_expandidos: Set[Tuple[int, int, int]] = set()  # Para armazenar os nós visitados

    def heuristica(self, posicao_atual: Tuple[int, int, int], posicao_fim: Tuple[int, int, int]) -> float:
        # Distância Euclidiana
        x1, y1, z1 = posicao_atual
        x2, y2, z2 = posicao_fim
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** 0.5

    def obter_vizinhos(self, no_atual: No) -> List[No]:
        vizinhos = []
        x, y, z = no_atual.posicao
        movimentos = [(-1, 0, 0), (1, 0, 0),
                      (0, -1, 0), (0, 1, 0),
                      (0, 0, -1), (0, 0, 1)]
        for dx, dy, dz in movimentos:
            nx, ny, nz = x + dx, y + dy, z + dz
            if (0 <= nx < self.grid.dimensoes[0] and
                0 <= ny < self.grid.dimensoes[1] and
                0 <= nz < self.grid.dimensoes[2]):
                if (nx, ny, nz) not in self.grid.obstaculos:
                    vizinhos.append(No(posicao=(nx, ny, nz)))
        return vizinhos

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
                return self.reconstruir_caminho(no_atual)

            vizinhos = self.obter_vizinhos(no_atual)
            for vizinho in vizinhos:
                if vizinho.posicao in conjunto_fechado:
                    continue

                vizinho.g = no_atual.g + 1
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
