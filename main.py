from functions import load_image, terminate
import pygame
from screens import start_screen, end_screen
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


def score(cat, dog):
    # возвращает текст счёта
    line = f'Кошечка {cat.score}         Собачка {dog.score}'
    font = pygame.font.Font(None, 30)
    text_coord = 30
    return font.render(line, 1, pygame.Color('white'))


hardness = start_screen(screen, (WIDTH, HEIGHT), clock, FPS)

running = True
players_group = pygame.sprite.Group()
cards = board.Board(WIDTH, HEIGHT, 'cards.jpg', hardness)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Кошечки и собачки')
speed = cards.cell_size[0] // (FPS // 2)  # скорость пережвижения

cat = players.Player('cat', cards.cell_size[1], cards.left, cards.top, 'Кошечка')
dog = players.Player('dog', cards.cell_size[1], cards.left, cards.top, 'Собачка')
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
while running:
    screen.fill((0, 0, 0))
    screen.blit(score(cat, dog), (50, 10))
    card_checked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not is_move:
                cards.get_click(event.pos)
                x, y = event.pos
                x1 = (((x - cards.left) // cards.cell_size[0]) * cards.cell_size[0]) + cards.left
                y1 = (((y - cards.top) // cards.cell_size[1]) * cards.cell_size[1]) + cards.top
                if cards.left < x < cards.right and cards.top < y < cards.bottom:
                    is_move = True
                    count = (count + 1) % 4
                    card_checked = True
                    if count % 4 > 1:
                        current_player = cat
                        past_player = dog
                    else:
                        current_player = dog
                        past_player = cat
                    print(current_player.name, count)

                start_time = pygame.time.get_ticks()
    if is_move:
        is_move = current_player.move(x1, y1, speed)
    else:
        current_player.dir = 'idle'

    if card_checked:
        current_card = ((y - cards.top) // cards.cell_size[1], (x - cards.left) // cards.cell_size[0])
        if count % 2 == 1:
            if cards.check(card1, current_card):
                current_player.score += 1
                count -= 2
            card2 = current_card

        else:
            if card2:
                if not cards.check(card1, card2):
                    cards.close(card1)
                    cards.close(card2)

            card1 = current_card
            card2 = None

    cards.render(screen)
    players_group.update()
    players_group.draw(screen)
    pygame.display.flip()
    if 2 * (cat.score + dog.score) == hardness[0] * hardness[1]:
        running = False

    clock.tick(FPS)
end_screen(screen, (WIDTH, HEIGHT), clock, FPS, speed, cat, dog)
terminate()
