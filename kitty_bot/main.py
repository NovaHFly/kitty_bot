#! .venv/scripts/python

import requests as req
import telebot as tb
from dotenv import load_dotenv
from telebot.types import Message

from kitty_bot import config

load_dotenv()

CAT_API = 'https://api.thecatapi.com/v1/images/search'

bot = tb.TeleBot(token=config.TOKEN)

newcat_keyboard = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
newcat_keyboard.row(
    tb.types.KeyboardButton('Который час?'),
    tb.types.KeyboardButton('Определи мой ip'),
)
newcat_keyboard.row(
    tb.types.KeyboardButton('/random_digit'),
    tb.types.KeyboardButton('/newcat'),
    tb.types.KeyboardButton('/remove_keyboard'),
)


def get_cat_url() -> str:
    (res_json,) = req.get(CAT_API).json()
    return res_json['url']


def send_cat_picture(chat_id: int) -> None:
    cat_url = get_cat_url()
    bot.send_photo(chat_id=chat_id, photo=cat_url)


@bot.message_handler(commands=['start'])
def greeting(message: Message) -> None:
    chat = message.chat
    chat_id = chat.id
    name = chat.first_name
    text = f'Привет, {name}. Посмотри, какого котика я тебе нашёл'
    bot.send_message(chat_id=chat_id, text=text, reply_markup=newcat_keyboard)
    send_cat_picture(chat_id)


@bot.message_handler(commands=['remove_keyboard'])
def remove_keyboard(message: Message) -> None:
    bot.send_message(
        chat_id=message.chat.id,
        text='Мяу!',
        reply_markup=tb.types.ReplyKeyboardRemove(),
    )


@bot.message_handler(commands=['newcat'])
def new_cat(message: Message) -> None:
    bot.send_message(chat_id=message.chat.id, text='Вам телеграмма!')
    send_cat_picture(message.chat.id)


@bot.message_handler(content_types=['text'])
def echo(message: Message) -> None:
    chat_id = message.chat.id
    text = 'Привет, я KittyBot!'
    bot.send_message(chat_id=chat_id, text=text)


def main() -> None:
    print('Bot is running!')
    bot.polling()


if __name__ == '__main__':
    main()
