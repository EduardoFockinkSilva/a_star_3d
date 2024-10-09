# no.py
from typing import Optional, Tuple

class No:
    def __init__(self, posicao: Tuple[int, int, int], pai: Optional['No'] = None):
        self.posicao: Tuple[int, int, int] = posicao
        self.pai: Optional['No'] = pai
        self.g: float = 0.0  # Custo do início até este nó
        self.h: float = 0.0  # Heurística estimada até o fim
        self.f: float = 0.0  # Custo total (g + h)

    def __eq__(self, outro: object) -> bool:
        if isinstance(outro, No):
            return self.posicao == outro.posicao
        return False

    def __lt__(self, outro: 'No') -> bool:
        return self.f < outro.f
