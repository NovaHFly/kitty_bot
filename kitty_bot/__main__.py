from asyncio import run
from logging import (
    basicConfig as setup_logging,
    FileHandler,
    INFO,
    StreamHandler,
)
from os import getenv
from sys import stdout

from .asgi import webserver
from .bot import bot
from .paths import BOT_DATA_PATH


async def main() -> None:
    setup_logging(
        level=INFO,
        handlers=[
            FileHandler(BOT_DATA_PATH / 'main.log'),
            StreamHandler(stdout),
        ],
    )
    await bot.set_webhook(
        url=getenv('WEBHOOK_URL'),
        secret_token=getenv('WEBHOOK_TOKEN'),
    )
    await webserver.serve()


if __name__ == '__main__':
    run(main())
