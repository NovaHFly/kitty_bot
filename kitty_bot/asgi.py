from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Route

from .bot import bot, dispatcher


async def webhook(request: Request) -> Response:
    update_json = await request.json()
    await dispatcher.feed_webhook_update(update=update_json, bot=bot)
    return Response()


async def check_health(_: Request) -> PlainTextResponse:
    return PlainTextResponse(content='Bot is still running.')


starlette_app = Starlette(
    routes=[
        Route('/', webhook, methods=['POST']),
        Route('/healthcheck/', check_health, methods=['GET']),
    ]
)
