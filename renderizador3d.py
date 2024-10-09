# renderizador3d.py
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from typing import List, Tuple
from grid import Grid
from camera import Camera
from controlador_entrada import ControladorEntrada

class Renderizador3D:
    def __init__(self, grid: Grid, caminho: List[Tuple[int, int, int]]):
        self.grid = grid
        self.caminho = caminho
        self.largura_tela = 800
        self.altura_tela = 600
        self.inicializar_pygame()
        self.inicializar_opengl()
        self.camera = Camera(
            posicao=[self.grid.dimensoes[0] / 2, self.grid.dimensoes[1] / 2, -max(self.grid.dimensoes) * 2],
            olhar_para=[self.grid.dimensoes[0] / 2, self.grid.dimensoes[1] / 2, self.grid.dimensoes[2] / 2],
            cima=[0, 1, 0]
        )
        self.controlador = ControladorEntrada(self.camera)
        self.rodando = True

    def inicializar_pygame(self):
        pygame.init()
        pygame.display.set_mode((self.largura_tela, self.altura_tela), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Algoritmo A* em Grid 3D")
        print("[Renderizador3D] Pygame inicializado")

    def inicializar_opengl(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        print("[Renderizador3D] OpenGL inicializado")

    def definir_parametros_camera(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.largura_tela / self.altura_tela), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        print("[Renderizador3D] Parâmetros da câmera definidos")

    def processar_eventos(self):
        self.controlador.processar_eventos()
        self.controlador.atualizar_camera()
        self.rodando = self.controlador.rodando

    def desenhar_grid(self):
        glColor3f(0.5, 0.5, 0.5)  # Cinza sem transparência
        glBegin(GL_LINES)
        x_max, y_max, z_max = self.grid.dimensoes
        for x in range(x_max + 1):
            for y in range(y_max + 1):
                glVertex3f(x, y, 0)
                glVertex3f(x, y, z_max)
        for x in range(x_max + 1):
            for z in range(z_max + 1):
                glVertex3f(x, 0, z)
                glVertex3f(x, y_max, z)
        for y in range(y_max + 1):
            for z in range(z_max + 1):
                glVertex3f(0, y, z)
                glVertex3f(x_max, y, z)
        glEnd()
        print("[Renderizador3D] Grid desenhado")

    def desenhar_caminho(self):
        glColor3f(0.0, 1.0, 0.0)  # Verde para o caminho
        glLineWidth(2)
        glBegin(GL_LINE_STRIP)
        for posicao in self.caminho:
            x, y, z = posicao
            glVertex3f(x + 0.5, y + 0.5, z + 0.5)
        glEnd()
        glLineWidth(1)
        print("[Renderizador3D] Caminho desenhado")

    def desenhar_ponto(self, posicao: Tuple[int, int, int], cor: Tuple[float, float, float]):
        glColor3f(*cor)
        glPushMatrix()
        x, y, z = posicao
        glTranslatef(x + 0.5, y + 0.5, z + 0.5)
        glScalef(0.2, 0.2, 0.2)
        self.desenhar_cubo()
        glPopMatrix()
        print(f"[Renderizador3D] Ponto desenhado em {posicao} com cor {cor}")

    def desenhar_cubo(self):
        glBegin(GL_QUADS)
        # Frente
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        # Traseira
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        # Lado esquerdo
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        # Lado direito
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        # Superior
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, -0.5)
        # Inferior
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glEnd()

    def executar(self):
        self.definir_parametros_camera()
        while self.rodando:
            self.processar_eventos()
            print(f"[Renderizador3D] Posição da câmera: {self.camera.posicao}, Olhando para: {self.camera.olhar_para}")
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            gluLookAt(
                self.camera.posicao[0], self.camera.posicao[1], self.camera.posicao[2],
                self.camera.olhar_para[0], self.camera.olhar_para[1], self.camera.olhar_para[2],
                self.camera.cima[0], self.camera.cima[1], self.camera.cima[2]
            )

            self.desenhar_grid()
            self.desenhar_caminho()

            # Desenhar pontos inicial e final
            self.desenhar_ponto(self.grid.inicio, (0.0, 0.0, 1.0))  # Azul
            self.desenhar_ponto(self.grid.fim, (1.0, 1.0, 0.0))     # Amarelo

            pygame.display.flip()
            pygame.time.wait(10)
        pygame.quit()
        print("[Renderizador3D] Execução finalizada")
