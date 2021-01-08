import os
from functions import load_image
import pygame

STEP = 10


class Player(pygame.sprite.Sprite):
    """Класс персонажей

    """

    def __init__(self, player_dir, height, pos_x, pos_y, name):
        """Персонаж с анимацией из папки player_dir, высотой height,
        в точке с координатами pos_x, pos_y, имя персонажа name

        """
        super().__init__()
        player_dir = os.path.join('movies', player_dir)
        img_path = os.path.join(player_dir, 'idle', 'Idle (1).png')
        self.name = name
        self.image = load_image(img_path, size=height)
        self.size = self.image.get_rect().size
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.frames = {
            'right': [load_image(os.path.join(player_dir, 'right', file), height) for file in
                      os.listdir(os.path.join(player_dir, 'right'))],
            'left': [load_image(os.path.join(player_dir, 'left', file), height) for file in
                     os.listdir(os.path.join(player_dir, 'left'))],
            'idle': [load_image(os.path.join(player_dir, 'idle', file), height) for file in
                     os.listdir(os.path.join(player_dir, 'idle'))],
            'run': [load_image(os.path.join(player_dir, 'run', file), height) for file in
                    os.listdir(os.path.join(player_dir, 'run'))],
            'slide': [load_image(os.path.join(player_dir, 'slide', file), height) for file in
                      os.listdir(os.path.join(player_dir, 'slide'))],
            'dead': [load_image(os.path.join(player_dir, 'dead', file), height) for file in
                     os.listdir(os.path.join(player_dir, 'dead'))],
            'hurt': [load_image(os.path.join(player_dir, 'hurt', file), height) for file in
                     os.listdir(os.path.join(player_dir, 'hurt'))],
            'jump': [load_image(os.path.join(player_dir, 'jump', file), height) for file in
                     os.listdir(os.path.join(player_dir, 'jump'))]

        }
        self.cur_frame = 0
        self.dir = 'idle'  # По-умолчанию персонаж стоит фронтально
        self.score = 0

    def update(self):
        """Анимация персонажа соответствеено self.dir

        """
        if self.dir != 'dead':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.dir])
        else:
            if self.cur_frame != len(self.frames['dead']) - 1:
                self.cur_frame += 1
        self.image = self.frames[self.dir][self.cur_frame]

    def move(self, x, y, speed, slide=None):
        """Движение персонажа в точку с координатами x, y и скоростью speed. Именованный аргумент slide устанавливает
         анимацию в протцессе движения. Возвращает True|False требуется ли дальшейшее движение для достижения x,y

        """
        if slide is None:
            if x - self.rect.x > -x + self.rect.x:
                self.dir = 'right'
            else:
                self.dir = 'left'
        else:
            self.dir = slide
        # считаем дистанцию (длину от точки А до точки Б) по т.Пифагора
        distance = ((x - self.rect.x) ** 2 + (y - self.rect.y) ** 2) ** (1 / 2)

        if distance > speed:  # убирает дерганье в конце пути
            self.rect.x += int(speed * (x - self.rect.x) / distance)  # смещаем по x с помощью вектора нормали
            self.rect.y += int(speed * (y - self.rect.y) / distance)  # смещаем по y так же
            return True
        else:
            return False
