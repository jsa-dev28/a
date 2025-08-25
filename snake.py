import pygame
import random
import sys

pygame.init()

# Tamaño de celda y pantalla
CELL_SIZE = 20
WIDTH, HEIGHT = 600, 400

# Colores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)  # Color para la cuadrícula

# Pantalla y reloj
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_snake(snake_body):
    for pos in snake_body:
        pygame.draw.rect(screen, GREEN, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def generate_food(snake_body):
    grid_w = WIDTH // CELL_SIZE
    grid_h = HEIGHT // CELL_SIZE
    while True:
        x = random.randint(0, grid_w - 1) * CELL_SIZE
        y = random.randint(0, grid_h - 1) * CELL_SIZE
        if (x, y) not in snake_body:
            return (x, y)

def get_speed(score):
    base_speed = 10
    increase_every = 5
    max_speed = 25
    return min(base_speed + (score // increase_every) * 2, max_speed)

def main():
    snake_pos = (100, 100)
    snake_body = [snake_pos]
    direction = "RIGHT"
    food_pos = generate_food(snake_body)
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        x, y = snake_pos
        if direction == "UP":
            y -= CELL_SIZE
        elif direction == "DOWN":
            y += CELL_SIZE
        elif direction == "LEFT":
            x -= CELL_SIZE
        elif direction == "RIGHT":
            x += CELL_SIZE

        snake_pos = (x, y)
        snake_body.insert(0, snake_pos)

        if snake_pos == food_pos:
            score += 1
            food_pos = generate_food(snake_body)
        else:
            snake_body.pop()

        if (
            x < 0 or x >= WIDTH or
            y < 0 or y >= HEIGHT or
            snake_pos in snake_body[1:]
        ):
            draw_text("Game Over! Puntaje: " + str(score), RED, 100, HEIGHT // 2)
            pygame.display.update()
            pygame.time.wait(2000)
            main()

        screen.fill(BLACK)
        draw_grid()  # ⚠️ Cuadrícula visual
        draw_snake(snake_body)
        pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))
        draw_text("Puntaje: " + str(score), WHITE, 10, 10)
        pygame.display.update()

        clock.tick(get_speed(score))

if __name__ == "__main__":
    main()
