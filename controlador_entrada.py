# controlador_entrada.py
import pygame
from camera import Camera

class ControladorEntrada:
    def __init__(self, camera: Camera):
        self.camera = camera
        self.rodando = True

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.rodando = False

    def atualizar_camera(self):
        teclas = pygame.key.get_pressed()
        # Movimentação
        if teclas[pygame.K_w]:
            self.camera.mover('frente')
        if teclas[pygame.K_s]:
            self.camera.mover('tras')
        if teclas[pygame.K_d]:
            self.camera.mover('esquerda')
        if teclas[pygame.K_a]:
            self.camera.mover('direita')
        if teclas[pygame.K_q]:
            self.camera.mover('cima')
        if teclas[pygame.K_e]:
            self.camera.mover('baixo')
        # Rotação
        if teclas[pygame.K_i]:
            self.camera.rotacionar('pitch', 1)  # Olhar para cima
        if teclas[pygame.K_k]:
            self.camera.rotacionar('pitch', -1)  # Olhar para baixo
        if teclas[pygame.K_j]:
            self.camera.rotacionar('yaw', -1)  # Olhar para esquerda
        if teclas[pygame.K_l]:
            self.camera.rotacionar('yaw', 1)   # Olhar para direita
        if teclas[pygame.K_u]:
            pass  # Opcional: Rotação em torno do eixo Z (roll)
        if teclas[pygame.K_o]:
            pass  # Opcional: Rotação em torno do eixo Z (roll)
