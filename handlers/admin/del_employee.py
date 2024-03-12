from handlers.admin.main import router_admin
from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from data_base import base_employees
from aiogram.filters import Command
from keyboards import keyboard_admin


@router_admin.message(Command('del'))
async def get_employee_funk(message: Message, session: AsyncSession):
    """
    Функция вывода всех сотрудников
    :param message: Message
    :param session: AsyncSession
    :return:
    """
    employees = await base_employees.get_employees(session)
    await message.answer(
        'Сотрудники:',
        reply_markup=keyboard_admin.del_employee(employees)
    )


@router_admin.callback_query(F.data.startswith('del employee_'))
async def del_employee_funk(callback: CallbackQuery, session: AsyncSession,
                            bot: Bot):
    """
    Функция удаления сотрудника
    :param bot: Bot
    :param callback: CallbackQuery
    :param session: AsyncSession
    :return:
    """
    user_id: int = int(callback.data.split('_')[1])
    await base_employees.del_employee(session, user_id)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=f'Сотрудник удален'
    )

    await bot.send_message(
        user_id,
        'Вы удалены из сотрудников'
    )
