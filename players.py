import os

import pygame

STEP = 10


def load_image(name, size=None, color_key=None):
    # fullname = os.path.join('movies/cat', name)
    print(name)
    try:
        image = pygame.image.load(name)
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


class Player(pygame.sprite.Sprite):
    def __init__(self, player_dir, size, pos_x, pos_y, name):
        super().__init__()
        player_dir = os.path.join('movies', player_dir)
        img_path = os.path.join(player_dir, 'idle', 'Idle (1).png')
        self.name = name
        self.size = size
        self.image = load_image(img_path, size=size)
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

        #   time=pygame.time.get_ticks()-star_time # время прошедшее с начала дживения
        #  print(time)
        distance = ((x - self.rect.x) ** 2 + (y - self.rect.y) ** 2) ** (1 / 2)
        # считаем дистанцию (длину от точки А до точки Б).формула длины вектора
        if distance > speed:
            # print('+x', speed * (x - self.rect.x) / distance)
            self.rect.x += int(speed * (x - self.rect.x) / distance)  # идем по иксу с помощью вектора нормали
            # print('+y', speed * (y - self.rect.y) / distance)
            self.rect.y += int(speed * (y - self.rect.y) / distance)  # идем по игреку так же
            # print(self.rect.x, self.rect.y)
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
