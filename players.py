import os
from functions import load_image
import pygame

STEP = 10





class Player(pygame.sprite.Sprite):
    def __init__(self, player_dir, size, pos_x, pos_y, name):
        super().__init__()
        player_dir = os.path.join('movies', player_dir)
        img_path = os.path.join(player_dir, 'idle', 'Idle (1).png')
        self.name = name

        self.image = load_image(img_path, size=size)
        self.size = self.image.get_rect().size
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.frames = {
            'right': [load_image(os.path.join(player_dir, 'right', file), size) for file in
                      os.listdir(os.path.join(player_dir, 'right'))],
            'left': [load_image(os.path.join(player_dir, 'left', file), size) for file in
                     os.listdir(os.path.join(player_dir, 'left'))],
            'idle': [load_image(os.path.join(player_dir, 'idle', file), size) for file in
                     os.listdir(os.path.join(player_dir, 'idle'))],
            'run': [load_image(os.path.join(player_dir, 'run', file), size) for file in
                    os.listdir(os.path.join(player_dir, 'run'))],
            'slide': [load_image(os.path.join(player_dir, 'slide', file), size) for file in
                      os.listdir(os.path.join(player_dir, 'slide'))],
            'dead': [load_image(os.path.join(player_dir, 'dead', file), size) for file in
                     os.listdir(os.path.join(player_dir, 'dead'))],
            'hurt': [load_image(os.path.join(player_dir, 'hurt', file), size) for file in
                     os.listdir(os.path.join(player_dir, 'hurt'))],
            'jump': [load_image(os.path.join(player_dir, 'jump', file), size) for file in
                     os.listdir(os.path.join(player_dir, 'jump'))]

        }
        self.frames['lie'] = [self.frames['dead'][-1]]
        self.cur_frame = 0
        self.dir = 'idle'
        self.score = 0

    def update(self):
        # print(self.cur_frame)
        if self.dir != 'dead':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.dir])
        else:
            if self.cur_frame != len(self.frames['dead']) - 1:
                self.cur_frame += 1
        self.image = self.frames[self.dir][self.cur_frame]

    def move(self, x, y, speed, slide=None):

        if slide is None:
            if x - self.rect.x > -x + self.rect.x:
                self.dir = 'right'
            else:
                self.dir = 'left'
        else:
            self.dir = slide
        distance = ((x - self.rect.x) ** 2 + (y - self.rect.y) ** 2) ** (1 / 2)
        # считаем дистанцию (длину от точки А до точки Б).формула длины вектора
        if distance > speed:
            self.rect.x += int(speed * (x - self.rect.x) / distance)  # идем по иксу с помощью вектора нормали
            self.rect.y += int(speed * (y - self.rect.y) / distance)  # идем по игреку так же
            return True
        else:
            return False

    def jump(self, h):
        if self.is_up:
            if self.up_count <= 8:
                self.rect.y -= h // 8
                self.up_count += 1
            else:
                self.is_up = False
                self.up_count = 1
        print(self.up_count)
