# Модуль вспомогательных функций
import os
import sys

import pygame


def load_image(name, size=None, dir=None, color_key=None):
    """Создание Surface с изображением
    :param name: фйал изображения
    :param size: кортеж размеров либо число-высота с сохранением исходных пропорций
    :param dir: папка изображения
    :param color_key: -1 если нужно вырезать фон
    :return: Surface
    """
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
    """Корректное завершение программы

    """
    pygame.quit()
    sys.exit()
