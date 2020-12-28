import pygame
import os
import board

def load_image(name, size=None, color_key=None):
    fullname = os.path.join('movies/cat', name)
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

class Player(pygame.sprite.Sprite):
    def __init__(self,player_image,size, pos_x, pos_y):
        super().__init__()
        self.image =  pygame.transform.scale(load_image(player_image),size)

        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def move_right(self):
        pass