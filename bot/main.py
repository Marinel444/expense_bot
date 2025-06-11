import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import BOT_TOKEN
from database.db import init_db, async_session
from database.models import Category, Currency
from bot.handlers import expense, commands
from sqlalchemy import select


async def seed_data():
    async with async_session() as session:
        result = await session.execute(select(Category))
        if result.scalars().first():
            return  # данные уже есть

        session.add_all([
            Category(name="Продукты"),
            Category(name="Одежда"),
            Category(name="Коммунальные"),
            Category(name="Рестораны"),
            Category(name="Развлечения"),
            Category(name="Здоровье"),
            Category(name="Путешествия"),
            Category(name="Другое"),
        ])
        session.add_all([
            Currency(code="UAH", symbol="₴"),
            Currency(code="RON", symbol="lei"),
            Currency(code="USD", symbol="$"),
            Currency(code="EUR", symbol="€"),
        ])
        await session.commit()


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
    await seed_data()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
