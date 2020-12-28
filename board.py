import pygame
import os

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.new_board()

    def new_board(self,dir):
        print("Текущая деректория:", os.getcwd())
        print("Все папки и файлы:", os.listdir())



    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                    pygame.draw.rect(screen, 'green', (self.left + self.cell_size * j, self.top + self.cell_size * i,
                                                       self.cell_size, self.cell_size), width=0)

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

