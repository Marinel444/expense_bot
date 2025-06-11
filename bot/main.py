import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import BOT_TOKEN
from database.db import init_db
from bot.handlers import expense, commands


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    await bot.set_my_commands([
        BotCommand(command="start", description="🟢 Начать заново"),
        BotCommand(command="expense", description="💸 Добавить трату"),
        BotCommand(command="stats", description="📊 Статистика"),
        BotCommand(command="settings", description="⚙️ Настройки"),
    ])

    dp.include_routers(commands.router, expense.router)

    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
