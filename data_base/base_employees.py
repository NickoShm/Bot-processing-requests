from data_base.create_models import Employees
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete


async def add_employee(session: AsyncSession, data: dict):
    """
    Функция добавления менеджеров в БД
    :param session: AsyncSession
    :param data: dict
    :return:
    """
    odj = Employees(
        user_id=data['user_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        username=data['username'],
        status='await'
    )
    session.add(odj)
    await session.commit()


async def get_employees(session: AsyncSession):
    """
    Функция получает из БД менеджеров
    :param session: AsyncSession
    :return:
    """
    query = (select(Employees))
    employees = await session.execute(query)
    return employees.scalars().all()


async def get_employee(session: AsyncSession, user_id: int):
    """
    Функция получает менеджера из БД по его id
    :param session: AsyncSession
    :param user_id: int
    :return:
    """
    employee = await session.get(Employees, user_id)
    return employee


async def update_status_employee(session: AsyncSession, user_id: int,
                                 status: str):
    """
    Функция обновляет статус менеджера в БД
    :param session: AsyncSession
    :param user_id: int
    :param status: str
    :return:
    """
    employee = await session.get(Employees, user_id)
    employee.status = status
    await session.commit()
    await session.refresh(employee)
    return employee


async def del_employee(session: AsyncSession, user_id: int):
    """
    Функция удаляет сотрудника из БД
    :param session: AsyncSession
    :param user_id: int
    :return:
    """
    query = (
        delete(Employees).filter(Employees.user_id == user_id)
    )
    await session.execute(query)
    await session.commit()
