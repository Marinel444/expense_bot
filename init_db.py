# init_db.py
import asyncio
from database.db import init_db, async_session
from database.models import Category, Currency


async def seed_data():
    async with async_session() as session:

        default_categories = [
            "Продукты", "Одежда", "Коммунальные",
            "Рестораны", "Развлечения", "Здоровье",
            "Путешествия", "Другое",
        ]
        for name in default_categories:
            session.add(Category(name=name))

        session.add_all([
            Currency(code="UAH", symbol="₴"),
            Currency(code="RON", symbol="lei"),
            Currency(code="USD", symbol="$"),
            Currency(code="EUR", symbol="€"),
        ])

        await session.commit()


async def main():
    await init_db()
    await seed_data()


if __name__ == "__main__":
    asyncio.run(main())
