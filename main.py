import requests
import hashlib
import telebot
import datetime
from repository import SQLiteRepository

token = '5493314841:AAH-rW6sOPXetnX18V9rYnPx1xWdfR8w09U'
bot = telebot.TeleBot(token)


def calc_hash(text: str):
    return hashlib.md5(text.encode()).hexdigest()


def track_changes(user, url, src_hash_old):
    src = requests.get(url).text
    time, milliseconds = str(datetime.datetime.now()).split('.')
    src_hash = calc_hash(src)

    if src_hash != src_hash_old:
        key = user + '_' + url
        hashes.update(key, src_hash)
        print(f'У {user} есть изменения на {url}')  # и написать челу
        bot.send_message(user, f'{time}\nПроведена проверка. На {url} произошли изменения')
    else:
        print(f'У {user} нет изменений на {url}')


if __name__ == "__main__":
    hashes = SQLiteRepository('hashes', 'chat_id_url', 'hash')
    queue = hashes.read_all()
    for user_url, src_hash_old in queue:
        user, url = user_url.split('_')
        track_changes(user, url, src_hash_old)
