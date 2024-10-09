# renderizador3d.py
import pygame
from pygame.locals import *
from OpenGL.GL import *
from typing import List, Tuple, Set
from grid import Grid
from camera import Camera
from controlador_entrada import ControladorEntrada
import numpy as np
from vertices import vertices_cubo, indices_cubo

class Renderizador3D:
    # Definição das cores e opacidades
    COR_CAMINHO = (0.0, 1.0, 0.0, 1.0)            # Verde sólido
    COR_NOS_EXPANDIDOS = (0.0, 0.0, 1.0, 0.1)     # Azul com baixa opacidade
    COR_OBSTACULOS = (0.8, 0.1, 0.1, 0.1)         # Vermelho escuro acinzentado
    COR_GRID = (0.5, 0.5, 0.5, 0.2)               # Cinza claro com baixa opacidade
    COR_PONTO_INICIO = (0.0, 1.0, 1.0, 1.0)       # Ciano
    COR_PONTO_FIM = (1.0, 1.0, 0.0, 1.0)          # Amarelo

    def __init__(self, grid: Grid, caminho: List[Tuple[int, int, int]], nos_expandidos: Set[Tuple[int, int, int]]):
        self.grid = grid
        self.caminho = caminho
        self.nos_expandidos = nos_expandidos
        self.largura_tela = 800
        self.altura_tela = 600
        self.inicializar_pygame()
        self.inicializar_opengl()
        self.shader_program = self.compilar_shaders()

        self.instancias_obstaculos = self.preparar_instancias(grid.obstaculos)
        self.instancias_nos_expandidos = self.preparar_instancias(nos_expandidos)

        self.inicializar_buffers()
        # Ajuste da posição inicial da câmera
        distancia_inicial = max(self.grid.dimensoes) * 2
        self.camera = Camera(
            posicao=[self.grid.dimensoes[0] / 2, self.grid.dimensoes[1] / 2, distancia_inicial],
            olhar_para=[self.grid.dimensoes[0] / 2, self.grid.dimensoes[1] / 2, self.grid.dimensoes[2] / 2],
            cima=[0, 1, 0]
        )
        self.controlador = ControladorEntrada(self.camera)
        self.rodando = True

    def inicializar_pygame(self):
        pygame.init()
        pygame.display.set_mode((self.largura_tela, self.altura_tela), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Algoritmo A* em Grid 3D")

    def inicializar_opengl(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def processar_eventos(self):
        self.controlador.processar_eventos()
        self.controlador.atualizar_camera()
        self.rodando = self.controlador.rodando

    def executar(self):
        while self.rodando:
            self.processar_eventos()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.shader_program)
            # Configurar as matrizes
            view = self.camera.obter_matriz_visao()
            projection = self.camera.obter_matriz_projecao(self.largura_tela, self.altura_tela)
            loc_view = glGetUniformLocation(self.shader_program, 'view')
            loc_projection = glGetUniformLocation(self.shader_program, 'projection')
            glUniformMatrix4fv(loc_view, 1, GL_FALSE, view)
            glUniformMatrix4fv(loc_projection, 1, GL_FALSE, projection)

            # Desenhar os objetos
            self.desenhar_ponto(self.grid.inicio, self.COR_PONTO_INICIO)
            self.desenhar_ponto(self.grid.fim, self.COR_PONTO_FIM)
            self.desenhar_caminho()
            self.desenhar_obstaculos()
            self.desenhar_nos_expandidos()
            self.desenhar_grid()

            pygame.display.flip()
            pygame.time.wait(10)
        pygame.quit()

    def inicializar_buffers(self):
        # VBO dos vértices do cubo
        self.vbo_cubo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_cubo)
        glBufferData(GL_ARRAY_BUFFER, vertices_cubo.nbytes, vertices_cubo, GL_STATIC_DRAW)

        # EBO dos índices do cubo
        self.ebo_cubo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo_cubo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_cubo.nbytes, indices_cubo, GL_STATIC_DRAW)

        # VBO das instâncias dos obstáculos
        self.vbo_instancias_obstaculos = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_instancias_obstaculos)
        glBufferData(GL_ARRAY_BUFFER, self.instancias_obstaculos.nbytes, self.instancias_obstaculos, GL_STATIC_DRAW)

        # VAO para obstáculos
        self.vao_obstaculos = glGenVertexArrays(1)
        glBindVertexArray(self.vao_obstaculos)

        # Vértices
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_cubo)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        # Instâncias
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_instancias_obstaculos)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glVertexAttribDivisor(1, 1)

        # Índices
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo_cubo)

        glBindVertexArray(0)

        # VBO das instâncias dos nós expandidos
        self.vbo_instancias_nos_expandidos = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_instancias_nos_expandidos)
        glBufferData(GL_ARRAY_BUFFER, self.instancias_nos_expandidos.nbytes, self.instancias_nos_expandidos, GL_DYNAMIC_DRAW)

        # VAO para nós expandidos
        self.vao_nos_expandidos = glGenVertexArrays(1)
        glBindVertexArray(self.vao_nos_expandidos)

        # Vértices
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_cubo)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        # Instâncias
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_instancias_nos_expandidos)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glVertexAttribDivisor(1, 1)

        # Índices
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo_cubo)

        glBindVertexArray(0)

        # VAO para o cubo único (pontos inicial e final)
        self.vao_cubo = glGenVertexArrays(1)
        glBindVertexArray(self.vao_cubo)

        # Vértices
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_cubo)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        # Índices
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo_cubo)

        glBindVertexArray(0)

    def preparar_instancias(self, posicoes):
        instancias = []
        for posicao in posicoes:
            x, y, z = posicao
            instancias.append([x + 0.5, y + 0.5, z + 0.5])
        return np.array(instancias, dtype=np.float32)

    def carregar_shader(self, caminho_shader):
        with open(caminho_shader, 'r') as arquivo:
            shader_src = arquivo.read()
        return shader_src

    def compilar_shaders(self):
        vertex_shader_src = self.carregar_shader('vertex_shader.glsl')
        fragment_shader_src = self.carregar_shader('fragment_shader.glsl')

        # Compilar Vertex Shader
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, vertex_shader_src)
        glCompileShader(vertex_shader)
        if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(vertex_shader).decode()
            print(f"Erro ao compilar o Vertex Shader:\n{error}")
            raise RuntimeError("Erro ao compilar o Vertex Shader")

        # Compilar Fragment Shader
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, fragment_shader_src)
        glCompileShader(fragment_shader)
        if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(fragment_shader).decode()
            print(f"Erro ao compilar o Fragment Shader:\n{error}")
            raise RuntimeError("Erro ao compilar o Fragment Shader")

        # Linkar o Programa
        shader_program = glCreateProgram()
        glAttachShader(shader_program, vertex_shader)
        glAttachShader(shader_program, fragment_shader)
        glLinkProgram(shader_program)
        if not glGetProgramiv(shader_program, GL_LINK_STATUS):
            error = glGetProgramInfoLog(shader_program).decode()
            print(f"Erro ao linkar o Programa de Shader:\n{error}")
            raise RuntimeError("Erro ao linkar o Programa de Shader")

        # Deletar shaders já que foram linkados
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

        return shader_program

    def desenhar_obstaculos(self):
        glUseProgram(self.shader_program)
        glBindVertexArray(self.vao_obstaculos)
        model = np.identity(4, dtype=np.float32)
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, 'model'), 1, GL_FALSE, model)
        glUniform4f(glGetUniformLocation(self.shader_program, "color"), *self.COR_OBSTACULOS)
        glDrawElementsInstanced(GL_TRIANGLES, len(indices_cubo), GL_UNSIGNED_INT, None, len(self.instancias_obstaculos))
        glBindVertexArray(0)

    def desenhar_nos_expandidos(self):
        glUseProgram(self.shader_program)
        glBindVertexArray(self.vao_nos_expandidos)
        model = np.identity(4, dtype=np.float32)
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, 'model'), 1, GL_FALSE, model)
        glUniform4f(glGetUniformLocation(self.shader_program, "color"), *self.COR_NOS_EXPANDIDOS)
        glDrawElementsInstanced(GL_TRIANGLES, len(indices_cubo), GL_UNSIGNED_INT, None, len(self.instancias_nos_expandidos))
        glBindVertexArray(0)

    def desenhar_ponto(self, posicao, cor):
        glUseProgram(self.shader_program)
        glBindVertexArray(self.vao_cubo)
        model = self.translacao(posicao[0] + 0.5, posicao[1] + 0.5, posicao[2] + 0.5)
        model = np.dot(model, self.escalonamento(1, 1, 1))
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, 'model'), 1, GL_FALSE, model)
        glUniform4f(glGetUniformLocation(self.shader_program, "color"), *cor)
        glDrawElements(GL_TRIANGLES, len(indices_cubo), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def desenhar_caminho(self):
        # Preparar VBO para o caminho
        caminho_vertices = []
        for posicao in self.caminho:
            x, y, z = posicao
            caminho_vertices.append([x + 0.5, y + 0.5, z + 0.5])
        caminho_vertices = np.array(caminho_vertices, dtype=np.float32)

        vbo_caminho = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_caminho)
        glBufferData(GL_ARRAY_BUFFER, caminho_vertices.nbytes, caminho_vertices, GL_STATIC_DRAW)

        vao_caminho = glGenVertexArrays(1)
        glBindVertexArray(vao_caminho)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glUseProgram(self.shader_program)
        model = np.identity(4, dtype=np.float32)
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, 'model'), 1, GL_FALSE, model)
        glUniform4f(glGetUniformLocation(self.shader_program, "color"), *self.COR_CAMINHO)
        glLineWidth(3)
        glBindVertexArray(vao_caminho)
        glDrawArrays(GL_LINE_STRIP, 0, len(self.caminho))
        glBindVertexArray(0)
        glLineWidth(1)

        # Liberar recursos
        glDeleteBuffers(1, [vbo_caminho])
        glDeleteVertexArrays(1, [vao_caminho])

    def desenhar_grid(self):
        # Implementação semelhante à do caminho
        linhas = []
        x_max, y_max, z_max = self.grid.dimensoes
        # Linhas no eixo X
        for y in range(y_max + 1):
            for z in range(z_max + 1):
                linhas.append([0, y, z])
                linhas.append([x_max, y, z])
        # Linhas no eixo Y
        for x in range(x_max + 1):
            for z in range(z_max + 1):
                linhas.append([x, 0, z])
                linhas.append([x, y_max, z])
        # Linhas no eixo Z
        for x in range(x_max + 1):
            for y in range(y_max + 1):
                linhas.append([x, y, 0])
                linhas.append([x, y, z_max])

        linhas = np.array(linhas, dtype=np.float32)

        vbo_grid = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_grid)
        glBufferData(GL_ARRAY_BUFFER, linhas.nbytes, linhas, GL_STATIC_DRAW)

        vao_grid = glGenVertexArrays(1)
        glBindVertexArray(vao_grid)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glUseProgram(self.shader_program)
        model = np.identity(4, dtype=np.float32)
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, 'model'), 1, GL_FALSE, model)
        glUniform4f(glGetUniformLocation(self.shader_program, "color"), *self.COR_GRID)
        glBindVertexArray(vao_grid)
        glDrawArrays(GL_LINES, 0, len(linhas))
        glBindVertexArray(0)

        # Liberar recursos
        glDeleteBuffers(1, [vbo_grid])
        glDeleteVertexArrays(1, [vao_grid])

    def translacao(self, x, y, z):
        matriz = np.identity(4, dtype=np.float32)
        matriz[3][0] = x
        matriz[3][1] = y
        matriz[3][2] = z
        return matriz

    def escalonamento(self, sx, sy, sz):
        matriz = np.identity(4, dtype=np.float32)
        matriz[0][0] = sx
        matriz[1][1] = sy
        matriz[2][2] = sz
        return matriz
