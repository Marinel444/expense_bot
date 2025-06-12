from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.keyboards.categories import get_category_keyboard
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.keyboards.stats_keyboards import get_stats_keyboard
from bot.states import ExpenseStates
from database.models import User
from database.db import async_session
from sqlalchemy import select

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    async with async_session() as session:
        stmt = select(User).where(User.telegram_id == message.from_user.id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)


    await message.answer(
        "Выбери категорию трат:",
        reply_markup=await get_main_menu_keyboard()
    )
    await state.set_state(ExpenseStates.choosing_category)


@router.message(Command("expense"))
async def expense_handler(message: types.Message, state: FSMContext):
    await message.answer(
        "Доступный функционал:",
        reply_markup=await get_category_keyboard()
    )
    await state.set_state(ExpenseStates.choosing_category)


@router.message(Command("stats"))
async def expense_handler(message: types.Message):
    await message.answer(
        "Доступный функционал:",
        reply_markup=await get_stats_keyboard()
    )


@router.message(Command("admin"))
async def expense_handler(message: types.Message, state: FSMContext):
    await message.answer("Password:")
    await state.set_state(ExpenseStates.get_admin)


