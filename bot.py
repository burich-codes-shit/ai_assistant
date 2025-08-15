import telebot
from time import sleep
from config import BOT_TOKEN

from giga_chat.giga_main import giga_message_response

bot = telebot.TeleBot(BOT_TOKEN)
"""
Бот имеет лишь одну функцию - 
принимать cообщения от пользователя 
с последующей передачей
части запроса в gigachat
"""


@bot.message_handler()
def response(message):
    chat_id = message.chat.id
    message = message.text
    print(message)
    answer = giga_message_response(message)
    bot.send_message(chat_id, answer)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as _ex:
            print(f'Бот упал: {_ex}')
            sleep(0.3)
