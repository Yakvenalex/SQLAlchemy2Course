from dao.dao import UserDAO
from database import connection
from asyncio import run

from schemas import UserPydantic, UsernameIdPydantic


@connection
async def select_all_users(session):
    return await UserDAO.get_all_users(session)


@connection
async def select_username_id(session):
    return await UserDAO.get_username_id(session)


@connection
async def select_full_user_info(session, user_id):
    rez = await UserDAO.find_one_or_none_by_id(session=session, data_id=user_id)
    if rez:
        return UserPydantic.from_orm(rez).dict()
    return {'message': f'Пользователь с ID {user_id} не найден!'}


@connection
async def select_full_user_info_email(session, user_id, email):
    rez = await UserDAO.find_one_or_none(session=session, id=user_id, email=email)
    if rez:
        return UserPydantic.from_orm(rez).dict()
    return {'message': f'Пользователь с ID {user_id} не найден!'}


info = run(select_full_user_info_email(user_id=21, email='bob.smith@example.com'))
print(info)
