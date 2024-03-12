from aiogram.utils.keyboard import InlineKeyboardBuilder


def add_employee(user_id: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text='Добавить', callback_data=f'employee_add_{user_id}')
    keyboard.button(text='Отказать', callback_data=f'employee_del_{user_id}')
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)


def acceptance_of_work(request_id: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text='Принять работу', callback_data=f'принята_{request_id}')
    keyboard.button(text='Отправить на доработку', callback_data=f'доработать_{request_id}')
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)


def employee_key(employees: list, id_request: int):
    keyboard = InlineKeyboardBuilder()

    for employee in employees:
        keyboard.button(text=f'{employee.first_name}',
                        callback_data=f'выбрать_{id_request}_{employee.user_id}')
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)


def del_employee(employees):
    keyboard = InlineKeyboardBuilder()

    for employee in employees:
        keyboard.button(text=f'{employee.first_name}',
                        callback_data=f'del employee_{employee.user_id}')
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)
