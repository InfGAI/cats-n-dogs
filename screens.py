import pygame
import os
import sys
from functions import load_image, terminate


def start_screen(screen, size, clock, FPS):
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = load_image('grass.png', size, dir='data')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def end_screen(screen, size, clock, FPS, speed, cat, dog):
    WIDTH, HEIGHT = size

    line = f'{cat.name}     {cat.score}' + ' ' * 60 + f'{dog.name}     {dog.score}'
    fon = load_image('winner.jpg', (WIDTH, HEIGHT), dir='data')
    cat.dir = 'idle'
    dog.dir = 'idle'
    font = pygame.font.Font(None, 50)
    text_coord = 50
    loser_is_move = True
    string_rendered = font.render(line, 1, pygame.Color('red'))
    line_rect = string_rendered.get_rect()
    cat.rect.x, cat.rect.y = (WIDTH // 8, HEIGHT // 4)
    dog.rect.x, dog.rect.y = (WIDTH * 3 // 4, HEIGHT // 4)
    if cat.score > dog.score:
        winner = cat
        loser = dog
    else:
        winner = dog
        loser = cat
    is_move = False
    count_dead = 0

    if WIDTH // 2 - loser.rect.x > 0:
        step = -WIDTH // 8
    else:
        step = WIDTH // 8
    dist_x = loser.rect.x + step
    stop = False
    while True:
        screen.blit(fon, (0, 0))
        screen.blit(string_rendered, (10, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not is_move and not stop:
                winner.dir = 'run'
                is_move = True
                distance = ((loser.rect.x - winner.rect.x) ** 2 + (loser.rect.y - winner.rect.y) ** 2) ** (1 / 2)

        if is_move:

            if ((loser.rect.x - winner.rect.x) ** 2 + (loser.rect.y - winner.rect.y) ** 2) ** (1 / 2) * 2 > distance:
                is_move = winner.move(loser.rect.x, loser.rect.y, speed // 2, slide='run')
            else:
                is_move = winner.move(loser.rect.x, loser.rect.y, speed // 2, slide='slide')
        elif winner.dir == 'slide':
            if loser_is_move:
                loser_is_move = loser.move(dist_x, loser.rect.y, speed // 2, slide='dead')
            else:
                winner.dir = 'jump'
                FPS = 5
                loser.dir = 'hurt'
                stop = True
        cat.update()
        dog.update()
        screen.blit(cat.image, cat.rect)
        screen.blit(dog.image, dog.rect)
        pygame.display.flip()
        clock.tick(FPS)
