from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select
from database.models import Category
from database.db import async_session


async def get_category_keyboard() -> InlineKeyboardMarkup:
    async with async_session() as session:
        result = await session.execute(select(Category))
        categories = result.scalars().all()

        buttons: list[list[InlineKeyboardButton]] = []
        row: list[InlineKeyboardButton] = []

        for i, category in enumerate(categories, 1):
            row.append(InlineKeyboardButton(
                text=category.name,
                callback_data=f"cat_{category.id}"
            ))
            if i % 3 == 0:
                buttons.append(row)
                row = []
        row.append(InlineKeyboardButton(text="Назад", callback_data="exit"))
        if row:
            buttons.append(row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)
