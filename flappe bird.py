import pygame
import random

# Inicializando o pygame
pygame.init()

# Definindo cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Dimensões da tela
WIDTH, HEIGHT = 400, 600
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Configurações do pássaro
bird_x = 50
bird_y = HEIGHT // 2
bird_size = 30
gravity = 0.5
bird_y_velocity = 0

# Configurações dos canos
pipe_width = 70
pipe_gap = 200
pipe_velocity = 3

# Função para gerar um novo conjunto de canos
def create_pipe():
    height = random.randint(100, 400)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap)
    return top_pipe, bottom_pipe

# Iniciando variáveis
pipes = [create_pipe()]
score = 0
font = pygame.font.SysFont("comicsansms", 35)
clock = pygame.time.Clock()

def display_score(score):
    score_text = font.render(f"Pontuação: {score}", True, BLACK)
    DISPLAY.blit(score_text, [10, 10])

# Função principal do jogo
def game_loop():
    global bird_y, bird_y_velocity, pipes, score
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_y_velocity = -8  # Faz o pássaro "voar" para cima quando a tecla espaço é pressionada

        # Aplicando a gravidade
        bird_y_velocity += gravity
        bird_y += bird_y_velocity

        # Movendo os canos
        for pipe in pipes:
            pipe[0].x -= pipe_velocity
            pipe[1].x -= pipe_velocity

        # Remover canos fora da tela e adicionar novos
        if pipes[0][0].x + pipe_width < 0:
            pipes.pop(0)
            pipes.append(create_pipe())
            score += 1  # Aumenta a pontuação ao passar por um conjunto de canos

        # Verificando colisões
        bird_rect = pygame.Rect(bird_x, bird_y, bird_size, bird_size)
        for top_pipe, bottom_pipe in pipes:
            if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
                game_over = True

        if bird_y < 0 or bird_y > HEIGHT:  # Verifica colisão com o chão e o teto
            game_over = True

        # Atualizando o display
        DISPLAY.fill(WHITE)
        pygame.draw.rect(DISPLAY, BLUE, bird_rect)
        for top_pipe, bottom_pipe in pipes:
            pygame.draw.rect(DISPLAY, GREEN, top_pipe)
            pygame.draw.rect(DISPLAY, GREEN, bottom_pipe)
        display_score(score)
        
        pygame.display.update()
        clock.tick(30)

    # Fim de jogo
    DISPLAY.fill(WHITE)
    game_over_text = font.render("Fim de jogo! Pressione R para reiniciar", True, BLACK)
    DISPLAY.blit(game_over_text, [WIDTH // 8, HEIGHT // 2])
    display_score(score)
    pygame.display.update()

    # Espera o jogador pressionar "R" para reiniciar ou fechar o jogo
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()

# Função de inicialização do jogo
def main():
    global bird_y, bird_y_velocity, pipes, score
    bird_y = HEIGHT // 2
    bird_y_velocity = 0
    pipes = [create_pipe()]
    score = 0
    game_loop()

# Inicia o jogo
main()
