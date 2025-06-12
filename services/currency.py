import os

import httpx

UAH_USD = os.getenv('UAH_USD')
RON_USD = os.getenv('RON_USD')
EUR_USD = os.getenv('EUR_USD')


async def get_currency_rate(amount: float, symbols: str = "UAH") -> float | None:
    url = "https://open.er-api.com/v6/latest/USD"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            currency = float(data["rates"].get(symbols))
            return amount / currency
        except Exception as e:
            print(f"Ошибка при получении курса: {e}")
            return None


async def get_default_currency(amount: float, symbols: str = "UAH") -> float:
    if symbols == "UAH":
        return amount / float(UAH_USD)
    elif symbols == "RON":
        return amount / float(RON_USD)
    elif symbols == "EUR":
        return amount / float(EUR_USD)
    elif symbols == "USD":
        return amount
