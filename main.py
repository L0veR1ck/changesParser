import requests
import hashlib
import telebot
import datetime


token = '5493314841:AAH-rW6sOPXetnX18V9rYnPx1xWdfR8w09U'
bot = telebot.TeleBot(token)

users = {}
with open('users.txt', 'r') as file:
    for i in file.readlines():
        key, val = i.strip().split(';')
        users[key] = val

hashes = {}
with open('hashes.txt', 'r') as file:
    for i in file.readlines():
        key, val = i.strip().split(';')
        hashes[key] = val


def main(user, url):
    src = requests.get(url).text
    time = datetime.datetime.now()
    src_hash = hashlib.md5(src.encode()).hexdigest()
    try:
        src_hash_old = hashes[user]
    except:
        hashes[user] = src_hash
        return
    if src_hash != src_hash_old:
        hashes[user] = src_hash
        print(f'У {user} есть изменения') # и написать челу
        bot.send_message(user, f'{time}\nПроведена проверка. На отслеживаемом сайте произошли изменения')
    else:
        print(f'У {user} нет изменений')
        bot.send_message(user, f'{time}\nПроведена проверка. Изменения на отслеживаемом сайте отсутствуют')


if __name__ == "__main__":
    for user in users:
        url = users[user]
        main(user, url)

    with open('hashes.txt', 'w') as file:
        for u in hashes:
            file.write(u + ';' + hashes[u] + '\n')
