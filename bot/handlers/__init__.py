"""Handlerlarni bitta routerga yig'ish."""
from aiogram import Router

from bot.handlers import start, sections, text_query


def get_router() -> Router:
    router = Router()
    router.include_router(start.router)
    router.include_router(sections.router)
    router.include_router(text_query.router)  # matnli savol — oxirgi (fallback)
    return router
