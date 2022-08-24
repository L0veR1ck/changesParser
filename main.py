import requests
import hashlib
import telebot
import datetime
from os import mkdir
import sys
from repository import SQLiteRepository


def calc_hash(text: str):
    return hashlib.md5(text.encode()).hexdigest()


def save_page(src, user, url):
    url = url[:-1]
    url = url.replace('.', '')
    ext, url = url.split('://')
    url = url.replace('/', '')

    try:
        mkdir(f'sources/{user}')
    except:
        pass

    with open(f'sources/{user}/{url}.html', 'w') as file:
        file.write(src)


def track_changes(user, url, src_hash_old):
    src = requests.get(url).text
    time, milliseconds = str(datetime.datetime.now()).split('.')
    src_hash = calc_hash(src)

    if src_hash != src_hash_old:
        key = user + '_' + url
        hashes.update(key, src_hash)
        save_page(src, user, url)
        print(f'У {user} есть изменения на {url}')
        bot.send_message(user, f'{time}\nПроведена проверка. На {url} произошли изменения')
    else:
        print(f'У {user} нет изменений на {url}')


if __name__ == "__main__":
    token = sys.argv[1]
    bot = telebot.TeleBot(token)

    hashes = SQLiteRepository('hashes', 'chat_id_url', 'hash')
    queue = hashes.read_all()
    for user_url, src_hash_old in queue:
        print(user_url)
        user, url = user_url.split('_')
        track_changes(user, url, src_hash_old)
