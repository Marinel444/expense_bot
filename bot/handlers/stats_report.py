from datetime import datetime, timedelta

from aiogram import Router, types, F
from sqlalchemy import select, desc, func
from sqlalchemy.orm import joinedload

from database.db import async_session
from database.models import User, Expense

router = Router()


@router.callback_query(F.data.startswith("stats_"))
async def category_chosen(callback: types.CallbackQuery):
    async with (async_session() as session):
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

            trunc_day_raw = func.date_trunc("day", Expense.created_at)
            trunc_day_labeled = trunc_day_raw.label("day")

            stmt = (
                select(
                    trunc_day_labeled,
                    func.sum(Expense.amount).label("total")
                )
                .where(Expense.created_at >= ten_days_ago)
                .group_by(trunc_day_raw)
                .order_by(trunc_day_raw)
            )

            result = await session.execute(stmt)
            daily_stats = result.all()

            user_answer = "📊 Расходы за последние 10 дней:\n\n"
            total_amount = 0
            for day, total in daily_stats:
                total_amount += float(total)
                user_answer += f"{day.strftime('%Y-%m-%d')}: {total:.2f} $\n"

            user_answer += f"\n💸Всего потраченно: {total_amount:.2f} $\n"

            await callback.message.answer(user_answer)
        elif stats == "week":
            four_weeks_ago = datetime.utcnow() - timedelta(weeks=4)

            trunc_week_raw = func.date_trunc("week", Expense.created_at)
            trunc_week_labeled = trunc_week_raw.label("week")

            stmt = (
                select(
                    trunc_week_labeled,
                    func.sum(Expense.amount).label("total")
                )
                .where(Expense.created_at >= four_weeks_ago)
                .group_by(trunc_week_raw)
                .order_by(trunc_week_raw)
            )

            result = await session.execute(stmt)
            weekly_stats = result.all()

            user_answer = "📆 Расходы по неделям (последние 4):\n\n"
            total_amount = 0
            for week_start, total in weekly_stats:
                week_label = week_start.strftime("%Y-%m-%d")
                total_amount += float(total)
                user_answer += f"🗓️ Неделя с {week_label}: {total:.2f} $\n"
            user_answer += f"\n💸Всего потраченно: {total_amount:.2f} $\n"
            await callback.message.answer(user_answer)
        elif stats == "month":
            now = datetime.utcnow()
            start_of_year = datetime(now.year, 1, 1)

            trunc_month_raw = func.date_trunc("month", Expense.created_at)
            trunc_month_labeled = trunc_month_raw.label("month")

            stmt = (
                select(
                    trunc_month_labeled,
                    func.sum(Expense.amount).label("total")
                )
                .where(Expense.created_at >= start_of_year)
                .group_by(trunc_month_raw)
                .order_by(trunc_month_raw)
            )

            result = await session.execute(stmt)
            monthly_stats = result.all()

            # 📅 Выводим красиво с названием месяца
            import calendar

            user_answer = f"📅 Расходы по месяцам за {now.year}:\n\n"
            total_amount = 0
            for month_start, total in monthly_stats:
                total_amount += float(total)
                month_name = calendar.month_name[month_start.month]
                user_answer += f"📆 {month_name}: {total:.2f} $\n"

            user_answer += f"\n💸Всего потраченно: {total_amount:.2f} $\n"

            await callback.message.answer(user_answer)


