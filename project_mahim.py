import random
import pygame as pg
import math as m

WIDTH = 1080 #CONST
HEIGHT = 700
FPS = 60

# not key: Base64 MD5 SHA1 SHA256 SHA512
# symmetry: AES(Rijndael) RC4
# asymmetry: RSA

tabs = ['Base64','MD5','SHA1','SHA256','SHA512','AES(Rijndael)','RC4','RSA']

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

input_box = dict()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Криптография") # Название
pg.display.set_icon(pg.image.load("pictures.jpg")) # Иконка

hacker_surf = pg.image.load("pictures.jpg") # Картинка фона
hacker_rect = hacker_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))

number = 5
input_box[0] = pg.Rect(HEIGHT/2 + HEIGHT/6, WIDTH/15, 200, 100)
for i in range(1,number):
    input_box[i] = pg.Rect(HEIGHT/2 + ((-1)**i)*HEIGHT/2, WIDTH/3 + (-1)**(m.ceil(i/2))*WIDTH/18, 140, 32)

 # Окошко ввода
color_inactive = pg.Color('lightskyblue3')
color_active = pg.Color('dodgerblue2')

input_box_1 = pg.Rect(100, 300, 140, 32)
color = []
active = []
text = []
for i in range(number):
    active.append(False)
    color.append(color_inactive)
    text.append('')


done = False

# Создаем игру и окно
pg.init()
pg.mixer.init()

# Цикл игры
while not done:
    font = pg.font.Font(None, 32)
    clock = pg.time.Clock()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            for i in range(number):
                if input_box[i].collidepoint(event.pos):
                # Toggle the active variable.
                    active[i] = not active[i]
                else:
                    active[i] = False
            # Change the current color of the input box.
                color[i] = color_active if active[i] else color_inactive
        if event.type == pg.KEYDOWN:
            for i in range(number):
                if active[i]:
                    if event.key == pg.K_RETURN:
                        print(text[i])
                    elif event.key == pg.K_BACKSPACE:
                        text[i] = text[i][:-1]
                    else:
                        text[i] += event.unicode
    #screen.fill((30, 30, 30))
    # Render the current text.

    for i in range(number):
        txt_surface = font.render(text[i], True, color[i])
        width = max(200, txt_surface.get_width() + 10)
        input_box[i].w = width + i*100 # Окошко ввода
        screen.blit(txt_surface, (input_box[i].x + 5, input_box[i].y + 5))
        pg.draw.rect(screen, color[i], input_box[i], 2)
    # Blit the text.

     # Окошко ввода

    # Blit the input_box rect.
     # Окошко ввода
    pg.display.flip()
    clock.tick(30)
    screen.blit(hacker_surf, hacker_rect)
    pg.display.update()

pg.quit()

