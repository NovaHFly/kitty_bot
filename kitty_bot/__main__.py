import asyncio
import logging
import sys
from os import getenv

from uvicorn import Config, Server

from .asgi import starlette_app
from .bot import bot


async def main() -> None:
    await bot.set_webhook(
        url=getenv('WEBHOOK_URL'),
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
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
