from functions import load_image, terminate
import pygame
from screens import start_screen, end_screen
import board
import players

FPS = 30
WIDTH = 1000
HEIGHT = 600
STEP = 10

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Кошечки и собачки')


def score(cat, dog):
    # возвращает текст счёта
    line = f'Кошечка {cat.score}         Собачка {dog.score}'
    font = pygame.font.Font(None, 30)
    text_coord = 30
    return font.render(line, 1, pygame.Color('white'))


repeat = True  # на финальном экране кнопка В начало позволяет начать с начала
while repeat:
    hardness = start_screen(screen, FPS)  # на стартовом экране выбирается сложность игры(по-умолчанию easy)
    cards = board.Board(WIDTH, HEIGHT, 'cards.jpg', hardness)
    speed = cards.cell_size[0] // (FPS // 2)  # скорость пережвижения в зависимости от размеров игрового поля
    # 2 игрока
    players_group = pygame.sprite.Group()
    cat = players.Player('cat', cards.cell_size[1], cards.left, cards.top, 'Кошечка')
    dog = players.Player('dog', cards.cell_size[1], cat.rect.right, cards.top, 'Собачка')
    players_group.add(cat)
    players_group.add(dog)
    dir = 'idle'
    is_move = False
    count = -1
    card1 = None
    card2 = None
    winner = None
    current_player = dog
    past_player = cat

    # Основной игровой цикл
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(score(cat, dog), (50, 10))
        card_checked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # По клику мыши вскрываем карточку и персонаж бежит к ней
                if not is_move:  # Запрет на смену траектории движения, если карта уже выбрана
                    cards.get_click(event.pos)
                    x, y = event.pos
                    if cards.rect.collidepoint(x, y):  # Проверяем, что кликнули по игровому полю
                        cell_y, cell_x = cards.get_cell(event.pos)
                        # Цель персонажа - начало выбранной карты
                        x1 = (cell_x * cards.cell_size[0]) + cards.left
                        y1 = (cell_y * cards.cell_size[1]) + cards.top
                        is_move = True
                        count = (count + 1) % 4
                        card_checked = True
                        if count % 4 > 1:
                            current_player = cat
                            past_player = dog
                        else:
                            current_player = dog
                            past_player = cat
                        start_time = pygame.time.get_ticks()
        if is_move:
            is_move = current_player.move(x1, y1, speed)
        else:
            current_player.dir = 'idle'
        # Если персонаж открыл пару, он имеет право на повторный ход, в противном случае карты закрываются
        if card_checked:
            current_card = (cell_y, cell_x)
            if count % 2 == 1:
                if cards.check(card1, current_card):
                    current_player.score += 1
                    count -= 2
                card2 = current_card
            else:
                if card2 is not None:
                    if not cards.check(card1, card2):
                        cards.close(card1, card2)
                card1 = current_card
                card2 = None

        cards.render(screen)
        players_group.update()
        players_group.draw(screen)
        pygame.display.flip()
        # Как только вскрыты все карты завершаем игру и переходим к итоговому экрану
        if 2 * (cat.score + dog.score) == hardness[0] * hardness[1]:
            running = False
        clock.tick(FPS)
    repeat = end_screen(screen, FPS, speed, cat, dog)  # На финальном экране есть кнопка В начало

terminate()
