# camera.py
import numpy as np
import math

class Camera:
    def __init__(self, posicao, olhar_para, cima):
        self.posicao = np.array(posicao, dtype=np.float32)
        self.olhar_para = np.array(olhar_para, dtype=np.float32)
        self.cima = np.array(cima, dtype=np.float32)
        self.velocidade = 0.5
        self.sensibilidade = 1.0
        self.yaw = -90.0
        self.pitch = 0.0
        self.atualizar_vetor_direcao()

    def atualizar_vetor_direcao(self):
        rad_yaw = math.radians(self.yaw)
        rad_pitch = math.radians(self.pitch)
        direcao_x = math.cos(rad_yaw) * math.cos(rad_pitch)
        direcao_y = math.sin(rad_pitch)
        direcao_z = math.sin(rad_yaw) * math.cos(rad_pitch)
        self.direcao = np.array([direcao_x, direcao_y, direcao_z], dtype=np.float32)
        self.direcao = self.direcao / np.linalg.norm(self.direcao)
        self.olhar_para = self.posicao + self.direcao

    def mover(self, direcao):
        if direcao == 'frente':
            self.posicao += self.direcao * self.velocidade
        elif direcao == 'tras':
            self.posicao -= self.direcao * self.velocidade
        elif direcao == 'esquerda':
            lateral = np.cross(self.direcao, self.cima)
            lateral = lateral / np.linalg.norm(lateral)
            self.posicao -= lateral * self.velocidade
        elif direcao == 'direita':
            lateral = np.cross(self.direcao, self.cima)
            lateral = lateral / np.linalg.norm(lateral)
            self.posicao += lateral * self.velocidade
        elif direcao == 'cima':
            self.posicao += self.cima * self.velocidade
        elif direcao == 'baixo':
            self.posicao -= self.cima * self.velocidade
        self.olhar_para = self.posicao + self.direcao

    def rotacionar(self, eixo, angulo):
        if eixo == 'yaw':
            self.yaw += angulo * self.sensibilidade
        elif eixo == 'pitch':
            self.pitch += angulo * self.sensibilidade
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0
        self.atualizar_vetor_direcao()

    def obter_matriz_visao(self):
        return self.look_at(self.posicao, self.olhar_para, self.cima)

    def obter_matriz_projecao(self, largura_tela, altura_tela):
        fov = 45.0
        aspecto = largura_tela / altura_tela
        near = 0.1
        far = 1000.0
        return self.perspective(fov, aspecto, near, far)

    def look_at(self, eye, center, up):
        f = center - eye
        f = f / np.linalg.norm(f)
        u = up / np.linalg.norm(up)
        s = np.cross(f, u)
        s = s / np.linalg.norm(s)
        u = np.cross(s, f)

        matriz = np.identity(4, dtype=np.float32)
        matriz[0][0] = s[0]
        matriz[1][0] = s[1]
        matriz[2][0] = s[2]
        matriz[0][1] = u[0]
        matriz[1][1] = u[1]
        matriz[2][1] = u[2]
        matriz[0][2] = -f[0]
        matriz[1][2] = -f[1]
        matriz[2][2] = -f[2]
        matriz[3][0] = -np.dot(s, eye)
        matriz[3][1] = -np.dot(u, eye)
        matriz[3][2] = np.dot(f, eye)
        return matriz

    def perspective(self, fov, aspecto, near, far):
        fov_rad = math.radians(fov)
        f = 1.0 / math.tan(fov_rad / 2.0)
        matriz = np.zeros((4, 4), dtype=np.float32)
        matriz[0][0] = f / aspecto
        matriz[1][1] = f
        matriz[2][2] = (far + near) / (near - far)
        matriz[2][3] = -1.0
        matriz[3][2] = (2.0 * far * near) / (near - far)
        return matriz
