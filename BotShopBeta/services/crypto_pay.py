import aiohttp

from config import CRYPTO_PAY_TOKEN, CRYPTO_PAY_API_URL


async def crypto_pay_request(method: str, data: dict | None = None):
    url = f"{CRYPTO_PAY_API_URL}/{method}"

    headers = {
        "Crypto-Pay-API-Token": CRYPTO_PAY_TOKEN
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data or {}, headers=headers) as response:
            result = await response.json()

    if not result.get("ok"):
        raise Exception(result)

    return result["result"]


async def create_crypto_invoice(
    order_id: int,
    rubles: int,
    description: str
):
    invoice = await crypto_pay_request(
        "createInvoice",
        {
            "currency_type": "fiat",
            "fiat": "RUB",
            "amount": str(rubles),
            "accepted_assets": "USDT,TON,BTC,ETH,LTC,TRX,USDC",
            "description": description,
            "payload": str(order_id),
            "allow_comments": False,
            "allow_anonymous": False,
            "expires_in": 1800
        }
    )

    return invoice


async def get_crypto_invoice(invoice_id: int):
    invoices = await crypto_pay_request(
        "getInvoices",
        {
            "invoice_ids": str(invoice_id)
        }
    )

    if not invoices:
        return None

    return invoices[0]