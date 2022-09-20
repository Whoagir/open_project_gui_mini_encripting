import pygame as pg
import hashlib


def C(s):
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)


pg.init()
pg.mixer.init()
clock = pg.time.Clock()
font = pg.font.SysFont('Comic sans', 14)

WIDTH = 1080  # CONST
HEIGHT = 700
FPS = 60
DT = 0.05

DEFAULT_MENU_ITEM_WIDTH = 100
DEFAULT_MENU_ITEM_HEIGHT = 30
DEFAULT_MENU_ITEM_FONT = pg.font.SysFont('Comic sans', 15)
DEFAULT_MENU_COLOR = C('448db6')
DEFAULT_BORDER_COLOR = C('4875a9')
DEFAULT_BORDER_RADIUS_1 = 2
DEFAULT_BORDER_RADIUS_2 = 4
DEFAULT_BACKGROUND_COLOR = C('52a9db')

MENU_ITEM_COLOR_TEXT_HOVER = C('234059')
MENU_ITEM_COLOR_HOVER = C('47dfdc')
MENU_ITEM_COLOR_TEXT_SELECTED = C('0f161f')
MENU_ITEM_COLOR_BORDER = DEFAULT_BORDER_COLOR
MENU_BORDER_RADIUS_2 = 1

INPUT_WIDTH = 300
INPUT_HEIGHT = 100
INPUT_BASE_BACKGROUND_COLOR = C('4efcf9')
INPUT_SELECTED_BACKGROUND_COLOR = C('4a99c6')
INPUT_BORDER_COLOR = DEFAULT_BORDER_COLOR
INPUT_BORDER_COLOR_FOCUSED = C('436190')
INPUT_DELETE_TIMER = 0.2

OUTPUT_WIDTH = 300
OUTPUT_HEIGHT = 100
OUTPUT_BACKGROUND_COLOR = C('4efcf9')
OUTPUT_BORDER_COLOR = DEFAULT_BORDER_COLOR

BUTTON_CLICK_TIME = 0.3
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 70
BUTTON_FONT = pg.font.SysFont('Comic sans', 23)
BUTTON_COLOR = C('4efcf9')
BUTTON_BORDER_COLOR = DEFAULT_BORDER_COLOR
BUTTON_TEXT_COLOR = C('000000')
BUTTON_COLOR_HOVER = C('48e5df')
BUTTON_COLOR_CLICKED = C('448db6')
BUTTON_BACKGROUND_COLOR = C('4efcf9')

LABEL_BACKGROUND_COLOR = C('3b799c')

TAB_BACKGROUND = C('212121')

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

BLUE = (0, 0, 255)
GRAY = (240, 240, 240)
GRAY_2 = (200, 200, 200)

focus_input = None


def set_focus(item):
    global focus_input
    focus_input = item


def reset_focus():
    global focus_input
    focus_input = None


class Base(object):
    def render(self, surface):
        pass

    def update(self):
        pass

    def event_handler(self, e):
        pass


class Input(Base):
    def __init__(self, label='', pos=(0, 0), size=(0, 0)):
        self.label = label
        self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.text = ''
        self.delete_timer = 0

    def render(self, surface):
        global focus_input
        border_color = INPUT_BORDER_COLOR
        background_color = INPUT_BASE_BACKGROUND_COLOR
        if self == focus_input:
            border_color = INPUT_BORDER_COLOR_FOCUSED
            background_color = INPUT_SELECTED_BACKGROUND_COLOR
        pg.draw.rect(surface, background_color, self.rect, border_radius=DEFAULT_BORDER_RADIUS_1)
        pg.draw.rect(surface, border_color, self.rect, DEFAULT_BORDER_RADIUS_2, border_radius=DEFAULT_BORDER_RADIUS_1)
        txt_surface = font.render(self.text, True, BLACK)
        surface.blit(txt_surface, (self.rect.x + 10, self.rect.y + 6))

    def event_handler(self, e):
        if e.type == pg.MOUSEBUTTONUP and self.rect.collidepoint(pg.mouse.get_pos()):
            self.click()

    def get_text(self):
        return self.text
        pass

    def click(self):
        global focus_input
        set_focus(self)

    def insert(self, key):
        self.text += key

    def delete(self):
        if self.delete_timer > 0:
            return
        self.text = self.text[:-1]
        self.delete_timer = INPUT_DELETE_TIMER

    def update(self):
        self.delete_timer = max(0, self.delete_timer - DT)


class Button(Base):

    def __init__(self, tab, callback, pos=(0, 0), size=(0, 0), text='Button'):
        self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.tab = tab
        self.text = text
        self.hover = False
        self.clicked = False
        self.callback = callback
        self.timer = BUTTON_CLICK_TIME

    def render(self, surface):
        txt_color = BLACK
        btn_color = BUTTON_BACKGROUND_COLOR
        if self.hover:
            txt_color = BUTTON_TEXT_COLOR
            btn_color = BUTTON_COLOR_HOVER
        if self.clicked:
            txt_color = BUTTON_COLOR
            btn_color = BUTTON_COLOR_CLICKED
        pg.draw.rect(surface, btn_color, self.rect, border_radius=DEFAULT_BORDER_RADIUS_1)
        pg.draw.rect(surface, DEFAULT_BORDER_COLOR, self.rect, DEFAULT_BORDER_RADIUS_2,
                     border_radius=DEFAULT_BORDER_RADIUS_1)
        txt_surface = BUTTON_FONT.render(self.text, True, txt_color)
        surface.blit(txt_surface, (self.rect.x + 20, self.rect.y + 20))

    def event_handler(self, e):
        self.hover = self.rect.collidepoint(pg.mouse.get_pos())
        if e.type == pg.MOUSEBUTTONUP and self.hover:
            self.click()

    def update(self):
        self.timer -= DT
        if self.timer <= 0:
            self.clicked = False

    def click(self):
        self.clicked = True
        self.callback()
        self.timer = BUTTON_CLICK_TIME


class Option(Base):
    def __init__(self, text='', pos=(0, 0), size=(0, 0)):
        self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.text = text

    def render(self, surface):
        pg.draw.rect(surface, GRAY_2, self.rect, border_radius=DEFAULT_BORDER_RADIUS_1)
        txt_surface = BUTTON_FONT.render(self.text, True, BLACK)
        surface.blit(txt_surface, (self.rect.x + 20, self.rect.y + 20))


class Select(Base):
    def __init__(self, pos=(0, 0), size=(0, 0), text_list=[], align='horizontal'):
        self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.option_list = []
        pos_option = list(pos[:])
        for idx, text in enumerate(text_list):
            if align == 'horizontal':
                pos_option[0] = (size[0] / len(text_list)) * idx
            else:
                pos_option[1] = (size[1] / len(text_list)) * idx
            self.option_list.append(
                Option(text, pos_option, size=(size[0] / (len(text_list)), size[1] / (len(text_list)))))
        self.selected = text_list[0] if text_list else None

    def render(self, surface):
        pg.draw.rect(surface, DEFAULT_BACKGROUND_COLOR, self.rect, border_radius=DEFAULT_BORDER_RADIUS_1)
        for option in self.option_list:
            option.render(surface)

    def event_handler(self, e):
        self.hover = self.rect.collidepoint(pg.mouse.get_pos())
        if e.type == pg.MOUSEBUTTONUP and self.hover:
            self.click()

    def click(self):
        pass

    def get_selected(self):
        return self.selected


class Output(Base):
    def __init__(self, pos=(0, 0), size=(0, 0), text=''):
        self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.width = INPUT_WIDTH
        self.height = INPUT_HEIGHT
        self.text = text

    def render(self, surface):
        pg.draw.rect(surface, OUTPUT_BACKGROUND_COLOR, self.rect, border_radius=DEFAULT_BORDER_RADIUS_1)
        pg.draw.rect(surface, OUTPUT_BORDER_COLOR, self.rect, DEFAULT_BORDER_RADIUS_2,
                     border_radius=DEFAULT_BORDER_RADIUS_1)
        txt_surface = font.render(self.text, True, BLACK)
        surface.blit(txt_surface, (self.rect.x + 10, self.rect.y + 6))

    def set_text(self, text):
        self.text = text


class Label(Base):
    def __init__(self, pos=(0, 0), size=(0, 0), text=''):
        self.text = text
        self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.width = INPUT_WIDTH
        self.height = INPUT_HEIGHT

    def render(self, surface):
        pg.draw.rect(surface, LABEL_BACKGROUND_COLOR, self.rect, border_radius=DEFAULT_BORDER_RADIUS_1)
        txt_surface = font.render(self.text, True, BLACK)
        surface.blit(txt_surface, (self.rect.x + 10, self.rect.y + 6))


class Tab(Base):  # создает объект (вкладку)
    def __init__(self, name=''):
        self.name = name
        self.fields = dict()
        self.setup()

    def render_content(self, surface):
        for name, field in self.fields.items():
            field.render(surface)

    def setup(self):
        pass

    def event_handler(self, e):
        for name, field in self.fields.items():
            field.event_handler(e)

    def update(self):
        for name, field in self.fields.items():
            field.update()

    def render(self, surface):
        self.render_content(surface)


class Menu(Base):
    def __init__(self, tab_list):
        self.surface = pg.Surface((WIDTH, DEFAULT_MENU_ITEM_HEIGHT))
        self.menu_list = []
        width_menu_item = max(DEFAULT_MENU_ITEM_WIDTH, WIDTH // len(tab_list))
        index_tab = 0
        for tab in tab_list:
            self.menu_list.append(MenuItem(
                tab,
                (index_tab * width_menu_item, 0),
                (width_menu_item, DEFAULT_MENU_ITEM_HEIGHT),
                self.select_item))
            index_tab += 1
        self.current_menu_item = self.menu_list[0]

    def render(self, surface):
        self.surface.fill(BLUE)
        for menu_item in self.menu_list:
            menu_item.render(self.surface, selected=menu_item == self.current_menu_item)
        surface.blit(self.surface, (0, 0))

    def event_handler(self, e):
        for menu_item in self.menu_list:
            menu_item.event_handler(event)

    def select_item(self, item):
        self.current_menu_item = item

    def get_selected_item_name(self):
        return self.current_menu_item.tab.name


class MenuItem(Base):
    def __init__(self, tab, pos, size, select_callback):
        self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.tab = tab
        self.text = self.tab.name
        self.hover = False
        self.select_callback = select_callback

    def render(self, surface, selected=False):
        menu_color = DEFAULT_MENU_COLOR
        txt_color = BLACK
        menu_border_radius = MENU_BORDER_RADIUS_2
        if self.hover:
            menu_color = MENU_ITEM_COLOR_HOVER
            txt_color = MENU_ITEM_COLOR_TEXT_HOVER
        if selected:
            menu_color = DEFAULT_BACKGROUND_COLOR
            txt_color = MENU_ITEM_COLOR_TEXT_SELECTED
            menu_border_radius = -1
        pg.draw.rect(surface, menu_color, self.rect, border_radius=DEFAULT_BORDER_RADIUS_1)
        pg.draw.rect(surface, MENU_ITEM_COLOR_BORDER, self.rect, menu_border_radius,
                     border_radius=DEFAULT_BORDER_RADIUS_1)
        txt_surface = DEFAULT_MENU_ITEM_FONT.render(self.text, True, txt_color)
        surface.blit(txt_surface, (self.rect.x + 5, self.rect.y + 2))

    def event_handler(self, e):
        self.hover = self.rect.collidepoint(pg.mouse.get_pos())
        if e.type == pg.MOUSEBUTTONDOWN and self.hover:
            self.select_callback(self)


class Base64(Tab):
    def setup(self):
        input_field = Input("input_field")
        input_field.text = self.name
        # output_field = InputField("output_field")
        # self.fields.append(input_field)
        # self.fields.append(output_field)
        # input_field = Field("input_field")
        # input_field = Field("input_field")


class MD5(Tab):
    def setup(self):
        input_field = Input("input_field")
        input_field.text = self.name
        input_field.rect.y = 200
        # output_field = InputField("output_field")
        # self.fields.append(input_field)


class SHA1(Tab):
    def setup(self):
        label_1 = Label(pos=(10, 10), size=(WIDTH - 20, 40), text='Поле ввода')
        self.fields['l1'] = label_1
        input_field = Input("input_field", pos=(10, 60), size=(WIDTH - 20, 80))
        input_field.text = ''
        self.fields['i1'] = input_field
        label_2 = Label(pos=(10, 120), size=(WIDTH - 20, 200),
                        text='Типа информация какая то. В криптографии SHA-1 (Secure Hash Algorithm 1) - это криптографическая хэш-функция')
        self.fields['l2'] = label_2
        button_1 = Button('', self.submit, pos=(10, 340), size=(WIDTH - 20, 80), text='Result')
        self.fields['b1'] = button_1
        output_1 = Output(pos=(10, 440), size=(WIDTH - 20, 80))
        self.fields['o1'] = output_1
        selected_1 = Select(pos=(10, 540), size=(WIDTH - 20, 80), text_list=['Кодировать', 'decod'])
        self.fields['s1'] = selected_1
        # input_field = Input("input_field", pos=(10, 540), size=(WIDTH - 20, 80))
        # input_field.text = ''
        # self.fields['i2'] = input_field

    def submit(self):
        text = self.fields['i1'].get_text()
        hash_text = hashlib.sha1()
        hash_text.update(text.encode('utf-8'))
        output_text = hash_text.hexdigest()
        self.fields['o1'].set_text(output_text)


class SHA256(Tab):
    def setup(self):
        label_1 = Label(pos=(10, 10), size=(WIDTH - 20, 40), text='Поле ввода')
        self.fields['l1'] = label_1
        input_field = Input("input_field", pos=(10, 60), size=(WIDTH - 20, 80))
        input_field.text = self.name
        self.fields['i1'] = input_field
        label_2 = Label(pos=(10, 120), size=(WIDTH - 20, 200),
                        text='Типа информация какая то. SHA256 - хеш-функция из семейства алгоритмов SHA-2 предназначена для создания «отпечатков» или «дайджестов» для сообщений произвольной длины')
        self.fields['l2'] = label_2
        button_1 = Button('', self.submit, pos=(10, 340), size=(WIDTH - 20, 80), text='Result')
        self.fields['b1'] = button_1
        output_1 = Output(pos=(10, 440), size=(WIDTH - 20, 80))
        self.fields['o1'] = output_1

    def submit(self):
        text = self.fields['i1'].get_text()
        hash_text = hashlib.sha256()
        hash_text.update(text.encode('utf-8'))
        output_text = hash_text.hexdigest()
        self.fields['o1'].set_text(output_text)


class SHA512(Tab):
    def setup(self):
        label_1 = Label(pos=(10, 10), size=(WIDTH - 20, 40), text='Поле ввода')
        self.fields['l1'] = label_1
        input_field = Input("input_field", pos=(10, 60), size=(WIDTH - 20, 80))
        input_field.text = self.name
        self.fields['i1'] = input_field
        label_2 = Label(pos=(10, 120), size=(WIDTH - 20, 200),
                        text='Типа информация какая то. SHA512 - хеш-функция из семейства алгоритмов SHA-2')
        self.fields['l2'] = label_2
        button_1 = Button('', self.submit, pos=(10, 340), size=(WIDTH - 20, 80), text='Result')
        self.fields['b1'] = button_1
        output_1 = Output(pos=(10, 440), size=(WIDTH - 20, 80))
        self.fields['o1'] = output_1

    def submit(self):
        text = self.fields['i1'].get_text()
        hash_text = hashlib.sha512()
        hash_text.update(text.encode('utf-8'))
        output_text = hash_text.hexdigest()
        self.fields['o1'].set_text(output_text)


class AES(Tab):
    def setup(self):
        input_field = Input("input_field")
        input_field.text = self.name
        # output_field = InputField("output_field")
        # self.fields.append(input_field)
        # self.fields.append(output_field)
        # input_field = Field("input_field")
        # input_field = Field("input_field")


class RC4(Tab):
    def setup(self):
        input_field = Input("input_field")
        input_field.text = self.name
        # output_field = InputField("output_field")
        # self.fields.append(input_field)
        # self.fields.append(output_field)
        # input_field = Field("input_field")
        # input_field = Field("input_field")


class RSA(Tab):
    def setup(self):
        input_field = Input("input_field")
        input_field.text = self.name
        # output_field = InputField("output_field")
        # self.fields.append(input_field)
        # self.fields.append(output_field)
        # input_field = Field("input_field")
        # input_field = Field("input_field")


tab_list = [
    Base64('Base64'),
    MD5('MD5'),
    SHA1('SHA1'),
    SHA256('SHA256'),
    SHA512('SHA512'),
    AES('AES'),
    RC4('RC4'),
    RSA('RSA')
]

current_tab = tab_list[0]

done = False

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Криптография")  # Название
pg.display.set_icon(pg.image.load("pictures.jpg"))  # Иконка
tab_surface = pg.Surface((WIDTH, HEIGHT - DEFAULT_MENU_ITEM_HEIGHT))

menu = Menu(tab_list)

# Цикл игры
while not done:
    for tab in tab_list:
        if tab.name == menu.get_selected_item_name():
            current_tab = tab
    # _цикл_событий_и_передача_в_таб
    key_input = pg.key.get_pressed()
    if key_input[pg.K_BACKSPACE]:
        focus_input.delete()
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONUP:
            reset_focus()
        if event.type == pg.QUIT:
            done = True
        menu.event_handler(event)
        for tab in tab_list:
            if tab != current_tab:
                continue
            tab.event_handler(event)
        if event.type == pg.KEYDOWN:
            if event.key != pg.K_BACKSPACE:
                focus_input.insert(event.unicode)
    # Пробегаемся по нашим вкладкам и проверяем обновление
    for tab in tab_list:
        if tab != current_tab:
            continue
        tab.update()
    screen.fill(WHITE)
    tab_surface.fill(DEFAULT_BACKGROUND_COLOR)
    menu.render(screen)
    for tab in tab_list:
        if tab != current_tab:
            continue
        tab.render(tab_surface)
    screen.blit(tab_surface, (0, DEFAULT_MENU_ITEM_HEIGHT))
    pg.display.flip()
    clock.tick(FPS)
pg.quit()
