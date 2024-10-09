# a_estrela.py
from typing import List, Tuple, Set, Dict
import heapq
import math
from no import No  # Suponho que a classe No gerencie estados ou posições no grid.
from grid import Grid  # A classe Grid representa o espaço tridimensional onde o algoritmo opera.

class AEstrela:
    def __init__(self, grid: Grid, permitir_diagonais: bool = False):
        # Inicializa a instância com o grid e uma flag para permitir ou não movimentação diagonal
        self.grid = grid
        self.permitir_diagonais = permitir_diagonais
        self.nos_expandidos: Set[Tuple[int, int, int]] = set()  # Conjunto para armazenar nós visitados
        self.custo_total: float = 0.0  # Armazena o custo total do caminho encontrado

        # Definindo os movimentos possíveis em um grid tridimensional (6 direções principais)
        self.movimentos = [(-1, 0, 0), (1, 0, 0),
                           (0, -1, 0), (0, 1, 0),
                           (0, 0, -1), (0, 0, 1)]
        if self.permitir_diagonais:
            # Adiciona movimentos diagonais (26 direções adicionais) caso permitido
            movimentos_diagonais = [
                (-1, -1, 0), (-1, 1, 0), (1, -1, 0), (1, 1, 0),
                (-1, 0, -1), (-1, 0, 1), (1, 0, -1), (1, 0, 1),
                (0, -1, -1), (0, -1, 1), (0, 1, -1), (0, 1, 1),
                (-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (-1, 1, 1),
                (1, -1, -1), (1, -1, 1), (1, 1, -1), (1, 1, 1)
            ]
            self.movimentos.extend(movimentos_diagonais)  # Adiciona à lista de movimentos

    def heuristica(self, posicao_atual: Tuple[int, int, int], posicao_fim: Tuple[int, int, int]) -> float:
        # Função que calcula a heurística usando a distância Euclidiana
        x1, y1, z1 = posicao_atual
        x2, y2, z2 = posicao_fim
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)

    def obter_vizinhos(self, posicao_atual: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
        # Retorna os vizinhos válidos (que não são obstáculos e estão dentro dos limites do grid)
        vizinhos = []
        x, y, z = posicao_atual
        for dx, dy, dz in self.movimentos:
            nx, ny, nz = x + dx, y + dy, z + dz
            # Verifica se a posição vizinha está dentro dos limites do grid
            if (0 <= nx < self.grid.dimensoes[0] and
                0 <= ny < self.grid.dimensoes[1] and
                0 <= nz < self.grid.dimensoes[2]):
                if (nx, ny, nz) not in self.grid.obstaculos:  # Verifica se não é um obstáculo
                    vizinhos.append((nx, ny, nz))
        return vizinhos

    def custo_movimento(self, posicao_atual: Tuple[int, int, int], posicao_vizinho: Tuple[int, int, int]) -> float:
        # Calcula o custo de movimento usando a distância Euclidiana entre posições
        dx = abs(posicao_atual[0] - posicao_vizinho[0])
        dy = abs(posicao_atual[1] - posicao_vizinho[1])
        dz = abs(posicao_atual[2] - posicao_vizinho[2])
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def buscar(self) -> List[Tuple[int, int, int]]:
        print("[AEstrela] Iniciando busca...")
        inicio = self.grid.inicio  # Ponto inicial do caminho
        fim = self.grid.fim  # Ponto final do caminho

        # Inicializa a lista aberta como uma fila de prioridade (usando heapq)
        lista_aberta: List[Tuple[float, Tuple[int, int, int]]] = []
        heapq.heappush(lista_aberta, (0.0, inicio))

        # Dicionários para guardar o custo acumulado até o momento e o caminho
        custo_ate_agora: Dict[Tuple[int, int, int], float] = {inicio: 0.0}
        came_from: Dict[Tuple[int, int, int], Tuple[int, int, int]] = {}

        while lista_aberta:
            _, atual = heapq.heappop(lista_aberta)
            self.nos_expandidos.add(atual)  # Marca o nó como visitado

            if atual == fim:
                print("[AEstrela] Caminho encontrado!")
                self.custo_total = custo_ate_agora[atual]
                return self.reconstruir_caminho(came_from, atual)  # Reconstrói o caminho encontrado

            for vizinho in self.obter_vizinhos(atual):
                novo_custo = custo_ate_agora[atual] + self.custo_movimento(atual, vizinho)

                # Se o vizinho não foi visitado ou o novo custo é menor, atualiza as informações
                if vizinho not in custo_ate_agora or novo_custo < custo_ate_agora[vizinho]:
                    custo_ate_agora[vizinho] = novo_custo
                    prioridade = novo_custo + self.heuristica(vizinho, fim)
                    heapq.heappush(lista_aberta, (prioridade, vizinho))
                    came_from[vizinho] = atual

        print("[AEstrela] Caminho não encontrado.")
        return []  # Retorna uma lista vazia se não há caminho

    def reconstruir_caminho(self, came_from: Dict[Tuple[int, int, int], Tuple[int, int, int]], atual: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
        # Reconstrói o caminho do ponto final até o inicial
        caminho = [atual]
        while atual in came_from:
            atual = came_from[atual]
            caminho.append(atual)
        caminho_invertido = caminho[::-1]  # Inverte a lista para obter o caminho do início ao fim
        print(f"[AEstrela] Caminho reconstruído: {caminho_invertido}")
        return caminho_invertido
