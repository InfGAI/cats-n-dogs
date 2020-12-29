import os
import sys

import pygame

import board
import players

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 30
WIDTH = 1000
HEIGHT = 600
STEP = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
'''
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
box_group=pygame.sprite.Group()
'''


def load_image(name, size=None, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if size is not None:
        image = pygame.transform.scale(image, size)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
        image = image.convert()
    else:
        image = image.convert_alpha()

    return image

def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = load_image('grass.png', (WIDTH, HEIGHT))
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

def end_screen(cat, dog):
    line = f'{cat.name}     {cat.score}' + ' ' * 60 + f'{dog.name}     {dog.score}'
    fon = load_image('winner.jpg', (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 50

    string_rendered = font.render(line, 1, pygame.Color('red'))
    line_rect = string_rendered.get_rect()
    screen.blit(string_rendered, (10, 20))
    if cat.score > dog.score:
        winner = cat
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

def score(cat, dog):
    line = f'Кошечка {cat.score}         Собачка {dog.score}'
    font = pygame.font.Font(None, 30)
    text_coord = 30
    return font.render(line, 1, pygame.Color('white'))


start_screen()
hardness = (4, 2)
print('start')
running = True
players_group = pygame.sprite.Group()
cards = board.Board(WIDTH, HEIGHT, 'cards.jpg', hardness)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Кошечки и собачки')

cat = players.Player('cat', cards.cell_size, cards.cell_size[0] // 4, 30, 'Кошечка')
dog = players.Player('dog', cards.cell_size, cards.cell_size[0] // 4, 30, 'Собачка')
players_group.add(cat)
players_group.add(dog)
dir = 'idle'
is_move = False
count = -1
card_checked = False
card1 = None
card2 = None
winner = None
while running:
    screen.fill((0, 0, 0))
    screen.blit(score(cat, dog), (50, 10))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not is_move:
                cards.get_click(event.pos)
                card_checked = True
                count += 1
                x, y = event.pos
                x1 = ((x - cards.left) // cards.cell_size[0] * cards.cell_size[0]) - 1 + cards.cell_size[0] // 4
                y1 = ((y - cards.top) // cards.cell_size[1] * cards.cell_size[1]) - 1 + cards.cell_size[0] // 4
                # print(x1, y1)
                is_move = True
                start_time = pygame.time.get_ticks()
                speed = cards.cell_size[0] // (FPS // 2)  # скорость пережвижения
        else:
            card_checked = False
    if card_checked:
        print('count', count)
        card_checked = False
        current_card = ((y - cards.top) // cards.cell_size[1], (x - cards.left) // cards.cell_size[0])

        if count % 2 == 0 and card2:
            print(cards.check(card1, card2))
            if not cards.check(card1, card2):
                cards.close(card1, card2)
            else:
                current_player.score += 1

        if count % 2 == 0:
            card1 = current_card
        else:
            card2 = current_card
        print(card1, card2, current_card)

    if count % 4 > 1:
        current_player = cat
    else:
        current_player = dog

    if is_move:
        is_move = current_player.move(x1, y1, speed)
    else:
        current_player.dir = 'idle'

    '''tiles_group.draw(screen)
    player_group.draw(screen)'''

    cards.render(screen)
    players_group.update()
    players_group.draw(screen)
    pygame.display.flip()
    if 2 * (cat.score + dog.score) == hardness[0] * hardness[1]:
        running = False

    clock.tick(FPS)
end_screen(cat, dog)
terminate()
