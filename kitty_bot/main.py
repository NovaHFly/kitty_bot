import logging
from random import choice

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from kitty_bot import config
from kitty_bot.fetcher import ApiRequest

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
)
logging.getLogger().addHandler(logging.StreamHandler())

CAT_API_URL = 'https://api.thecatapi.com/'
DOG_API_URL = 'https://api.thedogapi.com/'

newcat_keyboard = ReplyKeyboardMarkup(
    [['Хочу котиков!', 'Хочу пёсиков!']],
    resize_keyboard=True,
)


def get_random_animal_url(api_url: str) -> str:
    """Get a random animal picture url."""
    api_json = (
        ApiRequest.builder(api_url)
        .paths('v1', 'images', 'search')
        .build()
        .get_json()
    )

    if isinstance(api_json, list):
        if not len(api_json):
            raise ValueError('Empty api json')
        api_json = choice(api_json)

    picture_url = api_json.get('url')
    if not picture_url:
        raise ValueError('Picture url is missing')

    return picture_url


async def send_cat_picture(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Send a random cat picture to chat."""
    try:
        cat_url = get_random_animal_url(CAT_API_URL)
    except ValueError as e:
        logging.error(e)
        await update.message.reply_text('Прости, я не нашёл котиков :-(')
        return

    await update.message.reply_text('Смотри, какого котика я тебе нашёл:')
    await update.message.reply_photo(photo=cat_url)


async def send_dog_picture(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Send a random dog picture to chat."""
    try:
        dog_url = get_random_animal_url(DOG_API_URL)
    except ValueError as e:
        logging.error(e)
        await update.message.reply_text('Собачек сегодня нет :3')
        return

    await update.message.reply_text('Держи своего пёсика :<')
    await update.message.reply_photo(photo=dog_url)


async def greet_user(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Greet user and send them cat picture on /start."""
    name = update.effective_user.first_name

    text = (
        f'Привет, {name}. Я кошкабот. '
        'Я существую для того, чтобы ты увидел котиков.'
    )
    await update.message.reply_text(text, reply_markup=newcat_keyboard)
    await send_cat_picture(update, context)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Мяу! Увидимся!', reply_markup=ReplyKeyboardRemove()
    )


def main() -> None:
    application = Application.builder().token(config.TOKEN).build()

    application.add_handler(
        MessageHandler(
            filters=filters.Text(['Хочу котиков!']),
            callback=send_cat_picture,
        )
    )
    application.add_handler(
        MessageHandler(
            filters=filters.Text(['Хочу пёсиков!']),
            callback=send_dog_picture,
        ),
    )
    application.add_handler(CommandHandler('start', greet_user))
    application.add_handler(CommandHandler('stop', stop))

    application.run_polling()


if __name__ == '__main__':
    main()
