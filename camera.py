# camera.py
from typing import List
import math

class Camera:
    def __init__(self, posicao: List[float], olhar_para: List[float], cima: List[float]):
        self.posicao = posicao      # Posição da câmera [x, y, z]
        self.olhar_para = olhar_para  # Ponto para onde a câmera está olhando [x, y, z]
        self.cima = cima            # Vetor "up" da câmera [x, y, z]
        self.velocidade = 0.3       # Velocidade de movimento da câmera
        self.sensibilidade = 0.4   # Sensibilidade da rotação
        self.yaw = 0.0              # Rotação em torno do eixo Y
        self.pitch = 0.0            # Rotação em torno do eixo X
        self.atualizar_vetor_direcao()

    def atualizar_vetor_direcao(self):
        # Calcula o vetor direção baseado nos ângulos yaw e pitch
        direcao_x = math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        direcao_y = math.sin(math.radians(self.pitch))
        direcao_z = math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        self.direcao = [direcao_x, direcao_y, direcao_z]
        # Atualiza o ponto para onde a câmera está olhando
        self.olhar_para = [
            self.posicao[0] + self.direcao[0],
            self.posicao[1] + self.direcao[1],
            self.posicao[2] + self.direcao[2]
        ]

    def mover(self, direcao: str):
        if direcao == 'frente':
            for i in range(3):
                self.posicao[i] += self.direcao[i] * self.velocidade
        elif direcao == 'tras':
            for i in range(3):
                self.posicao[i] -= self.direcao[i] * self.velocidade
        elif direcao == 'esquerda':
            # Produto vetorial entre vetor direção e vetor cima
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
        elif direcao == 'cima':
            for i in range(3):
                self.posicao[i] += self.cima[i] * self.velocidade
        elif direcao == 'baixo':
            for i in range(3):
                self.posicao[i] -= self.cima[i] * self.velocidade
        self.atualizar_vetor_direcao()

    def rotacionar(self, eixo: str, angulo: float):
        if eixo == 'yaw':
            self.yaw += angulo * self.sensibilidade
        elif eixo == 'pitch':
            self.pitch += angulo * self.sensibilidade
            # Limita o pitch para evitar gimbal lock
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0
        self.atualizar_vetor_direcao()

    def atualizar_velocidade(self, nova_velocidade: float):
        self.velocidade = nova_velocidade
