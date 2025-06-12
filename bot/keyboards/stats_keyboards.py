from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_stats_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📅 День", callback_data="stats_day"),
            InlineKeyboardButton(text="📈 Неделя", callback_data="stats_week"),
            InlineKeyboardButton(text="🗓 Месяц", callback_data="stats_month"),
        ]
    ])

