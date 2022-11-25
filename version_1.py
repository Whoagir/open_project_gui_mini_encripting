import pygame as pg
import hashlib
import base64
import pyperclip
from constant import *

pg.init()
pg.mixer.init()
clock = pg.time.Clock()
font = pg.font.SysFont('Comic sans', 14)

DEFAULT_MENU_ITEM_FONT = pg.font.SysFont('Comic sans', 15)
BUTTON_FONT = pg.font.SysFont('Comic sans', 23)

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
        if len(self.text) >= len_text_input:
            text_o = []
            c = 0
            for i in range(0, len(self.text), len_text_input):
                text_o.append(self.text[i:i + len_text_input])
            for i in text_o:
                txt_surface = font.render(i, True, BLACK)
                surface.blit(txt_surface, (self.rect.x + 10, self.rect.y + 6 + c))
                c += 12
        else:
            txt_surface = font.render(self.text, True, BLACK)
            surface.blit(txt_surface, (self.rect.x + 10, self.rect.y + 6))

    def get_text(self):
        return self.text
        pass

    def event_handler(self, e):
        if e.type == pg.MOUSEBUTTONUP and self.rect.collidepoint(pg.mouse.get_pos()):
            self.click()
        if (pg.key.get_pressed()[pg.K_c] and (
                pg.key.get_pressed()[pg.K_LCTRL] or pg.key.get_pressed()[pg.K_RCTRL])) and self == focus_input:
            pyperclip.copy(self.text)
        if pg.key.get_pressed()[pg.K_v] and (pg.key.get_pressed()[pg.K_LCTRL] or pg.key.get_pressed()[pg.K_RCTRL]):
            self.text = pyperclip.paste()

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

    def select_text(self):
        pass

    def update(self):
        self.delete_timer = max(0, self.delete_timer - DT)


class Button(Base):
    def __init__(self, tab, callback, pos=(0, 0), size=(0, 0), text='Button', flag=0, speed_l=70):
        self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.tab = tab
        self.text = text
        self.hover = False
        self.clicked = False
        self.callback = callback
        self.timer = BUTTON_CLICK_TIME

        self.rect_out = pg.Rect(pos[0], pos[1] + size[1] + 10, size[0], size[1] // 4)
        self.pos_0 = pos[0]
        self.pos_1 = pos[1]
        self.size_0 = size[0]
        self.size_1 = size[1]
        self.point = False
        self.speed_loading = speed_l
        self.flag = flag

        self.point_callback = False

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

        if self.flag != 0:
            pg.draw.rect(surface, BUTTON_BACKGROUND_COLOR, self.rect_out, border_radius=DEFAULT_BORDER_RADIUS_1)
        if self.flag == 1:
            delt = 2
        elif self.flag == 2:
            delt = 0
        if self.point and self.flag != 0:
            t = - int(self.timer * self.speed_loading)
            print(t, self.size_0, self.timer)
            if t >= self.size_0:
                t = self.size_0 - 30
                self.point_callback = True
            for i in range(0, t, self.size_0 // 20):
                rect_1 = pg.Rect(self.pos_0 + i + 3, self.pos_1 + 4 + self.size_1 + 10, self.size_0 // 20 - delt,
                                 self.size_1 // 4 - 8)
                pg.draw.rect(surface, BUTTON_COLOR_CLICKED, rect_1)
            print(self.point_callback)
        if self.flag != 0:
            pg.draw.rect(surface, DEFAULT_BORDER_COLOR, self.rect_out, DEFAULT_BORDER_RADIUS_2,
                         border_radius=DEFAULT_BORDER_RADIUS_1)

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
        self.point = True

    def get_time(self):
        return pg.time.get_ticks()

    def get_point(self):
        return self.point_callback


class Option(Base):
    def __init__(self, text='', pos=(0, 0), size=(0, 0), color=GRAY_2):
        self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.text = text
        self.color = color

    def render(self, surface):
        pg.draw.rect(surface, self.color, self.rect, border_radius=DEFAULT_BORDER_RADIUS_1)
        pg.draw.rect(surface, BLACK, self.rect, DEFAULT_BORDER_RADIUS_2,
                     border_radius=DEFAULT_BORDER_RADIUS_1)
        txt_surface = BUTTON_FONT.render(self.text, True, BLACK)
        surface.blit(txt_surface, (self.rect.x + 20, self.rect.y + 20))


class Select(Base):
    def __init__(self, pos=(0, 0), size=(0, 0), text_list=[], align='horizontal'):
        self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.option_list = []
        self.rect_list = []
        self.clicked = [False] * len(text_list)
        self.color = [GRAY_2] * len(text_list)
        count = 0
        pos_option = list(pos[:])
        size_option = list(size[:])
        for idx, text in enumerate(text_list):
            if align == 'horizontal':
                pos_option[0] = pos[0] + (size[0] / len(text_list)) * idx
            else:
                pos_option[1] = pos[1] + (size[1] / len(text_list)) * idx
            size_option[0] = size[0] / 2
            self.option_list.append(
                Option(text, pos_option, size_option, color=self.color[count]))
            self.rect_list.append(
                pg.Rect(pos_option[0], pos_option[1], size_option[0], size_option[1]))
            self.selected = text_list[0] if text_list else None
            count += 1

    def render(self, surface):
        pg.draw.rect(surface, WHITE, self.rect, border_radius=DEFAULT_BORDER_RADIUS_1)
        count = 0
        for option in self.option_list:
            option.color = self.color[count]
            option.render(surface)
            count += 1

    def event_handler(self, e):
        for i in range(2):
            self.hover = self.rect_list[i].collidepoint(pg.mouse.get_pos())
            if e.type == pg.MOUSEBUTTONUP and self.hover:
                activate = i
                self.click(activate)

    def click(self, activate):
        for i in range(len(self.clicked)):
            self.clicked[i] = False
            self.color[i] = GRAY_2
        self.clicked[activate] = True
        self.color[activate] = WHITE

    def get_selected(self):
        return self.clicked


class Output(Base):
    def __init__(self, pos=(0, 0), size=(0, 0), text=''):
        self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.width = INPUT_WIDTH
        self.height = INPUT_HEIGHT
        self.text = text
        self.delete_timer = 0

    def render(self, surface):
        border_color = OUTPUT_BORDER_COLOR
        background_color = OUTPUT_BACKGROUND_COLOR
        if self == focus_input:
            border_color = OUTPUT_BORDER_COLOR
            background_color = INPUT_SELECTED_BACKGROUND_COLOR
        pg.draw.rect(surface, background_color, self.rect, border_radius=DEFAULT_BORDER_RADIUS_1)
        pg.draw.rect(surface, border_color, self.rect, DEFAULT_BORDER_RADIUS_2,
                     border_radius=DEFAULT_BORDER_RADIUS_1)
        if len(self.text) >= len_text:
            text_o = []
            c = 0
            for i in range(0, len(self.text), len_text):
                text_o.append(self.text[i:i + len_text])
            for i in text_o:
                txt_surface = font.render(i, True, BLACK)
                surface.blit(txt_surface, (self.rect.x + 10, self.rect.y + 6 + c))
                c += 12
        else:
            txt_surface = font.render(self.text, True, BLACK)
            surface.blit(txt_surface, (self.rect.x + 10, self.rect.y + 6))

    def event_handler(self, e):
        if e.type == pg.MOUSEBUTTONUP and self.rect.collidepoint(pg.mouse.get_pos()):
            self.click()
        if (pg.key.get_pressed()[pg.K_c] and (
                pg.key.get_pressed()[pg.K_LCTRL] or pg.key.get_pressed()[pg.K_RCTRL])) and self == focus_input:
            pyperclip.copy(self.text)
        if pg.key.get_pressed()[pg.K_v] and (pg.key.get_pressed()[pg.K_LCTRL] or pg.key.get_pressed()[pg.K_RCTRL]):
            self.text = pyperclip.paste()

    def click(self):
        global focus_input
        set_focus(self)

    def set_text(self, text, type='full'):
        if type == 'full':
            self.text = text
        else:
            self.text = self.text + text

    def insert(self, key):
        pass

    def update(self):
        self.delete_timer = max(0, self.delete_timer - DT)


class Label(Base):
    def __init__(self, pos=(0, 0), size=(0, 0), text=''):
        self.text = text
        self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.width = INPUT_WIDTH
        self.height = INPUT_HEIGHT

    def render(self, surface):
        pg.draw.rect(surface, LABEL_BACKGROUND_COLOR, self.rect, border_radius=DEFAULT_BORDER_RADIUS_1)
        if len(self.text) >= len_text_label:
            text_o = []
            c = 0
            for i in range(0, len(self.text), len_text_label):
                text_o.append(self.text[i:i + len_text_label])
            for i in text_o:
                txt_surface = font.render(i, True, BLACK)
                surface.blit(txt_surface, (self.rect.x + 10, self.rect.y + 6 + c))
                c += 12
        else:
            txt_surface = font.render(self.text, True, BLACK)
            surface.blit(txt_surface, (self.rect.x + 10, self.rect.y + 6))


class Tab(Base):
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


class MicroDraw(Base):
    def __init__(self, tab, func, pos=(0, 0), size=(0, 0), flag=1, pos_b=(0, 0), size_b=(0, 0), speed=100):
        # label_1 = MicroDraw('', self.submit, pos=(10, 340), size=(WIDTH - 20, 80))
        self.rect_out = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.rect_out_button = pg.Rect(pos_b[0], pos_b[1], size_b[0], size_b[1])
        self.pos_0 = pos[0]
        self.pos_1 = pos[1]
        self.size_0 = size[0]
        self.size_1 = size[1]
        self.tab = tab
        self.func = func
        self.hover = False
        self.clicked = False
        self.timer = 5
        self.point = False
        self.speed_loading = speed
        self.flag = flag

    def render(self, surface):
        btn_color = BUTTON_BACKGROUND_COLOR
        pg.draw.rect(surface, btn_color, self.rect_out, border_radius=DEFAULT_BORDER_RADIUS_1)
        if self.flag == 1:
            delt = 2
        elif self.flag == 2:
            delt = 0
        if self.point:
            t = self.speed_loading * (5 - int(self.timer))
            if t >= self.size_0:
                t = self.size_0 - 30
                self.func()
            for i in range(0, t, self.size_0 // 20):
                rect_1 = pg.Rect(self.pos_0 + i + 3, self.pos_1 + 4, self.size_0 // 20 - delt, self.size_1 - 8)
                pg.draw.rect(surface, BUTTON_COLOR_CLICKED, rect_1)
        pg.draw.rect(surface, DEFAULT_BORDER_COLOR, self.rect_out, DEFAULT_BORDER_RADIUS_2,
                     border_radius=DEFAULT_BORDER_RADIUS_1)

    def event_handler(self, e):
        self.hover = self.rect_out_button.collidepoint(pg.mouse.get_pos())
        if e.type == pg.MOUSEBUTTONUP and self.hover:
            self.click()

    def update(self):
        self.timer -= 0.5
        if self.timer <= 0:
            self.clicked = False

    def click(self):
        self.point = True
        self.clicked = True
        self.timer = 5


class Base64(Tab):
    def setup(self):
        label_1 = Label(pos=(10, 10), size=(WIDTH - 20, 40), text='Поле ввода')
        self.fields['l1'] = label_1
        input_field = Input("input_field", pos=(10, 60), size=(WIDTH - 20, 120))
        input_field.text = self.name
        self.fields['i1'] = input_field
        label_2 = Label(pos=(10, 160), size=(WIDTH - 20, 200),
                        text='Типа информация какая то. SHA512 - хеш-функция из семейства алгоритмов SHA-2')
        self.fields['l2'] = label_2
        button_1 = Button('', self.submit, pos=(10, 370), size=(WIDTH - 20, 80), text='Result', flag=0)
        self.fields['b1'] = button_1
        label_1 = MicroDraw('', self.submit_out, pos=(10, 460), size=(WIDTH - 20, 20), flag=2, pos_b=(10, 370),
                            size_b=(WIDTH - 20, 80), speed=120)
        self.fields['loa1'] = label_1
        output_1 = Output(pos=(10, 490), size=(WIDTH - 20, 120))
        self.fields['o1'] = output_1

    def submit(self):
        self.fields['o1'].set_text('  ')
        text = self.fields['i1'].get_text()
        b = base64.b64encode(bytes(text, 'utf-8'))
        self.output_text = b.decode('utf-8')

    def submit_out(self):
        self.fields['o1'].set_text(self.output_text)


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
                        text='Типа информация какая то. В криптографии SHA-1'
                             '(Secure Hash Algorithm 1) - это криптографическая хэш-функция')
        self.fields['l2'] = label_2
        button_1 = Button('', self.submit, pos=(10, 340), size=(WIDTH - 20, 80), text='Result')
        self.fields['b1'] = button_1
        output_1 = Output(pos=(10, 440), size=(WIDTH - 20, 80))
        self.fields['o1'] = output_1
        selected_1 = Select(pos=(10, 540), size=(WIDTH - 20, 80), text_list=['Кодировать', 'Декодировать'])
        self.fields['s1'] = selected_1
        # input_field = Input("input_field", pos=(10, 540), size=(WIDTH - 20, 80))
        # input_field.text = ''
        # self.fields['i2'] = input_field

    def submit(self):
        text = self.fields['i1'].get_text()
        d = self.fields['s1'].get_selected()
        if d[0]:
            hash_text = hashlib.sha1()
            hash_text.update(text.encode('utf-8'))
            output_text = hash_text.hexdigest()
            self.fields['o1'].set_text(output_text)


class SHA256(Tab):
    def setup(self):
        label_1 = Label(pos=(10, 10), size=(WIDTH - 20, 40), text='Поле ввода')
        self.fields['l1'] = label_1
        input_field = Input("input_field", pos=(10, 60), size=(WIDTH - 20, 120))
        input_field.text = self.name
        self.fields['i1'] = input_field
        label_2 = Label(pos=(10, 160), size=(WIDTH - 20, 200),
                        text='Типа информация какая то. SHA512 - хеш-функция из семейства алгоритмов SHA-2')
        self.fields['l2'] = label_2
        button_1 = Button('', self.submit, pos=(10, 370), size=(WIDTH - 20, 80), text='Result', flag=0)
        self.fields['b1'] = button_1
        label_1 = MicroDraw('', self.submit_out, pos=(10, 460), size=(WIDTH - 20, 20), flag=2, pos_b=(10, 370),
                            size_b=(WIDTH - 20, 80), speed=120)
        self.fields['loa1'] = label_1
        output_1 = Output(pos=(10, 490), size=(WIDTH - 20, 120))
        self.fields['o1'] = output_1

    def submit(self):
        self.fields['o1'].set_text('  ')
        text = self.fields['i1'].get_text()
        hash_text = hashlib.sha256()
        hash_text.update(text.encode('utf-8'))
        self.output_text = hash_text.hexdigest()

    def submit_out(self):
        self.fields['o1'].set_text(self.output_text)


class SHA512(Tab):
    def setup(self):
        label_1 = Label(pos=(10, 10), size=(WIDTH - 20, 40), text='Поле ввода')
        self.fields['l1'] = label_1
        input_field = Input("input_field", pos=(10, 60), size=(WIDTH - 20, 120))
        input_field.text = self.name
        self.fields['i1'] = input_field
        label_2 = Label(pos=(10, 160), size=(WIDTH - 20, 200),
                        text='Типа информация какая то. SHA512 - хеш-функция из семейства алгоритмов SHA-2')
        self.fields['l2'] = label_2
        button_1 = Button('', self.submit, pos=(10, 370), size=(WIDTH - 20, 80), text='Result', flag=0)
        self.fields['b1'] = button_1
        label_1 = MicroDraw('', self.submit_out, pos=(10, 460), size=(WIDTH - 20, 20), flag=2, pos_b=(10, 370),
                            size_b=(WIDTH - 20, 80), speed=120)
        self.fields['loa1'] = label_1
        output_1 = Output(pos=(10, 490), size=(WIDTH - 20, 120))
        self.fields['o1'] = output_1

    def submit(self):
        self.fields['o1'].set_text('  ')
        text = self.fields['i1'].get_text()
        hash_text = hashlib.sha512()
        hash_text.update(text.encode('utf-8'))
        self.output_text = hash_text.hexdigest()

    def submit_out(self):
        self.fields['o1'].set_text(self.output_text)


class AES(Tab):
    def setup(self):
        input_field = Input("input_field")
        input_field.text = self.name
        # label_1 = MicroDraw('', self.submit, pos=(10, 340), size=(WIDTH - 20, 20), flag=1)
        # self.fields['loa1'] = label_1

    def submit(self):
        pass


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
# pg.display.set_icon(pg.image.load("pictures.jpg"))  # Иконка
tab_surface = pg.Surface((WIDTH, HEIGHT - DEFAULT_MENU_ITEM_HEIGHT))

menu = Menu(tab_list)

while not done:
    for tab in tab_list:
        if tab.name == menu.get_selected_item_name():
            current_tab = tab
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
            # print(focus_input)
        if event.type == pg.KEYDOWN:
            # not key_input[pg.K_BACKSPACE] and not key_input[pg.K_c] and not (key_input[pg.K_LCTRL] or key_input[pg.K_RCTRL])
            if event.unicode != '':
                focus_input.insert(event.unicode)
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
