from aiogram.enums import ContentType
from handlers.main import router_client, command_start
from aiogram.types import Message
from aiogram import F, Bot
from keyboards import keyboard_client, keyboard_admin
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import ID_ADMIN
from data_base import base_requests, base_employees
from sqlalchemy.ext.asyncio import AsyncSession


class FsmCreateRequest(StatesGroup):
    """
    почта - email
    ФИО родителя - name_parent
    ФИО ученика - name_student
    номер телефона - phone
    опишите свою ситуацию - description
    файл - file
    проверка - examination

    """
    email = State()
    name_parent = State()
    name_student = State()
    phone = State()
    file = State()
    description = State()
    examination = State()


@router_client.message(F.text == '📩Регистрация заявки')
async def start_create_request(message: Message, state: FSMContext):
    """
    Функция начала создания заявки
    :param state: FSMContext
    :param message: Message
    :return:
    """
    await state.set_state(FsmCreateRequest.email)
    await message.answer(
        '<b>Заполните форму:</b>'
        '\n⭕ Почта'
        '\n⭕ ФИО родителя'
        '\n⭕ ФИО ученика'
        '\n⭕ Номер телефона'
        '\n⭕ Описание ситуации'
        '\n⭕ Файл (скрин, аудио, видео)'
        '\n\nНапишите Вашу почту',
        reply_markup=keyboard_client.cansel()
    )


@router_client.message(FsmCreateRequest.email)
async def load_email(message: Message, state: FSMContext):
    """
    Функция загрузки почты пользователя
    запроса на ФИО
    :param message: Message
    :param state: FSMContext
    :return:
    """
    if message.content_type != ContentType.TEXT:
        await message.answer(
            'Вы должны отправить текст'
        )
        return
    if message.text == '❌ОТМЕНА':
        await command_start(message, state)
        return

    context_state = await state.get_state()
    if context_state == 'FsmCreateRequest:email':
        await state.update_data(email=message.text)
    context_data = await state.get_data()
    await state.set_state(FsmCreateRequest.name_parent)
    await message.answer(
        '<b>Заполните форму:</b>'
        f'\n✅ Почта: <i>{context_data.get("email")}</i>'
        '\n⭕ ФИО родителя'
        '\n⭕ ФИО ученика'
        '\n⭕ Номер телефона'
        '\n⭕ Описание ситуации'
        '\n⭕ Файл (скрин, аудио, видео)'
        '\n\nНапишите ФИО родителя',
        reply_markup=keyboard_client.back_and_cansel()
    )


@router_client.message(FsmCreateRequest.name_parent)
async def load_name_parent(message: Message, state: FSMContext):
    """
    Функция загрузки ФИО родителя
    запроса на номер телефона
    :param message: Message
    :param state: FSMContext
    :return:
    """
    if message.content_type != ContentType.TEXT:
        await message.answer(
            'Вы должны отправить текст'
        )
        return
    if message.text == '❌ОТМЕНА':
        await command_start(message, state)
        return

    context_state = await state.get_state()
    if message.text == '🔙НАЗАД' and context_state == 'FsmCreateRequest:name_parent':
        await start_create_request(message, state)
        return

    if context_state == 'FsmCreateRequest:name_parent':
        await state.update_data(name_parent=message.text)

    await state.set_state(FsmCreateRequest.name_student)

    context_date = await state.get_data()

    await message.answer(
        '<b>Заполните форму:</b>'
        f'\n✅ Почта: <i>{context_date.get("email")}</i>'
        f'\n✅ ФИО родителя: <i>{context_date.get("name_parent")}</i>'
        '\n⭕ ФИО ученика'
        '\n⭕ Номер телефона'
        '\n⭕ Описание ситуации'
        '\n⭕ Файл (скрин, аудио, видео)'
        '\n\nНапишите ФИО ученика',
        reply_markup=keyboard_client.back_and_cansel()
    )


@router_client.message(FsmCreateRequest.name_student)
async def load_name_student(message: Message, state: FSMContext):
    """
    Функция загрузки ФИО пользователя
    запроса на номер телефона
    :param message: Message
    :param state: FSMContext
    :return:
    """
    if message.content_type != ContentType.TEXT:
        await message.answer(
            'Вы должны отправить текст'
        )
        return
    if message.text == '❌ОТМЕНА':
        await command_start(message, state)
        return

    context_state = await state.get_state()
    if message.text == '🔙НАЗАД' and context_state == 'FsmCreateRequest:name_student':
        await load_email(message, state)
        return

    if context_state == 'FsmCreateRequest:name_student':
        await state.update_data(name_student=message.text)

    await state.set_state(FsmCreateRequest.phone)

    context_date = await state.get_data()

    await message.answer(
        '<b>Заполните форму:</b>'
        f'\n✅ Почта: <i>{context_date.get("email")}</i>'
        f'\n✅ ФИО родителя: <i>{context_date.get("name_parent")}</i>'
        f'\n✅ ФИО ученика: <i>{context_date.get("name_student")}</i>'
        '\n⭕ Номер телефона'
        '\n⭕ Описание ситуации'
        '\n⭕ Файл (скрин, аудио, видео)'
        '\n\nНапишите Ваш номер телефона '
        'или нажмите на соответствующую кнопку',
        reply_markup=keyboard_client.phone_back_and_cansel()
    )


@router_client.message(FsmCreateRequest.phone)
async def load_phone(message: Message, state: FSMContext):
    """
    Функция загрузки номера телефона пользователя
    запроса на отправку файла
    :param message: Message
    :param state: FSMContext
    :return:
    """
    if message.content_type != ContentType.TEXT and message.content_type != ContentType.CONTACT:
        await message.answer(
            'Вы должны написать номер телефона или отправить его, нажав на соответствующую кнопку'
        )
        return
    if message.text == '❌ОТМЕНА':
        await command_start(message, state)
        return

    context_state = await state.get_state()
    if message.text == '🔙НАЗАД' and context_state == 'FsmCreateRequest:phone':
        await load_name_parent(message, state)
        return

    if context_state == 'FsmCreateRequest:phone':
        try:
            await state.update_data(phone=message.contact.phone_number)
        except AttributeError:
            await state.update_data(phone=message.text)

    await state.set_state(FsmCreateRequest.description)
    context_date = await state.get_data()
    await message.answer(
        '<b>Заполните форму:</b>'
        f'\n✅ Почта: <i>{context_date.get("email")}</i>'
        f'\n✅ ФИО родителя: <i>{context_date.get("name_parent")}</i>'
        f'\n✅ ФИО ученика: <i>{context_date.get("name_student")}</i>'
        f'\n✅ Номер телефона: <i>{context_date.get("phone")}</i>'
        '\n⭕ Описание ситуации'
        '\n⭕ Файл (скрин, аудио, видео)'
        '\n\nОпишите свою ситуацию',
        reply_markup=keyboard_client.back_and_cansel()
    )


@router_client.message(FsmCreateRequest.description)
async def load_description(message: Message, state: FSMContext):
    """
    Функция загрузки описание проблемы ситуации
    запроса на подтверждение
    :param message: Message
    :param state: FSMContext
    :return:
    """
    if message.content_type != ContentType.TEXT:
        await message.answer(
            'Вы должны описать проблемы ситуации и отправить текст'
        )
        return

    if message.text == '❌ОТМЕНА':
        await command_start(message, state)
        return

    context_state = await state.get_state()
    if message.text == '🔙НАЗАД' and context_state == 'FsmCreateRequest:description':
        await load_name_student(message, state)
        return

    if context_state == 'FsmCreateRequest:description':
        await state.update_data(
            description=message.text,
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
        )

    await state.set_state(FsmCreateRequest.file)
    context_date = await state.get_data()
    await message.answer(
        '<b>Заполните форму:</b>'
        f'\n✅ Почта: <i>{context_date.get("email")}</i>'
        f'\n✅ ФИО родителя: <i>{context_date.get("name_parent")}</i>'
        f'\n✅ ФИО ученика: <i>{context_date.get("name_student")}</i>'
        f'\n✅ Номер телефона: <i>{context_date.get("phone")}</i>'
        f'\n✅ Описание ситуации: <i>{context_date.get("description")}</i>'
        '\n⭕ Файл (скрин, аудио, видео)'
        '\n\nЗагрузите фото, видео, голосовое сообщение или отправьте документ '
        'или пропустите нажав на соответствующую кнопку',
        reply_markup=keyboard_client.back_and_cansel_next()
    )


@router_client.message(FsmCreateRequest.file)
async def load_file(message: Message, state: FSMContext):
    """
    Функция загрузки файла
    :param message: Message
    :param state: FSMContext
    :return:
    """
    if message.text == '❌ОТМЕНА':
        await command_start(message, state)
        return

    context_state = await state.get_state()
    if message.text == '🔙НАЗАД' and context_state == 'FsmCreateRequest:file':
        await load_phone(message, state)
        return

    if message.text == 'ПРОПУСТИТЬ⏭':
        await state.set_state(FsmCreateRequest.examination)
        context_data = await state.get_data()
        await message.answer(
            '<b>Заполните форму:</b>'
            f'\n✅ Почта: <i>{context_data.get("email")}</i>'
            f'\n✅ ФИО родителя: <i>{context_data.get("name_parent")}</i>'
            f'\n✅ ФИО ученика: <i>{context_data.get("name_student")}</i>'
            f'\n✅ Номер телефона: <i>{context_data.get("phone")}</i>'
            f'\n✅ Описание ситуации: <i>{context_data.get("description")}</i>'
            '\n❌ Файл: <i>не загружался</i>'
            '\n\nВсе верно?',
            reply_markup=keyboard_client.back_and_cansel_and_continue()
        )
        return

    if context_state == 'FsmCreateRequest:file':
        if message.content_type == ContentType.TEXT:
            await message.answer(
                'Вы должны загрузить фото, видео, голосовое сообщение, документ '
                'или нажать "ПРОПУСТИТЬ"'
            )
            return
        type_file = message.content_type
        if type_file == ContentType.PHOTO:
            file = message.photo[-1].file_id
        elif type_file == ContentType.VIDEO:
            file = message.video.file_id
        elif type_file == ContentType.VOICE:
            file = message.voice.file_id
        else:
            file = message.document.file_id
        list_files = [
            {
                'file': file,
                'type_file': type_file
            }
        ]
        await state.update_data(
            file=list_files
        )

    await state.set_state(FsmCreateRequest.examination)
    context_data = await state.get_data()
    list_files = context_data.get('file')
    if list_files is None:
        await message.answer(
            '<b>Заполните форму:</b>'
            f'\n✅ Почта: <i>{context_data.get("email")}</i>'
            f'\n✅ ФИО родителя: <i>{context_data.get("name_parent")}</i>'
            f'\n✅ ФИО ученика: <i>{context_data.get("name_student")}</i>'
            f'\n✅ Номер телефона: <i>{context_data.get("phone")}</i>'
            f'\n✅ Описание ситуации: <i>{context_data.get("description")}</i>'
            '\n❌ Файл: <i>не загружался</i>'
            '\n\nВсе верно?',
            reply_markup=keyboard_client.back_and_cansel_and_continue()
        )
        return
    if list_files[0]['type_file'] == ContentType.PHOTO:
        await message.answer_photo(
            photo=list_files[0]['file'],
            caption='<b>Заполните форму:</b>'
                    f'\n✅ Почта: <i>{context_data.get("email")}</i>'
                    f'\n✅ ФИО родителя: <i>{context_data.get("name_parent")}</i>'
                    f'\n✅ ФИО ученика: <i>{context_data.get("name_student")}</i>'
                    f'\n✅ Номер телефона: <i>{context_data.get("phone")}</i>'
                    f'\n✅ Описание ситуации: <i>{context_data.get("description")}</i>'
                    '\n✅ Файл: <i>загружено фото</i>'
                    '\n\nВсе верно?',
            reply_markup=keyboard_client.back_and_cansel_and_continue()
        )
        return

    if list_files[0]['type_file'] == ContentType.VIDEO:
        await message.answer_video(
            video=list_files[0]['file'],
            caption='<b>Заполните форму:</b>'
                    f'\n✅ Почта: <i>{context_data.get("email")}</i>'
                    f'\n✅ ФИО родителя: <i>{context_data.get("name_parent")}</i>'
                    f'\n✅ ФИО ученика: <i>{context_data.get("name_student")}</i>'
                    f'\n✅ Номер телефона: <i>{context_data.get("phone")}</i>'
                    f'\n✅ Описание ситуации: <i>{context_data.get("description")}</i>'
                    '\n✅ Файл: <i>загружено видео</i>'
                    '\n\nВсе верно?',
            reply_markup=keyboard_client.back_and_cansel_and_continue()
        )
        return

    if list_files[0]['type_file'] == ContentType.VOICE:
        await message.answer_voice(
            voice=list_files[0]['file'],
            caption='<b>Заполните форму:</b>'
                    f'\n✅ Почта: <i>{context_data.get("email")}</i>'
                    f'\n✅ ФИО родителя: <i>{context_data.get("name_parent")}</i>'
                    f'\n✅ ФИО ученика: <i>{context_data.get("name_student")}</i>'
                    f'\n✅ Номер телефона: <i>{context_data.get("phone")}</i>'
                    f'\n✅ Описание ситуации: <i>{context_data.get("description")}</i>'
                    '\n✅ Файл: <i>загружено голосовое сообщение</i>'
                    '\n\nВсе верно?',
            reply_markup=keyboard_client.back_and_cansel_and_continue()
        )
        return

    await message.answer_document(
        document=list_files[0]['file'],
        caption='<b>Заполните форму:</b>'
                f'\n✅ Почта: <i>{context_data.get("email")}</i>'
                f'\n✅ ФИО родителя: <i>{context_data.get("name_parent")}</i>'
                f'\n✅ ФИО ученика: <i>{context_data.get("name_student")}</i>'
                f'\n✅ Номер телефона: <i>{context_data.get("phone")}</i>'
                f'\n✅ Описание ситуации: <i>{context_data.get("description")}</i>'
                '\n✅ Файл: <i>загружен документ</i>'
                '\n\nВсе верно?',
        reply_markup=keyboard_client.back_and_cansel_and_continue()
    )


@router_client.message(FsmCreateRequest.examination)
async def load_examination(message: Message, state: FSMContext,
                           bot: Bot, session: AsyncSession):
    """
    Функция подтверждение данных
    отправка заявки админу и в БД
    :param session: AsyncSession
    :param bot: Bot
    :param message: Message
    :param state: FSMContext
    :return:
    """
    context_data = await state.get_data()
    list_files: list = context_data.get('file')
    if message.content_type != ContentType.TEXT:
        type_file = message.content_type
        if type_file == ContentType.PHOTO:
            file = message.photo[-1].file_id
        elif type_file == ContentType.VIDEO:
            file = message.video.file_id
        elif type_file == ContentType.VOICE:
            file = message.voice.file_id
        else:
            file = message.document.file_id
        list_files.append(
            {
                'file': file,
                'type_file': type_file
            }
        )
        await state.update_data(file=list_files)

        for i in list_files:
            if i['type_file'] == ContentType.PHOTO:
                await message.answer_photo(
                    photo=i['file']
                )
            elif i['type_file'] == ContentType.VIDEO:
                await message.answer_video(
                    video=i['file']
                )
            elif i['type_file'] == ContentType.VOICE:
                await message.answer_voice(
                    voice=i['file']
                )
            else:
                await message.answer_document(
                    document=i['file']
                )

        await message.answer(
            '<b>Заполните форму:</b>'
            f'\n✅ Почта: <i>{context_data.get("email")}</i>'
            f'\n✅ ФИО родителя: <i>{context_data.get("name_parent")}</i>'
            f'\n✅ ФИО ученика: <i>{context_data.get("name_student")}</i>'
            f'\n✅ Номер телефона: <i>{context_data.get("phone")}</i>'
            f'\n✅ Описание ситуации: <i>{context_data.get("description")}</i>'
            '\n✅ Файл: <i>загружена медиагруппа</i>'
            '\n\nВсе верно?',
            reply_markup=keyboard_client.back_and_cansel_and_continue()
        )
        return

    if message.text == '❌ОТМЕНА':
        await command_start(message, state)
        return

    context_state = await state.get_state()
    if message.text == '🔙НАЗАД' and context_state == 'FsmCreateRequest:examination':
        await load_description(message, state)
        return

    if message.text == '📨ОТПРАВИТЬ АДМИНУ':
        id_request: int = await base_requests.add_new_request(session, context_data)
        employees = await base_employees.get_employees(session)
        await message.answer(
            '🖇️Ваша заявка принята. Ваш регистрационный номер - '
            f'<b>{id_request}</b>'
        )
        if list_files is None:
            await bot.send_message(
                ID_ADMIN,
                f'<b>Пользователь {message.from_user.first_name} '
                f'отправил заявку</b>'
                f'\n✅ Почта: <i>{context_data.get("email")}</i>'
                f'\n✅ ФИО родителя: <i>{context_data.get("name_parent")}</i>'
                f'\n✅ ФИО ученика: <i>{context_data.get("name_student")}</i>'
                f'\n✅ Номер телефона: <i>{context_data.get("phone")}</i>'
                f'\n✅ Описание ситуации: <i>{context_data.get("description")}</i>'
                '\n❌ Файл: <i>не загружался</i>',
                reply_markup=keyboard_admin.employee_key(employees, id_request)
            )
        elif len(list_files) == 1:
            if list_files[0]['type_file'] == ContentType.PHOTO:
                await bot.send_photo(
                    chat_id=ID_ADMIN,
                    photo=list_files[0]['file'],
                    caption=f'<b>Пользователь {message.from_user.first_name} '
                            f'отправил заявку</b>'
                            f'\n✅ Почта: <i>{context_data.get("email")}</i>'
                            f'\n✅ ФИО родителя: <i>{context_data.get("name_parent")}</i>'
                            f'\n✅ ФИО ученика: <i>{context_data.get("name_student")}</i>'
                            f'\n✅ Номер телефона: <i>{context_data.get("phone")}</i>'
                            f'\n✅ Описание ситуации: <i>{context_data.get("description")}</i>'
                            '\n✅ Файл: <i>загружено фото</i>',
                    reply_markup=keyboard_admin.employee_key(employees, id_request)
                )

            elif list_files[0]['type_file'] == ContentType.VIDEO:
                await bot.send_video(
                    chat_id=ID_ADMIN,
                    video=list_files[0]['file'],
                    caption=f'<b>Пользователь {message.from_user.first_name} '
                            f'отправил заявку</b>'
                            f'\n✅ Почта: <i>{context_data.get("email")}</i>'
                            f'\n✅ ФИО родителя: <i>{context_data.get("name_parent")}</i>'
                            f'\n✅ ФИО ученика: <i>{context_data.get("name_student")}</i>'
                            f'\n✅ Номер телефона: <i>{context_data.get("phone")}</i>'
                            f'\n✅ Описание ситуации: <i>{context_data.get("description")}</i>'
                            '\n✅ Файл: <i>загружено видео</i>',
                    reply_markup=keyboard_admin.employee_key(employees, id_request)
                )

            elif list_files[0]['type_file'] == ContentType.VOICE:
                await bot.send_voice(
                    chat_id=ID_ADMIN,
                    voice=list_files[0]['file'],
                    caption=f'<b>Пользователь {message.from_user.first_name} '
                            f'отправил заявку</b>'
                            f'\n✅ Почта: <i>{context_data.get("email")}</i>'
                            f'\n✅ ФИО родителя: <i>{context_data.get("name_parent")}</i>'
                            f'\n✅ ФИО ученика: <i>{context_data.get("name_student")}</i>'
                            f'\n✅ Номер телефона: <i>{context_data.get("phone")}</i>'
                            f'\n✅ Описание ситуации: <i>{context_data.get("description")}</i>'
                            '\n✅ Файл: <i>загружено голосовое сообщение</i>',
                    reply_markup=keyboard_admin.employee_key(employees, id_request)
                )

            else:
                await bot.send_document(
                    chat_id=ID_ADMIN,
                    document=list_files[0]['file'],
                    caption=f'<b>Пользователь {message.from_user.first_name} '
                            f'отправил заявку</b>'
                            f'\n✅ Почта: <i>{context_data.get("email")}</i>'
                            f'\n✅ ФИО родителя: <i>{context_data.get("name_parent")}</i>'
                            f'\n✅ ФИО ученика: <i>{context_data.get("name_student")}</i>'
                            f'\n✅ Номер телефона: <i>{context_data.get("phone")}</i>'
                            f'\n✅ Описание ситуации: <i>{context_data.get("description")}</i>'
                            '\n✅ Файл: <i>загружен документ</i>',
                    reply_markup=keyboard_admin.employee_key(employees, id_request)
                )

        else:
            for i in list_files:
                if i['type_file'] == ContentType.PHOTO:
                    await message.answer_photo(
                        photo=i['file']
                    )
                elif i['type_file'] == ContentType.VIDEO:
                    await message.answer_video(
                        video=i['file']
                    )
                elif i['type_file'] == ContentType.VOICE:
                    await message.answer_voice(
                        voice=i['file']
                    )
                else:
                    await message.answer_document(
                        document=i['file']
                    )
            await bot.send_message(
                ID_ADMIN,
                f'<b>Пользователь {message.from_user.first_name} '
                f'отправил заявку</b>'
                f'\n✅ Почта: <i>{context_data.get("email")}</i>'
                f'\n✅ ФИО родителя: <i>{context_data.get("name_parent")}</i>'
                f'\n✅ ФИО ученика: <i>{context_data.get("name_student")}</i>'
                f'\n✅ Номер телефона: <i>{context_data.get("phone")}</i>'
                f'\n✅ Описание ситуации: <i>{context_data.get("description")}</i>'
                '\n✅ Файл: <i>загружена медиафайлы</i>',
                reply_markup=keyboard_admin.employee_key(employees, id_request)
            )

        await command_start(message, state)
