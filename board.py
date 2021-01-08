# Модуль описания игрового поля
import pygame
from random import shuffle
from functions import load_image

# Разметка spritesheet с карточками
COLUMNS = 5
ROWS = 5


class Board():
    """Класс игрового поля

    """

    def __init__(self, width, height, path, hardness):
        """Доска в картами
        :param width: ширина
        :param height: высота
        :param path: файл spritesheet
        :param hardness: кортеж - количество карточек по ширине и высоте

        """
        self.columns, self.rows = hardness
        self.left = width // 10
        self.top = height // 10
        self.cell_size = ((width - 2 * self.left) // self.columns, (height - 2 * self.top) // self.rows)
        self.right = self.left + self.cell_size[0] * self.columns
        self.bottom = self.top + self.cell_size[1] * self.rows
        self.rect = pygame.Rect((self.left, self.top),
                                (self.cell_size[0] * self.columns, self.cell_size[1] * self.rows))
        # Создаем и "перетасовываем" колоду карт
        frames = self.new_board(path)
        self.cards = [frames.pop() for i in range(self.rows * self.columns // 2)]
        self.cards += self.cards
        shuffle(self.cards)
        self.back = load_image('back.png', self.cell_size, dir='data')
        # Создаем логическую доску из кортежей, где на 1 месте номер карточки, а на втором метка 1 или 0 открыта/закрыта
        self.board = []
        self.opened = set()  # множество вскрытых карточек
        for i in range(self.rows):
            self.board.append(
                list(map(lambda x: [x[1], 0], self.cards[i * self.columns:i * self.columns + self.columns])))

    def new_board(self, image):
        """Игровое поле карточек
        :param image: файл spritesheet
        :return: Surface с игровым полем

        """
        frames = []
        img = load_image(image, dir='data')
        img_rect = pygame.Rect(0, 0, img.get_width() // COLUMNS,
                               img.get_height() // ROWS)
        for j in range(ROWS):
            for i in range(COLUMNS):
                frame_location = (img_rect.w * i, img_rect.h * j)
                frames.append((img.subsurface(pygame.Rect(
                    frame_location, img_rect.size)), j * COLUMNS + i))
        return frames

    def render(self, screen):
        """Отрисовка игрового поля в соответствии с логической доской
        :param screen: родительский экран

        """
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j][1]:
                    img = self.cards[i * self.columns + j][0]
                    img = pygame.transform.scale(img, self.cell_size)
                else:
                    img = self.back
                screen.blit(img, (self.left + self.cell_size[0] * j, self.top + self.cell_size[1] * i))

    def get_cell(self, pos):
        """ Преобразует еоординаты лкика в координаты логической доски
        :param pos: Координаты клика мыши
        :return: "Координаты" логической доски или None, если клик за ее пределами

        """
        if self.left + self.cell_size[0] * self.columns >= pos[0] >= self.left:
            x = (pos[0] - self.left) // self.cell_size[0]
        else:
            return None
        if self.top + self.cell_size[1] * self.rows >= pos[1] >= self.top:
            y = (pos[1] - self.top) // self.cell_size[1]
        else:
            return None
        return y, x

    def get_click(self, mouse_pos):
        """Отмечает карту в логическо доске как вскрытую
         :param mouse_pos: координаты клика мыши

         """
        cell_coords = self.get_cell(mouse_pos)
        if cell_coords:
            self.board[cell_coords[0]][cell_coords[1]][1] = 1

    def check(self, card1, card2):
        """Проверка пары карт на совпадение
        :param card1: координата карты1 логической доски
        :param card2: координата карты2 логической доски
        :return: True, если карты совпали и False в противном случае
        """
        if self.board[card1[0]][card1[1]][0] == self.board[card2[0]][card2[1]][0] and \
                self.board[card1[0]][card1[1]][0] not in self.opened:
            self.opened.add(self.board[card1[0]][card1[1]][0])
            return True
        else:
            return False

    def close(self, *args):
        """Переворачивает карточку рубашкой вверх
        :param args: координаты логической доски карт, которые нужно перевернуть, если они не отмечены как совпавшие

        """
        for i in args:
            x, y = i
            if self.board[x][y][0] not in self.opened:
                self.board[x][y][1] = 0
