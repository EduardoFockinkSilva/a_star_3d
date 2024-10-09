# Algoritmo A* em Grid 3D

## Descrição
Este projeto implementa o algoritmo A* em um grid 3D, permitindo visualizar o caminho encontrado, os obstáculos e os nós explorados durante a busca. A visualização é feita utilizando `pygame` e `PyOpenGL`, proporcionando um ambiente interativo onde é possível mover e rotacionar a câmera para explorar o espaço.

## Requisitos
- Python 3.6 ou superior
- pygame
- PyOpenGL

## Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Crie um ambiente virtual
Recomenda-se utilizar um ambiente virtual para gerenciar as dependências do projeto.
```bash
python -m venv venv
```

### 3. Ative o ambiente virtual
- Windows:
  ```bash
  venv\Scripts\activate
  ```
- Linux/MacOS:
  ```bash
  source venv/bin/activate
  ```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```
Nota: Caso o arquivo `requirements.txt` não esteja disponível, instale as dependências manualmente:
```bash
pip install pygame PyOpenGL
```

## Execução
Certifique-se de que o ambiente virtual está ativado e execute o arquivo `main.py`:
```bash
python main.py
```

## Controles da Câmera
Utilize as seguintes teclas para mover e rotacionar a câmera no ambiente 3D:

### Movimentação
- W: Mover para frente
- S: Mover para trás
- A: Mover para a esquerda
- D: Mover para a direita
- Q: Mover para cima
- E: Mover para baixo

### Rotação
- I: Rotacionar para cima
- K: Rotacionar para baixo
- J: Rotacionar para a esquerda
- L: Rotacionar para a direita

### Sair
- ESC: Fechar o programa
