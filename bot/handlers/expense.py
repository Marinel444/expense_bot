from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hitalic
from sqlalchemy import select

from bot.keyboards.categories import get_category_keyboard
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.states import ExpenseStates
from database.models import Expense, Currency, User
from database.db import async_session
from datetime import datetime

from services.currency import get_currency_rate, get_default_currency

router = Router()


@router.callback_query(F.data == "menu_add_expense")
async def handle_add_expense(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Выбери категорию трат:",
        reply_markup=await get_category_keyboard()
    )
    await state.set_state(ExpenseStates.choosing_category)


@router.callback_query(F.data == "exit")
async def exit_button(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Доступный функционал:",
        reply_markup=await get_main_menu_keyboard()
    )
    await state.set_state(ExpenseStates.choosing_category)


@router.callback_query(F.data.startswith("cat_"))
async def category_chosen(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data.split("_")[1]
    if callback_data == "exit":
        await callback.message.delete()
        await state.clear()
        return
    category_id = int(callback_data)
    await state.update_data(category_id=category_id)
    await callback.message.edit_text(
        "Введите данные: \n(пример: описание 100 uah/usd/eur/ron)"
    )
    await state.set_state(ExpenseStates.entering_amount)


@router.message(ExpenseStates.entering_amount)
async def enter_amount(message: types.Message, state: FSMContext):
    try:
        parts = message.text.strip().replace(",", ".").split()
        if not parts:
            raise ValueError("Пустое сообщение")
        if len(parts) == 1:
            amount = float(parts[0])
            description = ""
            currency_code = "UAH"
        elif len(parts) == 2:
            try:
                amount = float(parts[0])
                description = ""
                currency_code = parts[1].upper()
            except ValueError:
                description = parts[0]
                amount = float(parts[1])
                currency_code = "UAH"
        else:
            description = parts[0]
            amount = float(parts[1])
            currency_code = parts[2].upper()
    except Exception:
        await message.delete()
        await message.answer("❌ Неверный формат. Пример: обед 120 usd")
        return

    data = await state.get_data()
    category_id = data.get("category_id")

    async with async_session() as session:
        user_id = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user_id = user_id.scalar_one_or_none()
        result = await session.execute(select(Currency).where(Currency.code == currency_code))
        currency = result.scalar_one_or_none()
        if not currency:
            result = await session.execute(select(Currency).where(Currency.code == "UAH"))
            currency = result.scalar_one()

        amount = round(await get_currency_rate(amount=amount, symbols=currency.code), 2)
        if not amount:
            amount = round(await get_default_currency(amount=amount, symbols=currency.code), 2)

        expense = Expense(
            user_id=user_id.id,
            category_id=category_id,
            amount=amount,
            description=description,
            created_at=datetime.utcnow()
        )
        session.add(expense)
        await session.commit()

    await message.answer(f"✅ Трата {amount} $ сохранена!")
    await state.clear()
