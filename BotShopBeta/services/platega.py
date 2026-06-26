import aiohttp

from config import PLATEGA_API_URL
from config import PLATEGA_MERCHANT_ID
from config import PLATEGA_SECRET


async def platega_request(
    method: str,
    endpoint: str,
    data: dict | None = None
):
    url = f"{PLATEGA_API_URL}/{endpoint.lstrip('/')}"

    headers = {
        "X-MerchantId": PLATEGA_MERCHANT_ID,
        "X-Secret": PLATEGA_SECRET,
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        if method == "POST":
            async with session.post(url, json=data, headers=headers) as response:
                result = await response.json()
                return result

        if method == "GET":
            async with session.get(url, headers=headers) as response:
                result = await response.json()
                return result

    raise ValueError("Неверный HTTP метод")


async def create_platega_payment(
    order_id: int,
    amount: int,
    description: str
):
    data = {
        "paymentDetails": {
            "amount": amount,
            "currency": "RUB"
        },
        "description": description,
        "return": "https://t.me/ТВОЙ_БОТ",
        "failedUrl": "https://t.me/ТВОЙ_БОТ",
        "payload": str(order_id)
    }

    result = await platega_request(
        method="POST",
        endpoint="v2/transaction/process",
        data=data
    )

    return result


async def get_platega_payment_status(transaction_id: str):
    result = await platega_request(
        method="GET",
        endpoint=f"transaction/{transaction_id}"
    )

    return result