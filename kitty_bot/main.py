import logging
import time
from typing import Optional

import requests as req
import telebot as tb
from telebot.types import Message

from kitty_bot import config

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
)

CAT_API_URL = 'https://api.thecatapi.com/v1/images/search'
DOG_API_URL = 'https://api.thedogapi.com/v1/images/search'

bot = tb.TeleBot(token=config.TOKEN)

newcat_keyboard = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
newcat_keyboard.row(tb.types.KeyboardButton('Хочу котиков!'))


def _get_response(url: str) -> Optional[req.Response]:
    try:
        return req.get(url)
    except Exception as e:
        logging.error(f'Unexpected error while accessing {url}: {e}')
        return None


def _get_json(response: req.Response) -> Optional[dict]:
    try:
        (res_json,) = response.json()
    except Exception as e:
        logging.error(f'Unexpected error while decoding json: {e}')
        return None

    return res_json


def get_cat_url() -> str:
    """Get a random cat picture url.

    If cat api is unavailable get a random dog picture url."""
    res = _get_response(CAT_API_URL)

    if res is None:
        res = _get_response(DOG_API_URL)

    if res is None:
        return ''

    res_json = _get_json(res)
    if res_json is None:
        return ''

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
    """Send cat picture on /newcat or if requested."""
    bot.send_message(chat_id=message.chat.id, text='Вам телеграмма!')
    send_cat_picture(message.chat.id)


@bot.message_handler(content_types=['text'])
def reply_default(message: Message) -> None:
    """Reply to text messages."""

    text = message.text

    if text in COMMAND_MAP:
        return COMMAND_MAP[text](message)

    chat_id = message.chat.id
    text = 'Привет, я KittyBot!'
    bot.send_message(chat_id=chat_id, text=text)


COMMAND_MAP = {'Хочу котиков!': send_new_cat}


def main() -> None:
    print('Bot is running!')
    while True:
        try:
            bot.polling()
        except tb.apihelper.ApiException as err:
            logging.error(err)
            time.sleep(600)


if __name__ == '__main__':
    main()
