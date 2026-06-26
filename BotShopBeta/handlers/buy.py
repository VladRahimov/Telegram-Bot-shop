from aiogram import Router
from aiogram.types import CallbackQuery

from database import get_servers_from_db

from keyboards.servers import servers_keyboard
from keyboards.servers import virts_keyboard
from keyboards.servers import rub_keyboard

from utils.messages import safe_delete_message

router = Router()

from data.user_data import user_data


@router.callback_query(lambda c: c.data == "buy_virt")
async def buy_virt(call: CallbackQuery):

    await safe_delete_message(call.message)

    await call.message.answer(
        text="🌐 Выберите сервер, на котором хотите купить игровую валюту.",
        reply_markup=servers_keyboard(page=1)
    )

    await call.answer()

@router.callback_query(lambda c: c.data.startswith("servers_page_"))
async def change_servers_page(call: CallbackQuery):

    page = int(call.data.replace("servers_page_", ""))

    await call.message.edit_text(
        text="🌐 Выберите сервер, на котором хотите купить игровую валюту.",
        reply_markup=servers_keyboard(page=page)
    )

    await call.answer()

@router.callback_query(lambda c: c.data == "page_info")
async def page_info(call: CallbackQuery):

    await call.answer(
        "Это номер текущей страницы."
    )

@router.callback_query(lambda c: c.data.startswith("s_"))
async def server_picked(call: CallbackQuery):

    server_key = call.data.replace("s_", "")

    servers = get_servers_from_db()
    server = servers[server_key]

    msg = await call.message.answer(

        f"""
🎮Вы выбрали сервер <b>{server["name"]}</b>

💸Цена за 1.000.000 — {server["price"]}₽
<b>Напишите, сколько виртов вы ходите купить.</b>

500.000 — напишите «0.5» или «500000»
1.000.000 — напишите «1» или «1000000»
<b>И так далее...</b>

<b>⚠️Минимальная сумма для покупки — 500.000</b>
""",

        reply_markup=virts_keyboard(server_key),
        parse_mode="HTML"
    )

    user_data[call.from_user.id] = {

        "server": server_key,

        "step": "waiting_virts",

        "input_mode": "virts",

        "message_id": msg.message_id
    }

    await safe_delete_message(call.message)

    await call.answer()


@router.callback_query(lambda c: c.data == "returnToServ")
async def back_to_servers(call: CallbackQuery):

    await call.message.edit_text(
        "🌐 Выберите сервер, на котором хотите купить игровую валюту.",
        reply_markup=servers_keyboard(page=1)
    )

    await call.answer()


@router.callback_query(lambda c: c.data.startswith("transferRub_"))
async def transfer_rub(call: CallbackQuery):

    server_key = call.data.replace("transferRub_", "")

    servers = get_servers_from_db()
    server = servers[server_key]

    user_data[call.from_user.id]["input_mode"] = "rub"

    await call.message.edit_text(

        f"""
🎮Вы выбрали сервер <b>{server["name"]}</b>

<b>Цена за 1.000.000 — 70₽</b>
Укажите сумму в реальных рублях, на которую ходите купить вирты.

<b>⚠️Минимальная сумма для покупки — 35₽</b>
""",

        reply_markup=rub_keyboard(server_key),
        parse_mode="HTML"
    )

    await call.answer()


@router.callback_query(lambda c: c.data.startswith("transferVirt_"))
async def transfer_virt(call: CallbackQuery):

    server_key = call.data.replace("transferVirt_", "")

    servers = get_servers_from_db()
    server = servers[server_key]

    user_data[call.from_user.id]["input_mode"] = "virts"

    await call.message.edit_text(

        f"""
🎮Вы выбрали сервер <b>{server["name"]}</b>

💸Цена за 1.000.000 — {server["price"]}₽
<b>Напишите, сколько виртов вы ходите купить.</b>

500.000 — напишите «0.5» или «500000»
1.000.000 — напишите «1» или «1000000»
<b>И так далее...</b>

<b>⚠️Минимальная сумма для покупки — 500.000</b>

""",

        reply_markup=virts_keyboard(server_key),
        parse_mode="HTML"
    )

    await call.answer()