import requests
import hashlib
import telebot
import datetime

token = '5493314841:AAH-rW6sOPXetnX18V9rYnPx1xWdfR8w09U'
bot = telebot.TeleBot(token)


def read_file(filename):
    data = {}
    with open(filename, 'r') as file:
        for i in file.readlines():
            data_list = list(i.strip().split(';'))
            key = data_list[0]
            val = data_list[1:]
            data[key] = val
    return data


def track_changes(user, url_list, hashes):
    if user not in hashes:
        hashes[user] = []
        for url in url_list:
            src = requests.get(url).text
            src_hash = hashlib.md5(src.encode()).hexdigest()
            hashes[user].append(src_hash)

    for i in range(len(url_list)):
        url = url_list[i]
        src = requests.get(url).text
        time, milliseconds = str(datetime.datetime.now()).split('.')
        src_hash = hashlib.md5(src.encode()).hexdigest()
        try:
            src_hash_old = hashes[user][i]
        except:
            src_hash_old = src_hash
            hashes[user].append(src_hash)

        if src_hash != src_hash_old:
            hashes[user][i] = src_hash
            print(f'У {user} есть изменения на {url}')  # и написать челу
            bot.send_message(user, f'{time}\nПроведена проверка. На {url} произошли изменения')
        else:
            print(f'У {user} нет изменений на {url}')
            bot.send_message(user, f'{time}\nПроведена проверка. Изменения на {url} отсутствуют')


if __name__ == "__main__":
    users = read_file('users.txt')
    hashes = read_file('hashes.txt')

    for user in users:
        url_list = users[user]
        track_changes(user, url_list, hashes)

    with open('hashes.txt', 'w') as file:
        for chat_id in hashes:
            output_string = chat_id
            for cur_hash in hashes[chat_id]:
                output_string += ';' + cur_hash
            output_string += '\n'
            file.write(output_string)
