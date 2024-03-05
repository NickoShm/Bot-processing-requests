from aiogram.enums import ContentType
from handlers.admin.main import router_admin
from aiogram.types import CallbackQuery
from data_base import base_requests, base_employees
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot, F
from keyboards import keyboard_employee


@router_admin.callback_query(F.data.startswith('выбрать_'))
async def select_contractor_funk(callback: CallbackQuery, bot: Bot,
                                 session: AsyncSession):
    """
    Функция выбора исполнителя работ по заявке
    :param callback: CallbackQuery
    :param bot: Bot
    :param session: AsyncSession
    :return:
    """
    request_id: int = int(callback.data.split('_')[1])
    user_id: int = int(callback.data.split('_')[2])
    request = await base_requests.add_contractor(session, request_id, user_id)
    user = await base_employees.get_employee(session, user_id)
    if request.file is None:
        await bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            text=f'<b>На заявку №{request.id}</b> '
                 f'пользователя {request.first_name}'
                 f'\n✅ Почта: <i>{request.email}</i>'
                 f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                 f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                 f'\n✅ Номер телефона: <i>{request.phone}</i>'
                 f'\n✅ Описание ситуации: <i>{request.description}</i>'
                 '\n❌ Файл: <i>не загружался</i>'
                 f'\n\nНазначен исполнитель {user.first_name}',
        )
        await bot.send_message(
            user.user_id,
            f'<b>На заявку №{request.id}</b> '
            f'пользователя {request.first_name}'
            f'\n✅ Почта: <i>{request.email}</i>'
            f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
            f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
            f'\n✅ Номер телефона: <i>{request.phone}</i>'
            f'\n✅ Описание ситуации: <i>{request.description}</i>'
            '\n❌ Файл: <i>не загружался</i>'
            f'\n\nВы назначены исполнителем',
            reply_markup=keyboard_employee.completed(request_id)
        )
        return

    if len(request.file) == 1:
        await bot.edit_message_caption(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            caption=f'<b>На заявку №{request.id}</b> '
                    f'пользователя {request.first_name}'
                    f'\n✅ Почта: <i>{request.email}</i>'
                    f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                    f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                    f'\n✅ Номер телефона: <i>{request.phone}</i>'
                    f'\n✅ Описание ситуации: <i>{request.description}</i>'
                    '\n✅ Файл: <i>загружен</i>'
                    f'\n\nНазначен исполнитель {user.first_name}',
        )

        if request.file[0]['type_file'] == ContentType.PHOTO:
            await bot.send_photo(
                chat_id=user.user_id,
                photo=request.file[0]['file'],
                caption=f'<b>На заявку №{request.id}</b> '
                        f'пользователя {request.first_name}'
                        f'\n✅ Почта: <i>{request.email}</i>'
                        f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                        f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                        f'\n✅ Номер телефона: <i>{request.phone}</i>'
                        f'\n✅ Описание ситуации: <i>{request.description}</i>'
                        '\n✅ Файл: <i>загружено фото</i>'
                        f'\n\nВы назначены исполнителем',
                reply_markup=keyboard_employee.completed(request_id)
            )
            return

        if request.file[0]['type_file'] == ContentType.VIDEO:
            await bot.send_video(
                chat_id=user.user_id,
                video=request.file[0]['file'],
                caption=f'<b>На заявку №{request.id}</b> '
                        f'пользователя {request.first_name}'
                        f'\n✅ Почта: <i>{request.email}</i>'
                        f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                        f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                        f'\n✅ Номер телефона: <i>{request.phone}</i>'
                        f'\n✅ Описание ситуации: <i>{request.description}</i>'
                        '\n✅ Файл: <i>загружено видео</i>'
                        f'\n\nВы назначены исполнителем',
                reply_markup=keyboard_employee.completed(request_id)
            )
            return

        if request.file[0]['type_file'] == ContentType.VOICE:
            await bot.send_voice(
                chat_id=user.user_id,
                voice=request.file[0]['file'],
                caption=f'<b>На заявку №{request.id}</b> '
                        f'пользователя {request.first_name}'
                        f'\n✅ Почта: <i>{request.email}</i>'
                        f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                        f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                        f'\n✅ Номер телефона: <i>{request.phone}</i>'
                        f'\n✅ Описание ситуации: <i>{request.description}</i>'
                        '\n✅ Файл: <i>загружено голосовое сообщение</i>'
                        f'\n\nВы назначены исполнителем',
                reply_markup=keyboard_employee.completed(request_id)
            )
            return

        await bot.send_document(
            chat_id=user.user_id,
            document=request.file[0],
            caption=f'<b>На заявку №{request.id}</b> '
                    f'пользователя {request.first_name}'
                    f'\n✅ Почта: <i>{request.email}</i>'
                    f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                    f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                    f'\n✅ Номер телефона: <i>{request.phone}</i>'
                    f'\n✅ Описание ситуации: <i>{request.description}</i>'
                    '\n✅ Файл: <i>загружен документ</i>'
                    f'\n\nВы назначены исполнителем',
            reply_markup=keyboard_employee.completed(request_id)
        )
        return

    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=f'<b>На заявку №{request.id}</b> '
             f'пользователя {request.first_name}'
             f'\n✅ Почта: <i>{request.email}</i>'
             f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
             f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
             f'\n✅ Номер телефона: <i>{request.phone}</i>'
             f'\n✅ Описание ситуации: <i>{request.description}</i>'
             '\n✅ Файл: <i>загружен медиафайл</i>'
             f'\n\nНазначен исполнитель {user.first_name}',
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
        f'<b>На заявку №{request.id}</b> '
        f'пользователя {request.first_name}'
        f'\n✅ Почта: <i>{request.email}</i>'
        f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
        f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
        f'\n✅ Номер телефона: <i>{request.phone}</i>'
        f'\n✅ Описание ситуации: <i>{request.description}</i>'
        '\n✅ Файл: <i>загружена медиафайлы</i>'
        f'\n\nВы назначены исполнителем',
        reply_markup=keyboard_employee.completed(request_id)
    )
