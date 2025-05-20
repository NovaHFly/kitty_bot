from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

bot = Bot(
    getenv('TELEGRAM_TOKEN'),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dispatcher = Dispatcher()


@dispatcher.message(CommandStart())
async def handle_start_command(message: Message) -> None:
    await message.answer(f'Hello, {html.bold(message.from_user.full_name)}!')


@dispatcher.message()
async def handle_echo(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer('Nice try!')
