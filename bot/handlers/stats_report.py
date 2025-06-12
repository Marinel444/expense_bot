from datetime import datetime, timedelta

from aiogram import Router, types, F
from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload

from database.db import async_session
from database.models import User, Expense

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
        if stats == "last":
            stmt = (
                select(Expense).
                options(joinedload(Expense.category)).
                order_by(desc(Expense.created_at)).
                limit(10)
            )
            result = await session.execute(stmt)
            last_stats = result.scalars().all()
            user_answer = ""

            for index, stat in enumerate(last_stats):
                user_answer += (
                    f"{index + 1}.{stat.created_at.strftime('%Y/%m/%d %H:%M')} - {stat.category.name} - "
                    f"{stat.amount} $\n"
                )

            await callback.message.answer(user_answer)
        if stats == "day":
            ten_days_ago = datetime.utcnow() - timedelta(days=10)
            day_stats = select(Expense).where(Expense.created_at >= ten_days_ago)
        elif stats == "week":
            print("week")
        elif stats == "month":
            print("month")


