"""
Файл запроса на добавления в сотрудники
"""
from handlers.main import router_client
from aiogram import Bot
from aiogram.types import Message
from config import ID_ADMIN
from keyboards import keyboard_admin
from aiogram.filters import Command
from data_base import base_employees
from sqlalchemy.ext.asyncio import AsyncSession


@router_client.message(Command("add"))
async def add_employee_funk(message: Message, bot: Bot,
                            session: AsyncSession):
    """
    Функция добавления сотрудника
    :param session:
    :param bot:
    :param message:
    :return:
    """
    employee = await base_employees.get_employee(session, message.from_user.id)
    if employee is not None:
        if employee.status == 'active':
            await message.answer(
                'Вы уже зарегистрированы'
            )
            return
        if employee.status == 'close':
            await message.answer(
                'Вы уже пробовали регистрироваться Вам было отказано'
            )
            return
    data = {
        'user_id': message.from_user.id,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'username': message.from_user.username,
    }
    await base_employees.add_employee(session, data)
    await bot.send_message(
        ID_ADMIN,
        f'Пользователь {message.from_user.first_name} '
        f'{message.from_user.last_name} '
        f'{message.from_user.username} '
        f'просит добавить его в сотрудники',
        reply_markup=keyboard_admin.add_employee(message.from_user.id)
    )
    await message.answer(
        'Ваша заявка отправлена'
    )
