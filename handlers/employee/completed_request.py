from aiogram.enums import ContentType
from handlers.main import router_client
from aiogram import F, Bot
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import CallbackQuery, Message
from data_base import base_requests
from config import ID_ADMIN
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards import keyboard_client, keyboard_admin


class FsmCommitJob(StatesGroup):
    commit = State()


@router_client.callback_query(F.data.startswith('выполнил_'))
async def completed_request_funk(callback: CallbackQuery, state: FSMContext):
    """
    Функция подтверждает, что задание выполнено
    и ввод комментария по выполненной работе
    :param state: FSMContext
    :param callback: CallbackQuery
    :return:
    """
    await callback.answer()
    await state.set_state(FsmCommitJob.commit)
    request_id: int = int(callback.data.split('_')[1])

    mes = await callback.message.answer(
        'Напишите комментарий к выполненной работе',
        reply_markup=keyboard_client.cansel()
    )
    await state.update_data(
        mes=mes.message_id,
        request_id=request_id,
        message_id=callback.message.message_id
    )


@router_client.message(FsmCommitJob.commit)
async def load_commit_completed_request(message: Message, session: AsyncSession,
                                        bot: Bot, state: FSMContext):
    """
    Функция загружает комментарий по выполненной работе
    отправляет исполнителю
    отправляет сотруднику
    :param message: Message
    :param state: FSMContext
    :param session: AsyncSession
    :param bot: Bot
    :return:
    """
    context_data = await state.get_data()
    if message.text == '❌ОТМЕНА':
        await bot.delete_message(message.from_user.id, context_data.get('mes'))
        await state.clear()
        return

    if message.content_type != ContentType.TEXT:
        await message.answer(
            'В этом разделе принимается только текст'
        )
        return
    request_id: int = context_data.get('request_id')
    request = await base_requests.update_status_request(session, request_id,
                                                        'examination')
    message_id: int = context_data.get('message_id')
    if request.file is None:
        await bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=message_id,
            text=f'<b>Заявка №{request.id}</b> '
                 f'пользователя {request.first_name} <b>ВЫПОЛНЕНА</b>'
                 f'\n✅ Почта: <i>{request.email}</i>'
                 f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                 f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                 f'\n✅ Номер телефона: <i>{request.phone}</i>'
                 f'\n✅ Описание ситуации: <i>{request.description}</i>'
                 '\n❌ Файл: <i>не загружался</i>'
        )
        await bot.send_message(
            ID_ADMIN,
            f'<b>Заявка №{request.id}</b> '
            f'пользователя {request.first_name} <b>ВЫПОЛНЕНА</b>'
            f'\n✅ Почта: <i>{request.email}</i>'
            f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
            f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
            f'\n✅ Номер телефона: <i>{request.phone}</i>'
            f'\n✅ Описание ситуации: <i>{request.description}</i>'
            '\n❌ Файл: <i>не загружался</i>'
            '\n\n<b>Комментарий:</b>'
            f'\n{message.text}',
            reply_markup=keyboard_admin.acceptance_of_work(request_id)
        )
        return

    if len(request.file) == 1:
        await bot.edit_message_caption(
            chat_id=message.from_user.id,
            message_id=message_id,
            caption=f'<b>Заявка №{request.id}</b> '
                    f'пользователя {request.first_name} <b>ВЫПОЛНЕНА</b>'
                    f'\n✅ Почта: <i>{request.email}</i>'
                    f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                    f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                    f'\n✅ Номер телефона: <i>{request.phone}</i>'
                    f'\n✅ Описание ситуации: <i>{request.description}</i>'
                    '\n✅ Файл: <i>загружен</i>'
        )

        if request.file[0]['type_file'] == ContentType.PHOTO:
            await bot.send_photo(
                chat_id=ID_ADMIN,
                photo=request.file[0]['file'],
                caption=f'<b>Заявка №{request.id}</b> '
                        f'пользователя {request.first_name} <b>ВЫПОЛНЕНА</b>'
                        f'\n✅ Почта: <i>{request.email}</i>'
                        f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                        f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                        f'\n✅ Номер телефона: <i>{request.phone}</i>'
                        f'\n✅ Описание ситуации: <i>{request.description}</i>'
                        '\n✅ Файл: <i>загружено фото</i>',
                reply_markup=keyboard_admin.acceptance_of_work(request_id)
            )
            return

        if request.file[0]['type_file'] == ContentType.VIDEO:
            await bot.send_video(
                chat_id=ID_ADMIN,
                video=request.file[0]['file'],
                caption=f'<b>Заявка №{request.id}</b> '
                        f'пользователя {request.first_name} <b>ВЫПОЛНЕНА</b>'
                        f'\n✅ Почта: <i>{request.email}</i>'
                        f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                        f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                        f'\n✅ Номер телефона: <i>{request.phone}</i>'
                        f'\n✅ Описание ситуации: <i>{request.description}</i>'
                        '\n✅ Файл: <i>загружено видео</i>',
                reply_markup=keyboard_admin.acceptance_of_work(request_id)
            )
            return

        if request.file[0]['type_file'] == ContentType.VOICE:
            await bot.send_voice(
                chat_id=ID_ADMIN,
                voice=request.file[0]['file'],
                caption=f'<b>Заявка №{request.id}</b> '
                        f'пользователя {request.first_name} <b>ВЫПОЛНЕНА</b>'
                        f'\n✅ Почта: <i>{request.email}</i>'
                        f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                        f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                        f'\n✅ Номер телефона: <i>{request.phone}</i>'
                        f'\n✅ Описание ситуации: <i>{request.description}</i>'
                        '\n✅ Файл: <i>загружено голосовое сообщение</i>',
                reply_markup=keyboard_admin.acceptance_of_work(request_id)
            )
            return

        await bot.send_document(
            chat_id=ID_ADMIN,
            document=request.file[0]['file'],
            caption=f'<b>Заявка №{request.id}</b> '
                    f'пользователя {request.first_name} <b>ВЫПОЛНЕНА</b>'
                    f'\n✅ Почта: <i>{request.email}</i>'
                    f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
                    f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
                    f'\n✅ Номер телефона: <i>{request.phone}</i>'
                    f'\n✅ Описание ситуации: <i>{request.description}</i>'
                    '\n✅ Файл: <i>загружен документ</i>',
            reply_markup=keyboard_admin.acceptance_of_work(request_id)
        )
        return

    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=message_id,
        text=f'<b>Заявка №{request.id}</b> '
             f'пользователя {request.first_name} <b>ВЫПОЛНЕНА</b>'
             f'\n✅ Почта: <i>{request.email}</i>'
             f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
             f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
             f'\n✅ Номер телефона: <i>{request.phone}</i>'
             f'\n✅ Описание ситуации: <i>{request.description}</i>'
             '\n✅ Файл: <i>загружена медиагруппа</i>'
    )
    for i in request.file:
        if i['type_file'] == ContentType.PHOTO:
            await bot.send_photo(
                ID_ADMIN,
                photo=i['file']
            )
        elif i['type_file'] == ContentType.VIDEO:
            await bot.send_video(
                ID_ADMIN,
                video=i['file']
            )
        elif i['type_file'] == ContentType.VOICE:
            await bot.send_voice(
                ID_ADMIN,
                voice=i['file']
            )
        else:
            await bot.send_document(
                ID_ADMIN,
                document=i['file']
            )
    await bot.send_message(
        ID_ADMIN,
        f'<b>Заявка №{request.id}</b> '
        f'пользователя {request.first_name} <b>ВЫПОЛНЕНА</b>'
        f'\n✅ Почта: <i>{request.email}</i>'
        f'\n✅ ФИО родителя: <i>{request.name_parent}</i>'
        f'\n✅ ФИО ученика: <i>{request.name_student}</i>'
        f'\n✅ Номер телефона: <i>{request.phone}</i>'
        f'\n✅ Описание ситуации: <i>{request.description}</i>'
        '\n✅ Файл: <i>загружена медиагруппа</i>',
        reply_markup=keyboard_admin.acceptance_of_work(request_id)
    )
    await state.clear()
