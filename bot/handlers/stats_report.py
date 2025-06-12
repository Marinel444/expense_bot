from aiogram import Router, types, F
from sqlalchemy import select

from database.db import async_session
from database.models import User

router = Router()


@router.callback_query(F.data.startswith("stats_"))
async def category_chosen(callback: types.CallbackQuery):
    async with async_session() as session:
        stmt = select(User).where(User.telegram_id == callback.from_user.id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user or not user.is_admin:
            await callback.answer("У вас нет прав!", show_alert=True)
            return
        stats = callback.data.split("_")[1]
        if stats == "day":
            print("day")
        elif stats == "week":
            print("week")
        elif stats == "month":
            print("month")


