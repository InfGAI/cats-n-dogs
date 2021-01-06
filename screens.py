import pygame
import os
import sys
from functions import load_image, terminate
class Buttons(pygame.sprite.Sprite):
    def __init__(self, btn, txt, pos_x, pos_y, name=None):
        super().__init__()
        self.txt = load_image(txt)
        self.btn = load_image(btn, self.txt.get_rect().size)
        self.size = self.txt.get_rect().size
        self.rect = self.btn.get_rect().move(pos_x, pos_y)
        self.name = name

    def update(self, screen):
        screen.blit(self.btn, self.rect)
        screen.blit(self.txt, self.rect)

    def resize(self, *size):
        self.btn = pygame.transform.scale(self.btn, size)
        self.txt = pygame.transform.scale(self.txt, size)
        self.rect.width, self.rect.height = size


def start_screen(screen, size, clock, FPS):
    intro_text = ['Цель игры:', 'собрать как можно больше карточек и ',
                  'поразить всех своей феноменальной способностью запоминать.']
    game_hardness = {'easy': (4, 4), 'normal': (5, 6), 'hard': (6, 8)}
    fon = load_image('bg.png', size, dir='data')
    screen.blit(fon, (0, 0))
    play = Buttons('data/Button08.png', 'data/Text/TxtPlay.png', 0, 0)
    play.rect.center = (size[0] // 2, size[1] // 2)
    play.resize(150, 80)
    options = Buttons('data/Button09.png', 'data/Text/TxtOptions.png', 10, size[1] * 7 // 8)
    easy = Buttons('data/Button08.png', 'data/Text/easy.png', 10, size[1] * 6 // 8, name='easy')
    easy.resize(100, 30)
    normal = Buttons('data/Button09.png', 'data/Text/normal.png', easy.rect.right + 30, easy.rect.bottom + 5,
                     name='normal')
    normal.resize(100, 30)
    hard = Buttons('data/Button10.png', 'data/Text/hard.png', normal.rect.right + 20, normal.rect.bottom + 5,
                   name='hard')
    hard.resize(100, 30)

    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    hardness = game_hardness['easy']
    play.update(screen)
    options.update(screen)
    choice = False
    group_choices = pygame.sprite.Group()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:

                return  # начинаем игру по enter
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                mouse = Buttons('data/Button10.png', 'data/Text/hard.png', x, y)
                mouse.resize(1, 1)
                print(mouse.rect)

                if play.rect.left < x < play.rect.right and play.rect.top < y < play.rect.bottom:
                    return hardness  # начинаем игру по кнопке
                elif options.rect.left < x < options.rect.right and options.rect.top < y < options.rect.bottom:
                    choice = True
                    easy.update(screen)
                    group_choices.add(easy)
                    normal.update(screen)
                    group_choices.add(normal)
                    hard.update(screen)
                    group_choices.add(hard)
                    print(group_choices)
                    print(pygame.sprite.spritecollideany(mouse, group_choices))
                elif choice and pygame.sprite.spritecollideany(mouse, group_choices):
                    print(pygame.sprite.spritecollideany(mouse, group_choices))
                    hardness = game_hardness[pygame.sprite.spritecollideany(mouse, group_choices).name]
                    return hardness
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
    cat.rect.x, cat.rect.y = (cat.size[0], HEIGHT // 4)
    dog.rect.x, dog.rect.y = (WIDTH - dog.size[0] * 3 // 2, HEIGHT // 4)
    no_winner = False
    if cat.score > dog.score:
        winner = cat
        loser = dog
        finish = WIDTH
    elif cat.score < dog.score:
        winner = dog
        loser = cat
        finish = 0
    else:
        no_winner = True
    is_move = False

    stop = False
    while True:
        screen.blit(fon, (0, 0))
        screen.blit(string_rendered, (10, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not is_move and not stop:
                if not no_winner:
                    winner.dir = 'run'
                    is_move = True
                    distance = abs(loser.rect.x - winner.rect.x)
        if is_move and not no_winner:
            if not pygame.sprite.collide_rect_ratio(0.5)(loser, winner):
                if abs(loser.rect.x - winner.rect.x) * 2 > distance:
                    is_move = winner.move(loser.rect.x, loser.rect.y, speed // 2, slide='run')
                else:
                    is_move = winner.move(loser.rect.x, loser.rect.y, speed // 2, slide='slide')
                    # loser_is_move = loser.move(finish, loser.rect.y, speed // 4, slide='dead')
            else:
                winner.dir = 'jump'
                FPS = 5
                loser.dir = 'hurt'

        cat.update()
        dog.update()
        screen.blit(cat.image, cat.rect)
        screen.blit(dog.image, dog.rect)
        pygame.display.flip()
        clock.tick(FPS)
