import logging
from typing import Optional

import httpx
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from kitty_bot import config

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
)

CAT_API_URL = 'https://api.thecatapi.com/v1/images/search'
DOG_API_URL = 'https://api.thedogapi.com/v1/images/search'

newcat_keyboard = ReplyKeyboardMarkup(
    [['Хочу котиков!']], resize_keyboard=True
)


def _get_response(url: str) -> Optional[httpx.Response]:
    try:
        return httpx.get(url)
    except Exception as e:
        logging.error(f'Unexpected error while accessing {url}: {e}')
        return None


def _get_json(response: httpx.Response) -> Optional[dict]:
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


async def send_cat_picture(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Send a random cat picture to chat."""
    cat_url = get_cat_url()

    if not cat_url:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Прости, я не нашёл новых картинок :-(',
        )
        return

    await context.bot.send_photo(
        chat_id=update.effective_chat.id, photo=cat_url
    )


async def greet_user(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Greet user and send them cat picture on /start."""
    name = update.effective_user.first_name

    text = f'Привет, {name}. Посмотри, какого котика я тебе нашёл'
    await update.message.reply_text(text, reply_markup=newcat_keyboard)
    await send_cat_picture(update, context)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Мяу!', reply_markup=ReplyKeyboardRemove())


def main() -> None:
    application = Application.builder().token(config.TOKEN).build()

    application.add_handler(
        MessageHandler(
            filters=filters.Text(['Хочу котиков!']), callback=send_cat_picture
        )
    )
    application.add_handler(CommandHandler('start', greet_user))
    application.add_handler(CommandHandler('stop', stop))

    print('Bot is running!')
    application.run_polling()


if __name__ == '__main__':
    main()
