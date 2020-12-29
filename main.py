import pygame
import os
import sys
import board
import players


pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 30
WIDTH = 800
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

'''
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    repeat_map = [line.replace('@', '.') for line in level_map]
    level_map += repeat_map
    # и подсчитываем максимальную длину
    max_width = WIDTH // tile_width + 1
    # print(list(map(lambda x: x.ljust(max_width, '.'), level_map)))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y).add(box_group)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y

'''
def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('grass.png'), (WIDTH, HEIGHT))
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

'''
tile_images = {'wall': load_image('box.png',(80,80)), 'empty': load_image('grass.png',(80,80))}
player_image = load_image('mario.png', (50, 70))

tile_width = tile_height = 80


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
'''

start_screen()
hardness=(6,4)
print('start')
running = True
players_group = pygame.sprite.Group()
cards=board.Board(WIDTH,HEIGHT,'',hardness)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Кошечки и собачки')
cat=players.Player('cat',cards.cell_size,cards.cell_size[0]//4,30)
players_group.add(cat)

is_move=False
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y=event.pos
            is_move=True
            '''if event.key == pygame.K_LEFT:
                cat.rect.x -= STEP
            if event.key == pygame.K_RIGHT:
                cat.rect.x += STEP
            if event.key == pygame.K_UP:
                cat.rect.y -= STEP
            if event.key == pygame.K_DOWN:
                cat.rect.y += STEP
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.x=x
                player.rect.y=y
    cat.rect.x = cat.rect.x % WIDTH
    cat.rect.y = cat.rect.y % HEIGHT'''
    if is_move:
        is_move=cat.move(x, y)





    '''tiles_group.draw(screen)
    player_group.draw(screen)'''
    cards.render(screen)
    cat.update('right')
    players_group.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)

terminate()
