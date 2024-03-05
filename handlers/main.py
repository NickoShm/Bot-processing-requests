from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards import keyboard_client
from aiogram.fsm.context import FSMContext

router_client = Router()


@router_client.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    """
    Функция ответа на команду старт
    :param state: FSMContext
    :param message: Message
    :return:
    """
    await state.clear()
    await message.answer(
        f'Ответ на команду старт',
        reply_markup=keyboard_client.main_menu()
    )
