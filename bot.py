import telebot
import requests
from repository import SQLiteRepository
from main import calc_hash

token = '5493314841:AAH-rW6sOPXetnX18V9rYnPx1xWdfR8w09U'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['stop'])
def stop(msg):
    global delete_flag
    bot.send_message(msg.chat.id, 'Введите сайт для прекращения отслеживания изменений')
    delete_flag = True


@bot.message_handler(commands=['status'])
def status(msg):
    chat_id = str(msg.chat.id)
    try:
        output_string = ''
        urls = hashes.read_all()

        for user_url, src_hash in urls:
            user, url = user_url.split('_')
            if user == chat_id:
                output_string += url + '\n'

        bot.send_message(msg.chat.id, output_string)
    except:
        bot.send_message(msg.chat.id, 'Ошибка: отслеживаемые сайты не найдены')


@bot.message_handler(content_types=['text'])
def start(msg):
    chat_id = str(msg.chat.id)

    if delete_flag:
        url = msg.text
        if len(url) == 0:
            return
        if url[-1] != '/':
            url += '/'
        key = chat_id + '_' + url
        hashes.delete(key)
        bot.send_message(msg.chat.id, f'Вы прекратили отслеживать изменения на {url}')
        return

    try:
        src = requests.get(msg.text).text
        src_hash = calc_hash(src)

        url = msg.text
        if url[-1] != '/':
            url += '/'

        key = chat_id + '_' + url
        hashes.create(key, src_hash)

        bot.send_message(msg.chat.id, f'Начинаю отслеживать изменения на {url}.\nВведите /stop для отмены\n'
                                      f'Введите /status чтобы просмотреть список отслеживаемых сайтов')
    except:
        bot.send_message(msg.chat.id, 'Введите адрес сайта для отслеживания изменений')


if __name__ == '__main__':
    delete_flag = False
    hashes = SQLiteRepository('hashes', 'chat_id_url', 'hash')

    bot.infinity_polling()
