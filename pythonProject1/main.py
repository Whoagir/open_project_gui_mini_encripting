import random
import pygame as pg
import math as m

WIDTH = 1080  # CONST
HEIGHT = 700
FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


tab_list = ['Base64', 'MD5', 'SHA1', 'SHA256', 'SHA512', 'AES', 'RC4', 'RSA']




screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Криптография")  # Название
pg.display.set_icon(pg.image.load("pictures.jpg"))  # Иконка

hacker_surf = pg.image.load("pictures.jpg")  # Картинка фона
hacker_rect = hacker_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))

tab_label_list = ['Base64', 'MD5', 'SHA1', 'SHA256', 'SHA512', 'AES(Rijndael)', 'RC4', 'RSA']
input_box = dict()

number = 5
input_box[0] = pg.Rect(HEIGHT / 2 + HEIGHT / 6, WIDTH / 15, 200, 100)
for i in range(1, number):
    input_box[i] = pg.Rect(HEIGHT / 2 + ((-1) ** i) * HEIGHT / 2, WIDTH / 3 + (-1) ** (m.ceil(i / 2)) * WIDTH / 18, 140,
                           32)

tabs = []
for i in range(len(tab_label_list)):
    tabs.append(pg.Rect(HEIGHT / 15 + i * HEIGHT / 5.5, 0, 100, 100))

# Окошко ввода
color_inactive = pg.Color('lightskyblue3')
color_active = pg.Color('dodgerblue2')
color_active_menu = pg.Color('red')

input_box_1 = pg.Rect(100, 300, 140, 32)
color = []
active_box = []
active_menu = []
text = []
for i in range(number + len(tabs)):
    active_menu.append(False)
    active_box.append(False)
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
            for i in range(number + len(tab_label_list)):
                if i < number:
                    if input_box[i].collidepoint(event.pos):
                        active_box[i] = not active_box[i]
                    else:
                        active_box[i] = False  # box
                    color[i] = color_active if active_box[i] else color_inactive
                else:
                    if tabs[i - number].collidepoint(event.pos):
                        active_menu[i] = not active_menu[i]
                        for j in range(number, number + len(tab_label_list)):
                            if j != i:
                                active_menu[j] = False  # menu
                    color[i] = color_active_menu if active_menu[i] else color_inactive
                print(active_menu, active_box)
        if event.type == pg.KEYDOWN:
            for i in range(number):
                if active_box[i]:
                    if event.key == pg.K_RETURN:
                        print(text[i])
                    elif event.key == pg.K_BACKSPACE:
                        text[i] = text[i][:-1]
                    else:
                        text[i] += event.unicode

    for i in range(number):
        txt_surface = font.render(text[i], True, color[i])
        #width = max(200, txt_surface.get_width() + 10)
        #input_box[i].w = width + i * 100  # Окошко ввода
        screen.blit(txt_surface, (input_box[i].x + 5, input_box[i].y + 5))
        pg.draw.rect(screen, color[i], input_box[i], 2)

    for i in range(len(tabs)):
        txt_surface = font.render(tab_label_list[i], True, color[i + number])
        screen.blit(txt_surface, (tabs[i].x, tabs[i].y))

    # Окошко ввода

    # Окошко ввода
    pg.display.flip()
    clock.tick(FPS)
    screen.blit(hacker_surf, hacker_rect)
    pg.display.update()

pg.quit()
