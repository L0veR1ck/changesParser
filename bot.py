import telebot
import requests

token = '5493314841:AAH-rW6sOPXetnX18V9rYnPx1xWdfR8w09U'
bot = telebot.TeleBot(token)
users = {}
with open('users.txt', 'r') as file:
    for i in file.readlines():
        input_list = list(i.strip().split(';'))
        chat_id = input_list[0]
        url_list = input_list[1:]
        users[chat_id] = url_list
print(users)


@bot.message_handler(commands=['stop'])
def stop(msg):
    bot.send_message(msg.chat.id, 'Прекращаю отслеживать изменения')  # допилить


@bot.message_handler(commands=['status'])
def list(msg):
    try:
        output_string = ''
        for url in users[str(msg.chat.id)]:
            output_string += url + '\n'
        bot.send_message(msg.chat.id, output_string)
    except:
        bot.send_message(msg.chat.id, 'Ошибка: отслеживаемые сайты не найдены')


@bot.message_handler(content_types=['text'])
def start(msg, res=False):
    user = str(msg.chat.id)
    try:
        requests.get(msg.text)
        url = msg.text
        if user in users:
            users[user].append(url)
        else:
            users[user] = [url]
        with open('users.txt', 'w') as file:
            for chat_id in users:
                output_string = str(chat_id)
                for output_url in users[chat_id]:
                    output_string += ';' + output_url
                output_string += '\n'
                file.write(output_string)

        bot.send_message(msg.chat.id, f'Начинаю отслеживать изменения на {url}.\nВведите /stop для отмены\nВведите '
                                      f'/list чтобы просмотреть список отслеживаемых сайтов')
    except:
        bot.send_message(msg.chat.id, 'Введите адрес сайта для отслеживания изменений')


bot.infinity_polling()
