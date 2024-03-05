from aiogram.enums import ContentType
from handlers.admin.main import router_admin
from aiogram.types import CallbackQuery, Message
from data_base import base_requests, base_employees
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot, F
from keyboards import keyboard_employee, keyboard_client
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class FsmFinalizationOfTheOrder(StatesGroup):
    commit = State()


@router_admin.callback_query(F.data.startswith('принята_'))
async def work_accepted(callback: CallbackQuery, bot: Bot,
                        session: AsyncSession):
    """
    Функция работа принята
    :param callback: CallbackQuery
    :param bot: Bot
    :param session: AsyncSession
    :return:
    """
    request_id: int = int(callback.data.split('_')[1])
    request = await base_requests.update_status_request(session, request_id, 'completed')
    await bot.send_message(
        request.contractor,
        f'<b>Заявка №{request.id}</b>'
        f'\nпользователя {request.first_name} '
        f'ЗАКРЫТА'
    )
    await bot.send_message(
        request.user_id,
        f'<b>Заявка №{request.id}</b>'
        f'\nпользователя {request.first_name} '
        f'ЗАКРЫТА'
    )
    if request.file is None or len(request.file) > 1:
        await bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            text=f'<b>Заявка №{request.id}</b>'
                 f'\nпользователя {request.first_name} '
                 f'ЗАКРЫТА'
        )
        return
    await bot.edit_message_caption(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        caption=f'<b>Заявка №{request.id}</b>'
                f'\nпользователя {request.first_name} '
                f'ЗАКРЫТА',
    )


@router_admin.callback_query(F.data.startswith('доработать_'))
async def finalization_of_the_order(callback: CallbackQuery, state: FSMContext):
    """
    Функция работа требует доработки
    :param state: FSMContext
    :param callback: CallbackQuery
    :return:
    """
    await callback.answer()
    await state.set_state(FsmFinalizationOfTheOrder.commit)
    request_id: int = int(callback.data.split('_')[1])

    mes = await callback.message.answer(
        'Напишите комментарий к выполненной работе '
        '(что необходимо переделать)',
        reply_markup=keyboard_client.cansel()
    )
    await state.update_data(
        mes=mes.message_id,
        request_id=request_id,
        message_id=callback.message.message_id
    )


@router_admin.message(FsmFinalizationOfTheOrder.commit)
async def finalization_of_the_order(message: Message, bot: Bot,
                                    session: AsyncSession, state: FSMContext):
    """
    Функция выбора исполнителя работ по заявке
    :param message: Message
    :param state: FSMContext
    :param bot: Bot
    :param session: AsyncSession
    :return:
    """
    context_data = await state.get_data()
    if message.text == '❌ОТМЕНА':
        await bot.delete_message(message.from_user.id, context_data.get('mes'))
        await state.clear()
        return
    request_id: int = context_data.get('request_id')
    message_id: int = context_data.get('message_id')
    request = await base_requests.update_status_request(session, request_id, 'revision')
    user = await base_employees.get_employee(session, request.contractor)
    if request.file is None:
        await bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=message_id,
            text=f'<b>Заявка №{request.id}</b> пользователя {request.first_name}'
                 f'\nОтправлена на доработку'
                 f'\n✅ Почта: <i>{request.email}</i>'
                 f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                 f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                 f'\n✅ Номер телефона: <i>{request.phone}</i>'
                 f'\n✅ Описание ситуации: <i>{request.description}</i>'
                 '\n❌ Файл: <i>не загружался</i>'
                 f'\n\nИсполнитель {user.first_name}',
        )
        await bot.send_message(
            user.user_id,
            f'<b>Заявка №{request.id}</b> пользователя {request.first_name}'
            f'\nОтправлена на доработку'
            f'\n✅ Почта: <i>{request.email}</i>'
            f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
            f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
            f'\n✅ Номер телефона: <i>{request.phone}</i>'
            f'\n✅ Описание ситуации: <i>{request.description}</i>'
            '\n❌ Файл: <i>не загружался</i>'
            f'\n\nВы назначены исполнителем'
            f'\n\n<b>Комментарий:</b>'
            f'{message.text}',
            reply_markup=keyboard_employee.completed(request_id)
        )
        return

    if len(request.file) == 1:
        await bot.edit_message_caption(
            chat_id=message.from_user.id,
            message_id=message_id,
            caption=f'<b>Заявка №{request.id}</b> пользователя {request.first_name}'
                    f'\nОтправлена на доработку'
                    f'\n✅ Почта: <i>{request.email}</i>'
                    f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                    f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                    f'\n✅ Номер телефона: <i>{request.phone}</i>'
                    f'\n✅ Описание ситуации: <i>{request.description}</i>'
                    '\n✅ Файл: <i>загружен</i>'
                    f'\n\nИсполнитель {user.first_name}',
        )

        if request.file[0]['type_file'] == ContentType.PHOTO:
            await bot.send_photo(
                chat_id=user.user_id,
                photo=request.file[0]['file'],
                caption=f'<b>Заявка №{request.id}</b> пользователя {request.first_name}'
                        f'\nОтправлена на доработку'
                        f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                        f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                        f'\n✅ Номер телефона: <i>{request.phone}</i>'
                        f'\n✅ Описание ситуации: <i>{request.description}</i>'
                        '\n✅ Файл: <i>загружено фото</i>'
                        f'\n\nВы назначены исполнителем'
                        f'\n\n<b>Комментарий:</b>'
                        f'{message.text}',
                reply_markup=keyboard_employee.completed(request_id)
            )
            return

        if request.file[0]['type_file'] == ContentType.VIDEO:
            await bot.send_video(
                chat_id=user.user_id,
                video=request.file[0]['file'],
                caption=f'<b>Заявка №{request.id}</b> пользователя {request.first_name}'
                        f'\nОтправлена на доработку'
                        f'\n✅ Почта: <i>{request.email}</i>'
                        f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                        f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                        f'\n✅ Номер телефона: <i>{request.phone}</i>'
                        f'\n✅ Описание ситуации: <i>{request.description}</i>'
                        '\n✅ Файл: <i>загружено видео</i>'
                        f'\n\nВы назначены исполнителем'
                        f'\n\n<b>Комментарий:</b>'
                        f'{message.text}',
                reply_markup=keyboard_employee.completed(request_id)
            )
            return

        if request.file[0]['type_file'] == ContentType.VOICE:
            await bot.send_voice(
                chat_id=user.user_id,
                voice=request.file[0]['file'],
                caption=f'<b>Заявка №{request.id}</b> пользователя {request.first_name}'
                        f'\nОтправлена на доработку'
                        f'\n✅ Почта: <i>{request.email}</i>'
                        f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                        f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                        f'\n✅ Номер телефона: <i>{request.phone}</i>'
                        f'\n✅ Описание ситуации: <i>{request.description}</i>'
                        '\n✅ Файл: <i>загружено голосовое сообщение</i>'
                        f'\n\nВы назначены исполнителем'
                        f'\n\n<b>Комментарий:</b>'
                        f'{message.text}',
                reply_markup=keyboard_employee.completed(request_id)
            )
            return

        await bot.send_document(
            chat_id=user.user_id,
            document=request.file[0],
            caption=f'<b>Заявка №{request.id}</b> пользователя {request.first_name}'
                    f'\nОтправлена на доработку'
                    f'\n✅ Почта: <i>{request.email}</i>'
                    f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                    f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                    f'\n✅ Номер телефона: <i>{request.phone}</i>'
                    f'\n✅ Описание ситуации: <i>{request.description}</i>'
                    '\n✅ Файл: <i>загружен документ</i>'
                    f'\n\nВы назначены исполнителем'
                    f'\n\n<b>Комментарий:</b>'
                    f'{message.text}',
            reply_markup=keyboard_employee.completed(request_id)
        )
        return

    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=message_id,
        text=f'<b>Заявка №{request.id}</b> пользователя {request.first_name}'
             f'\nОтправлена на доработку'
             f'\n✅ Почта: <i>{request.email}</i>'
             f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
             f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
             f'\n✅ Номер телефона: <i>{request.phone}</i>'
             f'\n✅ Описание ситуации: <i>{request.description}</i>'
             '\n❌ Файл: <i>загружен медиафайл</i>'
             f'\n\nНазначен исполнитель {user.first_name}'
             f'\n\n<b>Комментарий:</b>'
             f'{message.text}',
    )

    for i in request.file:
        if i['type_file'] == ContentType.PHOTO:
            await bot.send_photo(
                user.user_id,
                photo=i['file']
            )
        elif i['type_file'] == ContentType.VIDEO:
            await bot.send_video(
                user.user_id,
                video=i['file']
            )
        elif i['type_file'] == ContentType.VOICE:
            await bot.send_voice(
                user.user_id,
                voice=i['file']
            )
        else:
            await bot.send_document(
                user.user_id,
                document=i['file']
            )
    await bot.send_message(
        user.user_id,
        f'<b>Заявка №{request.id}</b> пользователя {request.first_name}'
        f'\nОтправлена на доработку'
        f'\n✅ Почта: <i>{request.email}</i>'
        f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
        f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
        f'\n✅ Номер телефона: <i>{request.phone}</i>'
        f'\n✅ Описание ситуации: <i>{request.description}</i>'
        '\n✅ Файл: <i>загружена медиафайлы</i>'
        f'\n\nВы назначены исполнителем'
        f'\n\n<b>Комментарий:</b>'
        f'{message.text}',
        reply_markup=keyboard_employee.completed(request_id)
    )
    await state.clear()
