from aiogram.utils.keyboard import InlineKeyboardBuilder


def completed(request_id: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Выполнил', callback_data=f'выполнил_{request_id}')
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)
