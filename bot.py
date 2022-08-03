import telebot
import requests

token = '5493314841:AAH-rW6sOPXetnX18V9rYnPx1xWdfR8w09U'
bot = telebot.TeleBot(token)
users = {}
with open('users.txt', 'r') as file:
    for i in file.readlines():
        key, val = i.strip().split(';')
        users[key] = val


@bot.message_handler(commands=['stop'])
def stop(msg):
    bot.send_message(msg.chat.id, 'Прекращаю отслеживать изменения')


@bot.message_handler(content_types=['text'])
def start(msg, res=False):
    user = str(msg.chat.id)
    try:
        requests.get(msg.text)
        url = msg.text
        users[user] = url
        with open('users.txt', 'w') as file:
            for u in users:
                file.write(u + ';' + users[u] + '\n')
        bot.send_message(msg.chat.id, 'Начинаю отслеживать изменения.\nВведите /stop для отмены')
    except:
        bot.send_message(msg.chat.id, 'Введите адрес сайта для отслеживания изменений')


bot.infinity_polling()
