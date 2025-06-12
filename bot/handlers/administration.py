import os

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from bot.states import ExpenseStates
from database.models import User
from database.db import async_session

router = Router()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


@router.message(ExpenseStates.get_admin)
async def enter_amount(message: types.Message, state: FSMContext):
    try:
        user_password = message.text.strip()
        is_admin = ADMIN_PASSWORD == user_password
        if not is_admin:
            raise ValueError("Пустое сообщение")

    except Exception:
        await message.delete()
        await message.answer("❌ Неверный пароль")
        return

    async with async_session() as session:
        user = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = user.scalar_one_or_none()
        if user:
            user.is_admin = True
            await session.commit()
            await message.delete()
            await message.answer(f"✅ Ты стал админом!")
            await state.clear()
            return
        await message.delete()
        await message.answer(f"Не нашли пользователя в базе")
        await state.clear()

