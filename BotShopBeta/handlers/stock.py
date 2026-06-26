from aiogram import Router
from aiogram.types import CallbackQuery

from database import get_servers_from_db
from keyboards.servers import servers_keyboard


router = Router()


def format_virts(amount: int) -> str:
    return f"{amount:,}".replace(",", ".")


@router.callback_query(lambda c: c.data == "balance")
async def show_stock_servers(call: CallbackQuery):
    await call.message.delete()

    await call.message.answer(
        "🌐 Выберите сервер, чтобы посмотреть наличие виртов.",
        reply_markup=servers_keyboard(page=1, mode="stock")
    )

    await call.answer()


@router.callback_query(lambda c: c.data.startswith("stock_servers_page_"))
async def change_stock_servers_page(call: CallbackQuery):
    page = int(call.data.replace("stock_servers_page_", ""))

    await call.message.edit_text(
        "🌐 Выберите сервер, чтобы посмотреть наличие виртов.",
        reply_markup=servers_keyboard(page=page, mode="stock")
    )

    await call.answer()


@router.callback_query(lambda c: c.data.startswith("stock_s_"))
async def show_server_stock(call: CallbackQuery):
    server_key = call.data.replace("stock_s_", "")
    servers = get_servers_from_db()
    server = servers[server_key]

    stock = server.get("stock", 0)

    await call.answer(
        f'🌐 {server["name"]} [{server["id"]}]\n'
        f'💎 В наличии: {format_virts(stock)} виртов',
        show_alert=True
    )