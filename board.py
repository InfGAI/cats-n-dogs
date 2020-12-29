import pygame
import os
from random import shuffle

COLUMNS = 5
ROWS = 5


def load_image(name, size=None, color_key=None):
    fullname = os.path.join('data', name)
    print(fullname)
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


class Board:
    def __init__(self, width, height, dir, hardness):
        self.width, self.height = hardness
        self.board = [[0] * width for _ in range(height)]
        self.left = 30
        self.top = 30
        self.cell_size = ((width - 60) // 6, (height - 60) // 4)
        print(self.cell_size)
        frames = self.new_board(dir)
        print(frames)
        self.cards = [frames.pop() for i in range(self.height * self.width // 2)]
        self.cards += self.cards
        shuffle(self.cards)


    def new_board(self, dir):
        frames = []
        img = load_image(dir)
        img_rect = pygame.Rect(0, 0, img.get_width() // COLUMNS,
                               img.get_height() // ROWS)
        for j in range(ROWS):
            for i in range(COLUMNS):

                frame_location = (img_rect.w * i, img_rect.h * j)
                if self.board[i][j]:
                    frames.append((img.subsurface(pygame.Rect(
                        frame_location, img_rect.size)), j * COLUMNS + i))
                else:
                    frames.append(load_image('back.png', self.cell_size))
        return frames

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):

        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j]:
                    img = self.cards[i * self.width + j][0]
                    img = pygame.transform.scale(img, self.cell_size)
                else:
                    img = self.cards[i * self.width + j]

                screen.blit(img, (self.left + self.cell_size[0] * j, self.top + self.cell_size[1] * i))

    def get_cell(self, pos):
        if self.left + self.cell_size * self.width >= pos[0] >= self.left:
            x = (pos[0] - self.left) // self.cell_size
        else:
            return None
        if self.top + self.cell_size * self.height >= pos[1] >= self.top:
            y = (pos[1] - self.top) // self.cell_size
        else:
            return None
        return x, y

    def on_click(self, cell_coords):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

