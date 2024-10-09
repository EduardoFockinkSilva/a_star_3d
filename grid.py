# grid.py
from typing import List, Tuple, Set, Optional
from fabrica_de_obstaculos import FabricaDeObstaculos

class Grid:
    def __init__(self, dimensoes: Tuple[int, int, int], inicio: Tuple[int, int, int], fim: Tuple[int, int, int], obstaculos: Optional[List[Tuple[int, int, int]]] = None):
        self.dimensoes: Tuple[int, int, int] = dimensoes
        self.inicio: Tuple[int, int, int] = inicio
        self.fim: Tuple[int, int, int] = fim

        # Validação dos pontos
        self.validar_ponto(inicio)
        self.validar_ponto(fim)

        # Geração dos obstáculos
        if obstaculos is None:
            fabrica = FabricaDeObstaculos(dimensoes, inicio, fim)
            quantidade_obstaculos = (dimensoes[0] * dimensoes[1] * dimensoes[2]) // 4  # 25% do grid
            obstaculos = fabrica.gerar_obstaculos(quantidade_obstaculos)
        self.obstaculos: Set[Tuple[int, int, int]] = set(obstaculos)
        self.validar_obstaculos()
        print(f"[Grid] Grid criado com dimensões {self.dimensoes}, início em {self.inicio}, fim em {self.fim}, com {len(self.obstaculos)} obstáculos")

    def validar_ponto(self, ponto: Tuple[int, int, int]):
        x, y, z = ponto
        x_max, y_max, z_max = self.dimensoes
        if not (0 <= x < x_max and 0 <= y < y_max and 0 <= z < z_max):
            raise ValueError(f"Ponto {ponto} está fora das dimensões do grid.")

    def validar_obstaculos(self):
        if self.inicio in self.obstaculos:
            raise ValueError("O ponto inicial não pode ser um obstáculo.")
        if self.fim in self.obstaculos:
            raise ValueError("O ponto final não pode ser um obstáculo.")
