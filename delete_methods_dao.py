from pydantic import create_model
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from dao.dao import UserDAO
from dao.session_maker import connection
from models import User


@connection(commit=True)
async def delete_user_by_id(session: AsyncSession, user_id: int):
    user = await session.get(User, user_id)
    if user:
        await session.delete(user)


@connection(commit=True)
async def delete_user_by_id_dao(session: AsyncSession, user_id: int):
    await UserDAO.delete_one_by_id(session=session, data_id=user_id)


@connection(commit=True)
async def delete_user_username_ja(session: AsyncSession, start_letter: str = 'ja'):
    stmt = delete(User).where(User.username.like(f"{start_letter}%"))
    await session.execute(stmt)


@connection(commit=True)
async def delete_user_by_password(session: AsyncSession, password: str):
    filter_criteria = create_model('FilterModel', password=(str, ...))
    await UserDAO.delete_many(session=session, filters=filter_criteria(password=password))


@connection(commit=True)
async def delete_all_users(session: AsyncSession):
    await UserDAO.delete_many(session=session, filters=None)
