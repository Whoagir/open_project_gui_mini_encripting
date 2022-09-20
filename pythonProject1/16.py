from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mbox
from random import randint


# Импортируем ткинтер для вывода, импортируем месенджбокс для вывода окошек с информацией, имортируем рэндит для генерации ключа
root = Tk() #
root["bg"] = 'black'
# Название програмки
root.title('Encryption software')
# Размер окна
root.geometry("435x500")


my_notebook = ttk.Notebook(root)
my_notebook.pack()

#Микрофункция для вывода ключа не в формате messedgebox
def show_inf(a):
    root2 = Tk()

    root2["bg"] = '#7fc7ff'
    root2.title('Generation Key')
    root2.geometry("435x100")

    my_notebook1 = ttk.Notebook(root2)
    my_notebook1.pack()

    Label(my_notebook1, text=otvetrsa(1), bg='#7fc7ff', bd=30).grid(row=1, column=1, columnspan=3,stick='nesw')

    root2.mainloop()

#Микрофункция для вывода подсказки не в формате messedgebox
def show_inf2(a):

    root2 = Tk()

    root2["bg"] = '#99ff99'
    root2.title('Generation Key')
    root2.geometry("435x100")

    my_notebook1 = ttk.Notebook(root2)
    my_notebook1.pack()
    if h == "":
        Label(my_notebook1, text="Key not generation", bg='#99ff99', bd=30).grid(row=1, column=1, columnspan=3,stick='nesw')
    else:
        Label(my_notebook1, text=h, bg='#99ff99', bd=30).grid(row=1, column=1, columnspan=3,stick='nesw')
    root2.mainloop()

#Первая функция для запуска алгоритма цезаря
def output2(event):
    a = ca1.get()
    ca6.delete(0.0, END)
    ca6.insert(END, cezar(a))

#Алгоритм цезаря разбитый на две функции
def cezar(a):
    d = " "
    for i in range(0, len(a)):
        r = a[i]
        c = zamena(r)
        d = d + c
    return d

def zamena(l):
    t1 = "abcdefghijklmnopqrstuvwxyz"  # 26
    t2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    n = l
    m = int(ca2.get())
    for i in range(0, 26):
        if n == t1[i]:
            k = (i + m) % 26
            n = t1[k]
            break
        if n == t2[i]:
            k = (i + m) % 26
            n = t2[k]
            break
    return n

#Algorim RSA первая функция которая читает и обращается к функции stroke которая в свою очередь вызывает shifr
def output(event):
    a = calc1.get()
    calc6.delete(1.0, END)
    calc6.insert(END, stroke(a))

def stroke(r):
    d = " "
    for i in range(0, len(r)):
        a = ord(r[i])
        c = str(shifr(a))
        d = d + c + " "
    return d

#Algorim RSA прямое вычисление (немножко оптимизированное) защифровки
def shifr(a):
    okey1 = int(calc2.get())
    okey2 = int(calc3.get())
    b = a
    print (a)
    t = 1
    for j in range(1, okey1 + 1):
        t = t * b
    b = t % okey2
    return b

#Algorim RSA дешимфровка первая функция вызывающая функцию result и вызывающая в свою очередь deshifr
def output1(event):
    a = calc7.get()
    cal6.delete(1.0, END)
    cal6.insert(END, resultat(a))

def resultat(r):
    c = len(r)
    d = ""
    t = ""
    i = 1
    while i < c:
        if r[i] != " ":
            j = i
            while r[j] != " ":
                d = d + r[j]
                j += 1
            t = t + deshifr(d)
            i = j
        d = ""

        i += 1
    return t

#Algorim RSA прямое вычисление (немножко оптимизированное) защифровки
def deshifr(h):
    k = int(h)
    f = k
    d = int(cal4.get())
    m = int(cal5.get())
    for i in range(1, d):
        k = k * f
        k = k % m
    t = chr(k)
    return t

#Algorim EAS первая функция которая читает и обращается к функции EAS которая выполянет поблочно операцию исключаещего или
def output3(event):
    a = ce1.get()
    b = ce2.get()
    c6.delete(0.0, END)
    c6.insert(END, EAS(a, b))

def perevod1(a):
    t = ''
    while a != 0:
        m = a % 2
        t = str(m) + t
        a = a // 2
    while len(t)<7:
        t = '0'+t
    return t

def obratnoe(a):
    f = int(a, base=2)
    return f

#Основное преобразование в EAS
def EAS(text, key):
    k = len(text)
    h = len(key)
    s2 = ''
    s3 = ''
    s4 = ''
    s5 = ''
    f = ''
    for i in range(0,k):
        a = ord(text[i])-48
        s2 = s2 + perevod1(a)
    for i in range(0,h):
        s3 = perevod1(ord(key)-48)
    for i in range(0,len(s2)):
        s4 = s4 + str(int(s2[i])^int(s3[i%7]))
    t = len(s4)//7
    for i in range(0,t):
        f = ''
        for j in range(0,7):
            f = f+s4[i*7+j]
        s5 = s5 + str(chr(obratnoe(f)+48))
    return s5

#Блок функций для генерации ключа
def isprost(k : int):
    с = float()
    c = k ** (1 / 2)
    b = int(round(c))
    for i in range(2,b+1):
        if k%i == 0:
            return 0
            break
    return 1

def prostii(a):
    b = []
    c = randint(10,100)
    if a == 0:
        for i in range(1, 10000):
            if isprost(i) == 1:
                b.append(i)
        return b[c]
    else:
        for i in range(1, a+1):
            if (isprost(i) == 1):
                b.append(i)
        return b[randint(1,len(b)-1)]

def randomprost(a):
    p = prostii(0)
    q = prostii(0)
    n = p*q
    f = (p-1)*(q-1)
    e2 = prostii(f)
    d = f-1
    e = e2
    while e2>2:
        if (isprost(e2)==1) and (f%e2!=0):
            e = e2
            break
        e2 = e2-1
    while d>0:
        if (isprost(d) == 1) and ((d*e)%f==1) and (d!=e):
            break
        d = d-1
    e1 = (e,n,d,n)
    return  e1

h = str()

def randomprost1(a):
    global h
    i = 0
    t = randomprost(i)
    while t[2]==0:
        i = i+1
        t = randomprost(i)
    h = "Открытый ключ: " + str(t[0]) + " " + str(t[1]) + " Закрытый ключ " + str(t[2]) + " " + str(t[3])
    return h

def otvetrsa(a):
    randomprost1(1)
    c = h
    return c

#Блок функций для вывода подсказок
def check():
    answer = mbox.showinfo(title="Информация", message="Алгоритм цезаря преобразует текстовую строку с помощью смещения на какое-то кол-во символов")

def check1():
    answer = mbox.showinfo(title="Информация", message="Алгоритм RSA имеет открытый и закрытый ключ, что бы зашифровать сообщение нужен только открытый ключ")

def check2():
    show_inf(1)

def check3():
    answer = mbox.showinfo(title="Информация", message="Закрытый ключ введете в дешифровшике ")

def check4():
    answer = mbox.showinfo(title="Информация", message="Дешифровщик раскодирует сообщение только за счёт закрытого ключа")

def check5():
    answer = mbox.showinfo(title="Информация", message="Не обязательно вводить открытый ключ")

def check6():
    show_inf2(1)

def check7():
    answer = mbox.showinfo(title="Информация", message="Введите число (ключ) с помощью которого программа зашифрует сообщение")

def check8():
    answer = mbox.showinfo(title="Информация", message="Алгоритм EAS произведет операцию hor над данным сообщением и ключом")

def check9():
    answer = mbox.showinfo(title="Информация", message="Этот ключ будет блочно зашифровывать введенный вами текст, ключ должен быть 1 символом английского алфавита или цифрой")

#Блок задающий "вкладки"

my_frame3 = Frame(my_notebook, width=500, height=500, bg="#ce99ff")
my_frame4 = Frame(my_notebook, width=500, height=500, bg="#fcc49d")
my_frame1 = Frame(my_notebook, width=500, height=500, bg="#81d9eb")
my_frame2 = Frame(my_notebook, width=500, height=500, bg="#99ff99")

my_frame3.pack(fill="both", expand=1)
my_frame4.pack(fill="both", expand=1)
my_frame1.pack(fill="both", expand=1)
my_frame2.pack(fill="both", expand=1)

my_notebook.add(my_frame3, text="Алгоритм Цезаря")
my_notebook.add(my_frame4, text="Шифрование EAS")
my_notebook.add(my_frame1, text="Шифровнаие RSA")
my_notebook.add(my_frame2, text="Дешифрование RSA")

# Algoritm RSA шифрования ( визуализация )

Label(my_frame1, text="Введите сообщение для шифровки", bg='#7fc7ff', bd=3).grid(row=1, column=0, columnspan=3, stick='nesw')

calc1 = Entry(my_frame1, bg='#b1e0f2')
calc1.grid(row=2, column=1)

Button(my_frame1, text="Информация", bg='#75c1ff', command=check1).grid(row=1, column=0, padx=2, pady=2)

Label(my_frame1, text="Введите открытый ключ", bg='#7fc7ff', bd=3).grid(row=3, column=0, columnspan=3, stick='wens')

Button(my_frame1, text="Сгенерировать ключ", bg='#75c1ff', command=check2).grid(row=3, column=0, padx=10, pady=10)

calc2 = Entry(my_frame1, bg='#b1e0f2')
calc2.grid(row=4, column=0)

calc3 = Entry(my_frame1, bg='#b1e0f2')
calc3.grid(row=4, column=2)

Label(my_frame1, text="Введите закрытый ключ", bg='#7fc7ff', bd=3).grid(row=5, column=0, columnspan=3, stick='wens')

Button(my_frame1, text="Информация", bg='#75c1ff', command=check3).grid(row=5, column=0, padx=2, pady=2)

calc4 = Entry(my_frame1, bg='#b1e0f2')
calc4.grid(row=6, column=0)

calc5 = Entry(my_frame1, bg='#b1e0f2')
calc5.grid(row=6, column=2)

but = Button(my_frame1, text="Result", bg='#75c1ff', bd=3)
but.grid(row=7, column=1, stick='wens', padx=2, pady=2)

calc6 = Text(my_frame1, width=30, height=4, font='Times 10', wrap=WORD, bg='#b1e0f2')
calc6.grid(row=8, column=1)

but.bind("<Button-1>", output)

# Algoritm RSA расшифровка ( визуализация )

Label(my_frame2, text="Введите закодированное сообщение", bg='#77d496', bd=3).grid(row=1, column=0, columnspan=3, stick='nesw')

Button(my_frame2, text="Информация", bg='#75c1ff', command=check4).grid(row=1, column=0, padx=2, pady=2)

calc7 = Entry(my_frame2, bg='#c9f0d8')
calc7.grid(row=2, column=1)

Label(my_frame2, text="Введите открытый ключ", bg='#77d496', bd=3).grid(row=3, column=0, columnspan=3, stick='wens')

Button(my_frame2, text="Информация", bg='#75c1ff', command=check5).grid(row=3, column=0, padx=2, pady=2)

calc8 = Entry(my_frame2, bg='#c9f0d8')
calc8.grid(row=4, column=0)

calc9 = Entry(my_frame2, bg='#c9f0d8')
calc9.grid(row=4, column=2)

Label(my_frame2, text="Введите закрытый ключ", bg='#77d496', bd=3).grid(row=5, column=0, columnspan=3, stick='wens')

Button(my_frame2, text="Подсказка", bg='#75c1ff', command=check6).grid(row=5, column=0, padx=2, pady=2)

cal4 = Entry(my_frame2, bg='#c9f0d8')
cal4.grid(row=6, column=0)

cal5 = Entry(my_frame2, bg='#c9f0d8')
cal5.grid(row=6, column=2)

but1 = Button(my_frame2, text="Result", bd=3, bg='#77d99d')
but1.grid(row=7, column=1, stick='wens', padx=2, pady=2)

cal6 = Text(my_frame2, width=30, height=4, font='Times 10', wrap=WORD, bg='#c9f0d8')
cal6.grid(row=8, column=1)

but1.bind("<Button-1>", output1)

# algoritm Cezaru

Label(my_frame3, text="Введите сообщние для кодировки", bg='#c86fde', bd=3).grid(row=1, column=0, columnspan=5, stick='nesw')

Label(my_frame3, text="", bg='#c86fde').grid(row=1, column=5, stick='nesw')

ca1 = Entry(my_frame3, bg='#c9f0d8')
ca1.grid(row=2, column=3)

Button(my_frame3, text="Информация", bg='#b366ff', command=check).grid(row=2, column=1, padx=2, pady=2)

Label(my_frame3, text="Введите смещение", bg='#c86fde', bd=3).grid(row=3, column=0, columnspan=5, stick='wens')

Label(my_frame3, text="", bg='#c86fde').grid(row=3, column=5, stick='nesw')

ca2 = Entry(my_frame3, bg='#c9f0d8')
ca2.grid(row=4, column=3)

Button(my_frame3, text="Информация", bg='#b366ff', command=check7).grid(row=4, column=1, padx=2, pady=2)

but2 = Button(my_frame3, text="Result", bd=3, bg='#c86fde')
but2.grid(row=6, column=1, columnspan=3, stick='wens', padx=2, pady=2)

ca6 = Text(my_frame3, width=30, height=4, font='Times 10', wrap=WORD, bg='#c9f0d8')
ca6.grid(row=7, column=0, columnspan=5)

but2.bind("<Button-1>", output2)

# Algoritm EAS

Label(my_frame4, text="Введите сообщние для кодировки", bg='#ddadaf', bd=3).grid(row=1, column=0, columnspan=5, stick='nesw')

Label(my_frame4, text="", bg='#ddadaf').grid(row=1, column=5, stick='nesw')

ce1 = Entry(my_frame4, bg='#e6e6e6')
ce1.grid(row=2, column=3)

Button(my_frame4, text="Информация", bg='#75c1ff', command=check8).grid(row=2, column=1, padx=2, pady=2)

Label(my_frame4, text="Введите ключ", bg='#ddadaf', bd=3).grid(row=3, column=0, columnspan=5, stick='wens')

Label(my_frame4, text="", bg='#ddadaf').grid(row=3, column=5, stick='nesw')

ce2 = Entry(my_frame4, bg='#e6e6e6')
ce2.grid(row=4, column=3)

Button(my_frame4, text="Информация", bg='#75c1ff', command=check9).grid(row=4, column=1, padx=2, pady=2)

bu2 = Button(my_frame4, text="Result", bd=3, bg='#ddadaf')
bu2.grid(row=6, column=1, columnspan=3, stick='wens', padx=2, pady=2)

c6 = Text(my_frame4, width=30, height=4, font='Times 10', wrap=WORD, bg='#e6e6e6')
c6.grid(row=7, column=0, columnspan=5)

bu2.bind("<Button-1>", output3)

#Блок конфигураций для окон (столбцы и строки)

my_frame4.grid_columnconfigure(0, minsize=60)
my_frame4.grid_columnconfigure(1, minsize=60)
my_frame4.grid_columnconfigure(2, minsize=60)
my_frame4.grid_columnconfigure(3, minsize=60)
my_frame4.grid_columnconfigure(4, minsize=60)
my_frame4.grid_columnconfigure(5, minsize=60)

my_frame4.grid_rowconfigure(1, minsize=60)
my_frame4.grid_rowconfigure(2, minsize=60)
my_frame4.grid_rowconfigure(3, minsize=60)
my_frame4.grid_rowconfigure(4, minsize=60)
my_frame4.grid_rowconfigure(5, minsize=60)
my_frame4.grid_rowconfigure(6, minsize=60)
my_frame4.grid_rowconfigure(7, minsize=60)
my_frame4.grid_rowconfigure(8, minsize=60)

my_frame1.grid_columnconfigure(0, minsize=60)
my_frame1.grid_columnconfigure(1, minsize=60)
my_frame1.grid_columnconfigure(2, minsize=60)
my_frame1.grid_columnconfigure(3, minsize=60)
my_frame1.grid_columnconfigure(4, minsize=60)
my_frame1.grid_columnconfigure(5, minsize=60)

my_frame1.grid_rowconfigure(1, minsize=60)
my_frame1.grid_rowconfigure(2, minsize=60)
my_frame1.grid_rowconfigure(3, minsize=60)
my_frame1.grid_rowconfigure(4, minsize=60)
my_frame1.grid_rowconfigure(5, minsize=60)
my_frame1.grid_rowconfigure(6, minsize=60)
my_frame1.grid_rowconfigure(7, minsize=60)
my_frame1.grid_rowconfigure(8, minsize=60)

my_frame2.grid_columnconfigure(0, minsize=60)
my_frame2.grid_columnconfigure(1, minsize=60)
my_frame2.grid_columnconfigure(2, minsize=60)
my_frame2.grid_columnconfigure(3, minsize=60)
my_frame2.grid_columnconfigure(4, minsize=60)
my_frame2.grid_columnconfigure(5, minsize=60)

my_frame2.grid_rowconfigure(1, minsize=60)
my_frame2.grid_rowconfigure(2, minsize=60)
my_frame2.grid_rowconfigure(3, minsize=60)
my_frame2.grid_rowconfigure(4, minsize=60)
my_frame2.grid_rowconfigure(5, minsize=60)
my_frame2.grid_rowconfigure(6, minsize=60)
my_frame2.grid_rowconfigure(7, minsize=60)
my_frame2.grid_rowconfigure(8, minsize=60)

my_frame3.grid_columnconfigure(0, minsize=60)
my_frame3.grid_columnconfigure(1, minsize=60)
my_frame3.grid_columnconfigure(2, minsize=60)
my_frame3.grid_columnconfigure(3, minsize=60)
my_frame3.grid_columnconfigure(4, minsize=60)
my_frame3.grid_columnconfigure(5, minsize=60)

my_frame3.grid_rowconfigure(1, minsize=60)
my_frame3.grid_rowconfigure(2, minsize=60)
my_frame3.grid_rowconfigure(3, minsize=60)
my_frame3.grid_rowconfigure(4, minsize=60)
my_frame3.grid_rowconfigure(5, minsize=60)
my_frame3.grid_rowconfigure(6, minsize=60)
my_frame3.grid_rowconfigure(7, minsize=60)
my_frame3.grid_rowconfigure(8, minsize=60)

root.mainloop()
