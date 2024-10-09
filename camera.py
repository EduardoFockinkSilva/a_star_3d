# camera.py
from typing import List
import math

class Camera:
    def __init__(self, posicao: List[float], olhar_para: List[float], cima: List[float]):
        self.posicao = posicao      # Posição da câmera [x, y, z]
        self.olhar_para = olhar_para  # Ponto para onde a câmera está olhando [x, y, z]
        self.cima = cima            # Vetor "up" da câmera [x, y, z]
        self.velocidade = 0.5       # Velocidade de movimento da câmera
        self.atualizar_vetor_direcao()
        print(f"[Camera] Inicializada com posição {self.posicao} e olhando para {self.olhar_para}")

    def atualizar_vetor_direcao(self):
        self.direcao = [
            self.olhar_para[0] - self.posicao[0],
            self.olhar_para[1] - self.posicao[1],
            self.olhar_para[2] - self.posicao[2]
        ]
        magnitude = math.sqrt(sum([d ** 2 for d in self.direcao]))
        if magnitude != 0:
            self.direcao = [d / magnitude for d in self.direcao]
        else:
            self.direcao = [0.0, 0.0, -1.0]
        print(f"[Camera] Vetor direção atualizado: {self.direcao}")

    def mover(self, direcao: str):
        print(f"[Camera] Movendo câmera para {direcao}")
        if direcao == 'frente':
            for i in range(3):
                self.posicao[i] += self.direcao[i] * self.velocidade
                self.olhar_para[i] += self.direcao[i] * self.velocidade
        elif direcao == 'tras':
            for i in range(3):
                self.posicao[i] -= self.direcao[i] * self.velocidade
                self.olhar_para[i] -= self.direcao[i] * self.velocidade
        elif direcao == 'esquerda':
            # Movimento lateral (produto vetorial entre direção e vetor cima)
            lateral = [
                self.cima[1]*self.direcao[2] - self.cima[2]*self.direcao[1],
                self.cima[2]*self.direcao[0] - self.cima[0]*self.direcao[2],
                self.cima[0]*self.direcao[1] - self.cima[1]*self.direcao[0]
            ]
            magnitude = math.sqrt(sum([l ** 2 for l in lateral]))
            if magnitude != 0:
                lateral = [l / magnitude for l in lateral]
            for i in range(3):
                self.posicao[i] -= lateral[i] * self.velocidade
                self.olhar_para[i] -= lateral[i] * self.velocidade
        elif direcao == 'direita':
            lateral = [
                self.cima[1]*self.direcao[2] - self.cima[2]*self.direcao[1],
                self.cima[2]*self.direcao[0] - self.cima[0]*self.direcao[2],
                self.cima[0]*self.direcao[1] - self.cima[1]*self.direcao[0]
            ]
            magnitude = math.sqrt(sum([l ** 2 for l in lateral]))
            if magnitude != 0:
                lateral = [l / magnitude for l in lateral]
            for i in range(3):
                self.posicao[i] += lateral[i] * self.velocidade
                self.olhar_para[i] += lateral[i] * self.velocidade
        elif direcao == 'cima':
            for i in range(3):
                self.posicao[i] += self.cima[i] * self.velocidade
                self.olhar_para[i] += self.cima[i] * self.velocidade
        elif direcao == 'baixo':
            for i in range(3):
                self.posicao[i] -= self.cima[i] * self.velocidade
                self.olhar_para[i] -= self.cima[i] * self.velocidade
        self.atualizar_vetor_direcao()
        print(f"[Camera] Posição atual: {self.posicao}, Olhando para: {self.olhar_para}")

    def atualizar_velocidade(self, nova_velocidade: float):
        self.velocidade = nova_velocidade
        print(f"[Camera] Velocidade atualizada para {self.velocidade}")
