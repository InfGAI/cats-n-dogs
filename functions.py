import pygame
import sys
import os


def load_image(name, size=None, dir=None, color_key=None):
    ''' возвращает экземпляр Surface с изображением из файла name их папки dir.
    Если size - кортеж, то размер size, если size - число, то высотой size с сохранением исходных пропорций'''
    if dir is not None:
        name = os.path.join(dir, name)

    try:
        image = pygame.image.load(name)

    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if size is not None:
        if type(size) == tuple:
            image = pygame.transform.scale(image, size)
        else:
            w, h = image.get_rect().size
            image = pygame.transform.scale(image, (w * size // h, size))
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
        image = image.convert()
    else:
        image = image.convert_alpha()

    return image


def terminate():
    pygame.quit()
    sys.exit()
