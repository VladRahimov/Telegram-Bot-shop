import random

from aiogram import Router
from aiogram.types import CallbackQuery

from database import get_servers_from_db
from data.user_data import user_data

from utils.messages import safe_delete_message
from keyboards.servers import account_amount_keyboard

from keyboards.servers import (
    servers_keyboard,
    account_amount_keyboard,
    account_rub_keyboard
)


router = Router()


@router.callback_query(lambda c: c.data == "buy_account")
async def buy_account(call: CallbackQuery):
    await safe_delete_message(call.message)

    await call.message.answer(
        "🌐 Выберете сервер, на котором хотите купить аккаунт.",
        reply_markup=servers_keyboard(page=1, mode="account")
    )

    await call.answer()


@router.callback_query(lambda c: c.data.startswith("acc_servers_page_"))
async def change_account_servers_page(call: CallbackQuery):
    page = int(call.data.replace("acc_servers_page_", ""))

    await call.message.edit_text(
        "🌐 Выберете сервер, на котором хотите купить аккаунт.",
        reply_markup=servers_keyboard(page=page, mode="account")
    )

    await call.answer()


@router.callback_query(lambda c: c.data == "account_returnToServ")
async def account_return_to_servers(call: CallbackQuery):
    await call.message.edit_text(
        "🌐 Выберете сервер, на котором хотите купить аккаунт.",
        reply_markup=servers_keyboard(page=1, mode="account")
    )

    await call.answer()


@router.callback_query(lambda c: c.data.startswith("acc_s_"))
async def account_server_picked(call: CallbackQuery):
    server_key = call.data.replace("acc_s_", "")
    servers = get_servers_from_db()
    server = servers[server_key]

    price = server["price"] + 30

    order_id = random.randint(100000, 999999)

    msg = await call.message.answer(
        f"""
🎮 Вы выбрали сервер {server["name"]} [{server["id"]}]

💸 Цена за 1.000.000 на аккаунте — {price}₽

Напишите, сколько виртов вы хотите купить на аккаунте.

500.000 — напишите «0.5» или «500000»
1.000.000 — напишите «1» или «1000000»

⚠️ Минимальная сумма для покупки — 500.000
""",
        reply_markup=account_amount_keyboard(server_key)
    )

    user_data[call.from_user.id] = {
        "type": "account",
        "server": server_key,
        "step": "waiting_account_amount",
        "input_mode": "virts",
        "message_id": msg.message_id,
        "order_id": order_id
    }

    await safe_delete_message(call.message)
    await call.answer()


@router.callback_query(lambda c: c.data.startswith("acc_transferRub_"))
async def account_transfer_rub(call: CallbackQuery):
    user_id = call.from_user.id
    if user_id not in user_data:
        await call.answer(
        "Сессия устарела. Начните покупку заново.",
        show_alert=True
        )
        return
    server_key = call.data.replace("acc_transferRub_", "")
    servers = get_servers_from_db()
    server = servers[server_key]

    price = server["price"] + 30

    user_data[user_id]["input_mode"] = "rubles"
    user_data[user_id]["step"] = "waiting_account_amount"

    await call.message.edit_text(
        f"""
🎮 Вы выбрали сервер {server["name"]} [{server["id"]}]

💸 Цена за 1.000.000 на аккаунте — {price}₽

Укажите сумму в реальных рублях, на которую хотите купить вирты.

⚠️ Минимальная сумма для покупки — 35₽
""",
        reply_markup=account_rub_keyboard(server_key)
    )

    await call.answer()


@router.callback_query(lambda c: c.data.startswith("acc_transferVirt_"))
async def account_transfer_virt(call: CallbackQuery):
    user_id = call.from_user.id
    if user_id not in user_data:
        await call.answer(
        "Сессия устарела. Начните покупку заново.",
        show_alert=True
        )
        return
    server_key = call.data.replace("acc_transferVirt_", "")
    servers = get_servers_from_db()
    server = servers[server_key]

    price = server["price"] + 30

    user_data[user_id]["input_mode"] = "virts"
    user_data[user_id]["step"] = "waiting_account_amount"

    await call.message.edit_text(
        f"""
🎮 Вы выбрали сервер {server["name"]} [{server["id"]}]

💸 Цена за 1.000.000 на аккаунте — {price}₽

Напишите, сколько виртов вы хотите купить.

500.000 — напишите «0.5» или «500000»
1.000.000 — напишите «1» или «1000000»

⚠️ Минимальная сумма для покупки — 500.000
""",
        reply_markup=account_amount_keyboard(server_key)
    )

    await call.answer()


@router.callback_query(lambda c: c.data == "back_to_account_amount")
async def back_to_account_amount(call: CallbackQuery):
    user_id = call.from_user.id

    if user_id not in user_data:
        await call.answer(
            "Сессия устарела. Начните покупку заново.",
            show_alert=True
        )
        return

    data = user_data[user_id]

    if data.get("type") != "account":
        await call.answer(
            "Это не заказ аккаунта.",
            show_alert=True
        )
        return

    servers = get_servers_from_db()
    server_key = data["server"]
    server = servers[server_key]

    price = server["price"] + 30

    data["step"] = "waiting_account_amount"
    data["input_mode"] = "virts"

    await call.message.edit_text(
        f"""
🎮 Вы выбрали сервер {server["name"]} [{server["id"]}]

💸 Цена за 1.000.000 на аккаунте — {price}₽

Напишите, сколько виртов вы хотите купить на аккаунте.

500.000 — напишите «0.5» или «500000»
1.000.000 — напишите «1» или «1000000»

⚠️ Минимальная сумма для покупки — 500.000
""",
        reply_markup=account_amount_keyboard(server_key)
    )

    await call.answer()