from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu():
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='📩Регистрация заявки')
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)


def cansel():
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='❌ОТМЕНА')
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)


def back_and_cansel():
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='🔙НАЗАД')
    keyboard.button(text='❌ОТМЕНА')
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)


def phone_back_and_cansel():
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='☎️ОТПРАВИТЬ НОМЕР ТЕЛЕФОНА', request_contact=True)
    keyboard.button(text='🔙НАЗАД')
    keyboard.button(text='❌ОТМЕНА')
    keyboard.adjust(1, 2)
    return keyboard.as_markup(resize_keyboard=True)


def back_and_cansel_next():
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='ПРОПУСТИТЬ⏭')
    keyboard.button(text='🔙НАЗАД')
    keyboard.button(text='❌ОТМЕНА')
    keyboard.adjust(1, 2)
    return keyboard.as_markup(resize_keyboard=True)


def back_and_cansel_and_continue():
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='📨ОТПРАВИТЬ АДМИНУ')
    keyboard.button(text='🔙НАЗАД')
    keyboard.button(text='❌ОТМЕНА')
    keyboard.adjust(1, 1, 2)
    return keyboard.as_markup(resize_keyboard=True)
