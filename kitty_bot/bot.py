from logging import getLogger
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from .cat_fetcher import get_random_animal_url
from .constants import CAT_API_URL, DOG_API_URL, I_WANT_CATS, I_WANT_DOGS

logger = getLogger('kitty_bot')

bot = Bot(
    getenv('TELEGRAM_TOKEN'),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dispatcher = Dispatcher()


reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=I_WANT_CATS),
            KeyboardButton(text=I_WANT_DOGS),
        ],
    ],
    resize_keyboard=True,
)


@dispatcher.message(F.text == I_WANT_CATS)
async def handle_i_want_cats(message: Message) -> None:
    try:
        cat_url = get_random_animal_url(CAT_API_URL)
    except ValueError as e:
        logger.error(e)
        await message.answer('Прости, я не нашёл котиков :-(')
        return

    await message.answer('Смотри, какого котика я тебе нашёл:')
    await message.answer_photo(photo=cat_url)


@dispatcher.message(F.text == I_WANT_DOGS)
async def handle_i_want_dogs(message: Message) -> None:
    try:
        dog_url = get_random_animal_url(DOG_API_URL)
    except ValueError as e:
        logger.error(e)
        await message.answer('Собачек сегодня нет :3')
        return

    await message.answer('Держи своего пёсика :&lt')
    await message.answer_photo(photo=dog_url)


@dispatcher.message(CommandStart())
async def handle_start_command(message: Message) -> None:
    name = message.from_user.full_name

    text = (
        f'Привет, {name}. Я кошкабот. '
        'Я существую для того, чтобы ты увидел котиков.'
    )
    await message.answer(text, reply_markup=reply_keyboard)
    await handle_i_want_cats(message)


@dispatcher.message(Command('stop'))
async def handle_stop_command(message: Message) -> None:
    await message.answer(
        'Мяу! Увидимся!',
        reply_markup=ReplyKeyboardRemove(),
    )
