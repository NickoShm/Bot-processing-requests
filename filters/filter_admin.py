from aiogram.filters import Filter
from aiogram import Bot, types
from config import ID_ADMIN


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        return message.from_user.id == ID_ADMIN
