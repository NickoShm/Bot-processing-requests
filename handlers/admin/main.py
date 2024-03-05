from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


router_admin = Router()


@router_admin.message(Command("admin"))
async def start_admin(message: Message):
    """
    Функция старта меню админа
    :param message:
    :return:
    """
    await message.answer(
        'Меню админа',
    )



