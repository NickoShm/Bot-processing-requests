from data_base.create_models import Requests
from sqlalchemy.ext.asyncio import AsyncSession


async def add_new_request(session: AsyncSession, data: dict):
    """
    Функция добавления новой заявки в БД
    :param session: AsyncSession
    :param data: dict
    :return:
    """
    obj = Requests(
        user_id=data['user_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        username=data['username'],
        email=data['email'],
        name_parent=data['name_parent'],
        name_student=data['name_student'],
        phone=data['phone'],
        file=data.get('file'),
        description=data['description'],
        status='await',
    )
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj.id


async def add_contractor(session: AsyncSession, request_id: int,
                         user_id: int):
    """
    Функция добавления в БД исполнителя по указанной заявке
    :param session: AsyncSession
    :param request_id: int
    :param user_id: int
    :return:
    """
    request = await session.get(Requests, request_id)
    request.status = 'in work'
    request.contractor = user_id
    await session.commit()
    await session.refresh(request)
    return request


async def update_status_request(session: AsyncSession, request_id: int,
                                status: str):
    """
    Функция обновляет статус заказа
    :param session: AsyncSession
    :param request_id: int
    :param status: str
    :return:
    """
    request = await session.get(Requests, request_id)
    request.status = status
    await session.commit()
    await session.refresh(request)
    return request


async def get_request_by_id(session: AsyncSession, request_id: int):
    """
    Функция получает из БД заявку по ее id
    :param session: AsyncSession
    :param request_id: int
    :return:
    """
    request = await session.get(Requests, request_id)
    return request
