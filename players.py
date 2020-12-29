import pygame
import os
import board
STEP=10
def load_image(name, size=None, color_key=None):
    #fullname = os.path.join('movies/cat', name)
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
    def __init__(self,player_dir,size, pos_x, pos_y):
        super().__init__()

        img_path=os.path.join('movies',player_dir,'right','Walk (1).png')
        self.size=size
        self.image = pygame.transform.scale(load_image(img_path),size)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.frames={'right':[pygame.transform.scale(load_image(os.path.join('movies/cat/right/',file)),size) for file in os.listdir('movies/cat/right') ]}
        print(self.frames)
        self.cur_frame=0



    def update(self, dir):
       # print(self.cur_frame)
        self.cur_frame = (self.cur_frame + 1) % len(self.frames[dir])
        self.image = self.frames[dir][self.cur_frame]

    def move(self, x,y):
        print(x,y)
        print(self.rect.x,self.rect.y)
        if self.rect.x <x or self.rect.y<y:

            distance = ((x - self.rect.x) **2 + (y - self.rect.y) **2)**(1/2) # считаем дистанцию (длину от точки А до точки Б).формула длины вектора
            print(distance)
            if (distance > 2): # этим условием убираем дергание во время конечной позиции спрайта
                time=pygame.time.get_ticks()
                print(time/1000*((x - self.rect.x) /(distance)), time/1000*((y - self.rect.y) /(distance)))
                self.rect.x += time/1000*((x - self.rect.x) /(distance)) # идем по иксу с помощью вектора нормали
                self.rect.y += time/1000*((y - self.rect.y) /(distance)) # идем по игреку так же
                print(self.rect.x, self.rect.y)
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