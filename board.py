import pygame
import os

class Board:
    def __init__(self, width, height,dir,hardness):
        self.width,self.height  = hardness
        self.board = [[0] * width for _ in range(height)]
        self.left = 30
        self.top = 30
        self.cell_size = ((width-60)//6,(height-60)//4)
        print(self.cell_size)
        self.new_board(dir)

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
                    pygame.draw.rect(screen, 'green', (self.left + self.cell_size[0] * j, self.top + self.cell_size[1] * i,
                                                       self.cell_size[0], self.cell_size[1]), width=2)

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

