import asyncio
from pydantic import create_model, EmailStr
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from dao.dao import UserDAO, ProfileDAO
from dao.session_maker import connection
from models import Profile


@connection(commit=True)
async def update_username(session: AsyncSession, user_id: int, new_username: str):
    ValueModel = create_model('ValueModel', username=(str, ...))
    await UserDAO.update_one_by_id(session=session,
                                   data_id=user_id,
                                   values=ValueModel(username=new_username))


@connection(commit=True)
async def update_user(session: AsyncSession, user_id: int, new_username: str, email: EmailStr):
    ValueModel = create_model('ValueModel',
                              username=(str, ...),
                              email=(EmailStr, ...))
    await UserDAO.update_one_by_id(session=session,
                                   data_id=user_id,
                                   values=ValueModel(username=new_username, email=email))


@connection(commit=True)
async def update_user_age_username(session: AsyncSession, user_id: int, new_username: str, age: int):
    await UserDAO.update_username_age_by_id(session=session,
                                            data_id=user_id,
                                            username=new_username,
                                            age=age)


@connection(commit=True)
async def update_age_mass(session: AsyncSession, new_age: int, last_name: str):
    try:
        stmt = (
            update(Profile)
            .filter_by(last_name=last_name)
            .values(age=new_age)
        )

        result = await session.execute(stmt)
        updated_count = result.rowcount
        print(f'Обновлено {updated_count} записей')
        return updated_count
    except SQLAlchemyError as e:
        print(f"Error updating profiles: {e}")
        raise


@connection(commit=True)
async def update_age_mass_dao(session: AsyncSession, new_age: int, last_name: str):
    filter_criteria = create_model('FilterModel', last_name=(str, ...))
    values = create_model('ValuesModel', age=(int, ...))
    await ProfileDAO.update_many(session=session,
                                 filter_criteria=filter_criteria(last_name=last_name),
                                 values=values(age=new_age))


asyncio.run(update_age_mass_dao(new_age=33, last_name='Smith'))
