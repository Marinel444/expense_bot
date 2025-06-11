from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить трату", callback_data="menu_add_expense")]
    ])
