from handlers.admin.main import router_admin
from aiogram import Bot, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from data_base import base_employees


@router_admin.callback_query(F.data.startswith('employee_'))
async def add_employee_funk(callback: CallbackQuery, session: AsyncSession,
                            bot: Bot):
    """
    Функция добавления нового сотрудника
    при необходимости отказ
    :param bot: Bot
    :param callback: CallbackQuery
    :param session: AsyncSession
    :return:
    """
    action = callback.data.split('_')[1]
    user_id: int = int(callback.data.split('_')[2])
    if action == 'add':
        status = 'active'
    else:
        status = 'close'
    employee = await base_employees.update_status_employee(session, user_id, status)
    if status == 'active':
        await bot.send_message(
            user_id,
            'Вы добавлены в сотрудники'
        )
        await bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            text=f'Пользователь {employee.first_name} добавлен в сотрудники'
        )
        return
    await bot.send_message(
        user_id,
        'Вам отказано в добавлении в сотрудники'
    )
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=f'Пользователю {employee.first_name} отказано в добавлении в сотрудники'
    )
