# fabrica_de_obstaculos.py
from typing import List, Tuple
import random

class FabricaDeObstaculos:
    def __init__(self, dimensoes: Tuple[int, int, int], inicio: Tuple[int, int, int], fim: Tuple[int, int, int]):
        self.dimensoes = dimensoes
        self.inicio = inicio
        self.fim = fim

    def gerar_obstaculos(self, quantidade: int) -> List[Tuple[int, int, int]]:
        obstaculos = set()
        x_max, y_max, z_max = self.dimensoes
        while len(obstaculos) < quantidade:
            x = random.randint(0, x_max - 1)
            y = random.randint(0, y_max - 1)
            z = random.randint(0, z_max - 1)
            posicao = (x, y, z)
            if posicao != self.inicio and posicao != self.fim:
                obstaculos.add(posicao)
        return list(obstaculos)
