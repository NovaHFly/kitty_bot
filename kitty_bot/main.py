#! .venv/scripts/python

import logging

import requests as req
import telebot as tb
from dotenv import load_dotenv
from telebot.types import Message

from kitty_bot import config

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
)

load_dotenv()

CAT_API_URL = 'https://api.thecatapi.com/v1/images/search'
DOG_API_URL = 'https://api.thedogapi.com/v1/images/search'

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
    """Get a random cat picture url.

    If cat api is unavailable get a random dog picture url."""
    try:
        res = req.get(CAT_API_URL)
    except Exception as e:
        logging.error(f'Unexpected error while accessing cat api: {e}!')
        try:
            res = req.get(DOG_API_URL)
        except Exception as e:
            logging.error(f'Unexpected error while accessing cat api: {e}!')
            res = None

    if res is None:
        return ''

    (res_json,) = res.json()
    return res_json['url']


def send_cat_picture(chat_id: int) -> None:
    """Send a random cat picture to chat.

    Args:
        chat_id (int): Id of chat to send picture into."""
    cat_url = get_cat_url()

    if not cat_url:
        bot.send_message(
            chat_id=chat_id, text='Прости, я не нашёл новых картинок :-('
        )
        return

    bot.send_photo(chat_id=chat_id, photo=cat_url)


@bot.message_handler(commands=['start'])
def greet_user(message: Message) -> None:
    """Greet user and send them cat picture on /start."""
    chat = message.chat

    chat_id = chat.id
    name = chat.first_name

    text = f'Привет, {name}. Посмотри, какого котика я тебе нашёл'
    bot.send_message(chat_id=chat_id, text=text, reply_markup=newcat_keyboard)
    send_cat_picture(chat_id)


@bot.message_handler(commands=['remove_keyboard'])
def remove_keyboard(message: Message) -> None:
    """Remove reply keyboard."""
    bot.send_message(
        chat_id=message.chat.id,
        text='Мяу!',
        reply_markup=tb.types.ReplyKeyboardRemove(),
    )


@bot.message_handler(commands=['newcat'])
def send_new_cat(message: Message) -> None:
    """Send cat picture on /newcat."""
    bot.send_message(chat_id=message.chat.id, text='Вам телеграмма!')
    send_cat_picture(message.chat.id)


@bot.message_handler(content_types=['text'])
def reply_default(message: Message) -> None:
    """Send default reply message."""
    chat_id = message.chat.id
    text = 'Привет, я KittyBot!'
    bot.send_message(chat_id=chat_id, text=text)


def main() -> None:
    print('Bot is running!')
    bot.polling()


if __name__ == '__main__':
    main()
