import pygame
import pygame_gui as gui

from dialogs import file_dialog
from functions import load_image, terminate
from players import Player


class Buttons(pygame.sprite.Sprite):
    """Класс пользовательских кнопок

    """

    def __init__(self, btn, txt, pos_x, pos_y, size=None, proc=None, name=None, group=None):
        """Кнопка с изображением и надписью
        :param btn: файл изорбражения
        :param txt: файл надписи
        :param pos_x: координата размещения x
        :param pos_y: координаты размещения y
        :param size: размер экрана
        :param proc: размер кнопки в процентах от экрана по высоте
        :param name: внутренее имя

        """
        super().__init__()
        self.txt = load_image(txt)
        self.size = self.txt.get_rect().size
        if size is not None:
            koeff = self.size[0] / self.size[1]
            self.size = (int(size[1] * proc // 100 * koeff), size[1] * proc // 100)

        self.btn = load_image(btn, self.size)
        # 2 возможных состояния кнопки - не нажата и нажата
        self.normal_btn = self.btn
        self.check_btn = load_image('data/Button01.png', self.size)

        self.rect = pygame.Rect((pos_x, pos_y), self.size)
        self.resize(self.size)
        self.name = name
        if group is not None:
            group.add(self)

    def update(self, screen):
        """Обновление кнопки в кадре
        :param screen: на какой поверхности размещается
        """
        screen.blit(self.btn, self.rect)
        screen.blit(self.txt, self.rect)
        self.screen = screen

    def resize(self, size):
        """Изменение размеров кнопки

        :param size: кортеж (ширина, высота)
        """
        self.btn = pygame.transform.scale(self.btn, size)
        self.txt = pygame.transform.scale(self.txt, size)

    def choose_button(self):
        """Смена изображения кнопки при выборе

        """
        self.btn = self.check_btn
        self.update(self.screen)

    def unchoose_button(self):
        """Смена изображения кнопки при выборе другой кнопки

        """
        self.btn = self.normal_btn
        self.update(self.screen)


def group_click(mouse, group):
    if pygame.sprite.spritecollideany(mouse, group):
        button = pygame.sprite.spritecollideany(mouse, group)
        for item in group.sprites():
            item.unchoose_button()
        button.choose_button()
        print(button.name)
        return button.name


def start_screen(screen, FPS):
    """Стартовый экран игры
    :param screen: родительский экран
    :param FPS: частота кадров
    :return: кортеж сложности игры (количество карт в строке, количество карт в столбце)
    """
    size = screen.get_size()
    clock = pygame.time.Clock()
    game_hardness = {'easy': (4, 4), 'normal': (5, 6), 'hard': (6, 8)}  # Количество карт по ширине и высоте
    game_mode = {'single': 1, 'multi': 2}  # Количество игроков
    hardness = game_hardness['easy']  # по-умолчанию простой, меняется при выборе Options
    mode = 2  # по-умолчанию 2 игрока
    spritesheet = 'cards.jpg'
    fon = load_image('bg.png', size, dir='data')
    screen.blit(fon, (0, 0))
    main_buttons = pygame.sprite.Group()
    play = Buttons('data/Button08.png', 'data/Text/TxtPlay.png', 0, 0, size=size, proc=15, group=main_buttons)
    play.rect.center = (size[0] // 2, size[1] // 2 - 100)  # Размещаем ровно по центру
    mode_buttons = pygame.sprite.Group()
    single = Buttons('data/Button10.png', 'data/Text/TxtSingle.png', 0, 0, name='single', size=size, proc=10,
                     group=main_buttons)
    single.rect.topright = (play.rect.left - 20, play.rect.bottom + 20)
    mode_buttons.add(single)
    multi = Buttons('data/Button10.png', 'data/Text/TxtMulti.png', play.rect.right + 20, play.rect.bottom + 20,
                    name='multi', size=size, proc=10, group=main_buttons)
    mode_buttons.add(multi)
    options = Buttons('data/Button09.png', 'data/Text/TxtOptions.png', 10, size[1] * 7 // 8, size=size, proc=10,
                      group=main_buttons)
    # Кнопки меню Options появляются после нажатия на нее
    level_buttons = pygame.sprite.Group()
    easy = Buttons('data/Button08.png', 'data/Text/easy.png', options.rect.left,
                   options.rect.top - 2 * options.rect.height, name='easy', size=size, proc=7, group=level_buttons)
    normal = Buttons('data/Button09.png', 'data/Text/normal.png', easy.rect.right + 30, easy.rect.bottom + 5, size=size,
                     proc=7, name='normal', group=level_buttons)
    hard = Buttons('data/Button10.png', 'data/Text/hard.png', normal.rect.right + 20, normal.rect.bottom + 5, size=size,
                   proc=7, name='hard', group=level_buttons)

    picture = Buttons('data/Button07.png', 'data/Text/TxtMore.png', 0, 0, name='picture', size=size, proc=10,
                      group=main_buttons)
    picture.rect.topright = (size[0] - 10, size[1] * 7 // 8)
    # Формируем надпись
    intro_text = ['Цель игры:', 'собрать как можно больше карточек и ',
                  'поразить всех своей феноменальной способностью запоминать.']
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

    main_buttons.update(screen)
    choice = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return  # начинаем игру по enter с простым уровнем сложности
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Создаем микро-кнопку для отслеживания нажатия кнопок
                mouse = Buttons('data/Button10.png', 'data/Text/hard.png', x, y)
                mouse.resize((1, 1))
                if play.rect.colliderect(mouse.rect):
                    return (hardness, mode, spritesheet)  # начинаем игру по кнопке Play
                if options.rect.colliderect(mouse.rect):
                    # При нажатии на кнопку Options показываем кнопки сложности
                    level_buttons.update(screen)
                check_hardness = group_click(mouse, level_buttons)
                if check_hardness is not None:
                    hardness = game_hardness[check_hardness]
                check_mode = group_click(mouse, mode_buttons)
                if check_mode is not None:
                    mode = game_mode[check_mode]
                if picture.rect.colliderect(mouse.rect):
                    spritesheet = file_dialog()

        pygame.display.flip()
        clock.tick(FPS)


def end_screen(screen, FPS, speed, *players):
    """Заключительный экран
    :param screen: родительский экран
    :param FPS: частота кадров
    :param speed: скорость движения персонажей
    :param cat: Персонаж1
    :param dog: Персонаж2
    :return: True если игру нужно начать заново
    """
    pygame.mixer.music.load('data/champions.mp3')
    pygame.mixer.music.play()
    size = WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    manager = gui.UIManager(size)
    fon = load_image('winner.jpg', (WIDTH, HEIGHT), dir='data')
    cat = players[0]
    if len(players) == 2:
        dog = players[1]
    else:
        dog = Player('dog', 0, 0, 0, '')
    if dog.name:
        dog_score = dog.score
    else:
        dog_score = ''
    # Формируем надпись
    line = f'{cat.name}     {cat.score}' + ' ' * 60 + f'{dog.name}     {dog_score}'
    font = pygame.font.Font(None, 50)
    string_rendered = font.render(line, 1, pygame.Color('red'))
    # Размещаем персонажей на экране
    cat.dir = 'idle'
    dog.dir = 'idle'
    cat.rect.x, cat.rect.y = (cat.size[0], HEIGHT // 4)
    dog.rect.x, dog.rect.y = (WIDTH - dog.size[0] * 3 // 2, HEIGHT // 4)
    no_winner = False
    if cat.score > dog.score:
        winner = cat
        loser = dog
    elif cat.score < dog.score:
        winner = dog
        loser = cat
    else:
        no_winner = True
    is_move = False
    if not no_winner and len(players) == 2:
        winner.dir = 'run'
        is_move = True
        distance = abs(loser.rect.x - winner.rect.x)
    # Кнопка В начало
    btn_new_game = gui.elements.UIButton(
        relative_rect=pygame.Rect((20, HEIGHT - 150), (150, 100)),
        text='В начало',
        manager=manager
    )
    # Основной цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # обработка кнопки В начало
            if event.type == pygame.USEREVENT:
                if event.user_type == gui.UI_BUTTON_PRESSED:
                    if event.ui_element == btn_new_game:
                        pygame.mixer.music.stop()
                        return True
            manager.process_events(event)
        # анимация
        if len(players) == 2 and is_move and not no_winner:
            if not pygame.sprite.collide_rect_ratio(0.5)(loser, winner):
                if abs(loser.rect.x - winner.rect.x) * 2 > distance:
                    is_move = winner.move(loser.rect.x, loser.rect.y, speed // 2, slide='run')
                else:
                    is_move = winner.move(loser.rect.x, loser.rect.y, speed // 2, slide='slide')
            else:
                winner.dir = 'jump'
                FPS = 5
                loser.dir = 'hurt'
        cat.update()
        dog.update()
        screen.blit(cat.image, cat.rect)
        screen.blit(dog.image, dog.rect)
        pygame.display.flip()
        manager.update(FPS)
        screen.blit(fon, (0, 0))
        screen.blit(string_rendered, (10, 20))
        manager.draw_ui(screen)
        clock.tick(FPS)
