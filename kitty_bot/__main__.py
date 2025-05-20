from asyncio import run
from logging import basicConfig as setup_logging, FileHandler, INFO
from os import getenv
from sys import stdout

from uvicorn import Config, Server

from .asgi import starlette_app
from .bot import bot
from .paths import BOT_DATA_PATH


async def main() -> None:
    await bot.set_webhook(
        url=getenv('WEBHOOK_URL'),
        secret_token=getenv('WEBHOOK_TOKEN'),
    )

    webserver = Server(
        config=Config(
            app=starlette_app,
            port=int(getenv('PORT')),
            host=getenv('HOSTNAME'),
        )
    )

    await webserver.serve()


if __name__ == '__main__':
    setup_logging(
        level=INFO,
        stream=stdout,
        handlers=FileHandler(BOT_DATA_PATH / 'main.log'),
    )
    run(main())
