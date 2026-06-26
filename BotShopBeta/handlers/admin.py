from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from config import ADMIN_IDS
from data.admin_states import admin_states
from utils.messages import edit_text_or_caption


from database import (
    add_admin,
    remove_admin,
    is_admin_db,
    update_all_server_prices,
    add_server,
    delete_server_by_name,
    update_server_stock,
    get_all_user_chat_ids
)

from database import get_servers_from_db
from keyboards.admin import admin_servers_keyboard

from config import ADMIN_CHAT_ID
from data.user_data import user_data
from keyboards.payment import account_receive_keyboard


router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS or is_admin_db(user_id)


@router.message(Command("adm"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа.")
        return

    await message.answer(
        """
🛠 Админ-панель

Команды:

/adm_add — добавить админа
/adm_remove — удалить админа

/adm_server_price — изменить цену на всех серверах
/adm_server_add — добавить сервер
/adm_server_delete — удалить сервер

/adm_message — рассылка всем пользователям
/adm_server_virts — изменить наличие виртов
"""
    )


@router.message(Command("adm_add"))
async def adm_add(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа.")
        return

    admin_states[message.from_user.id] = "add_admin"

    await message.answer(
        "Введите Telegram ID аккаунта, которого нужно добавить в админы:"
    )


@router.message(Command("adm_remove"))
async def adm_remove(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа.")
        return

    admin_states[message.from_user.id] = "remove_admin"

    await message.answer(
        "Введите Telegram ID аккаунта, которого нужно удалить из админов:"
    )


@router.message(Command("adm_server_price"))
async def adm_server_price(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа.")
        return

    admin_states[message.from_user.id] = "server_price"

    await message.answer(
        "Введите новую цену за 1.000.000 виртов:"
    )


@router.message(Command("adm_server_add"))
async def adm_server_add(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа.")
        return

    admin_states[message.from_user.id] = "server_add"

    await message.answer(
        "Введите название сервера, который нужно добавить:"
    )


@router.message(Command("adm_server_delete"))
async def adm_server_delete(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа.")
        return

    admin_states[message.from_user.id] = "server_delete"

    await message.answer(
        "Введите название сервера, который нужно удалить:"
    )


@router.message(Command("adm_message"))
async def adm_message(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа.")
        return

    admin_states[message.from_user.id] = "send_message"

    await message.answer(
        "Введите сообщение, которое увидят все зарегистрированные пользователи:"
    )


@router.message(Command("adm_server_virts"))
async def adm_server_virts(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа.")
        return

    await message.answer(
        "🌐 Выберите сервер:",
        reply_markup=admin_servers_keyboard(page=1)
    )


@router.callback_query(lambda c: c.data.startswith("admin_stock_page_"))
async def admin_stock_page(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        await call.answer("Нет доступа.", show_alert=True)
        return

    page = int(call.data.replace("admin_stock_page_", ""))

    await call.message.edit_text(
        "🌐 Выберите сервер:",
        reply_markup=admin_servers_keyboard(page=page)
    )

    await call.answer()


@router.callback_query(lambda c: c.data.startswith("admin_stock_s_"))
async def admin_stock_server(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        await call.answer("Нет доступа.", show_alert=True)
        return

    server_key = call.data.replace("admin_stock_s_", "")

    admin_states[call.from_user.id] = {
        "step": "server_stock",
        "server_key": server_key
    }

    servers = get_servers_from_db()
    server = servers[server_key]

    await call.message.edit_text(
        f"""
🌐 Сервер: {server["name"]} [{server["id"]}]

Введите новое количество доступных виртов:
"""
    )

    await call.answer()


@router.message(lambda message: message.chat.id == ADMIN_CHAT_ID and message.text and message.text.startswith("#"))
async def send_account_data(message: Message):
    print("DEBUG: поймал сообщение с данными аккаунта")
    print("DEBUG chat_id:", message.chat.id)
    print("DEBUG text:", message.text)

    text = message.text.strip()
    parts = text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer(
            "❌ Укажите данные после номера заказа.\n\nПример:\n#123456 login password"
        )
        return

    order_text = parts[0].replace("#", "")

    if not order_text.isdigit():
        await message.answer("❌ Номер заказа должен быть числом.")
        return

    order_id = int(order_text)
    account_data = parts[1]

    buyer_id = None
    order_data = None

    for user_id, data in user_data.items():
        if data.get("order_id") == order_id and data.get("type") == "account":
            buyer_id = user_id
            order_data = data
            break

    if buyer_id is None:
        await message.answer(
            f"""
❌ Заказ #{order_id} не найден.

Возможные причины:
1. бот был перезапущен после создания заказа;
2. это не заказ аккаунта;
3. номер заказа введён неверно;
4. заказ уже завершён или удалён из памяти.
"""
        )
        return

    servers = get_servers_from_db()
    server = servers[order_data["server"]]
    virts = order_data["virts"]

    await message.bot.edit_message_text(
        chat_id=buyer_id,
        message_id=order_data["message_id"],
        text=f"""
Ваши данные входа в аккаунт на {server["name"]} [{server["id"]}] с {virts} виртов:

<code>{account_data}</code>

🖥 После проверки аккаунта, не забудьте нажать на кнопку «Подтвердить получение»
""",
        reply_markup=account_receive_keyboard(),
        parse_mode="HTML"
    )

    admin_message_id = order_data.get("admin_message_id")

    if admin_message_id:
            await edit_text_or_caption(
        bot=message.bot,
        chat_id=ADMIN_CHAT_ID,
        message_id=admin_message_id,
        text=f"""
    🛒 Заказ аккаунта

    🆔 Заказ: <code>#{order_id}</code>

    🌐 Сервер:
    {server["name"]} [{server["id"]}]

    💎 Вирты:
    {virts}

    ✅ Статус: <b>ДАННЫЕ ОТПРАВЛЕНЫ</b>
    """,
        parse_mode="HTML"
    )

    

@router.message(lambda message: message.from_user and message.from_user.id in admin_states)
async def admin_text_handler(message: Message):
    user_id = message.from_user.id

    if user_id not in admin_states:
        return

    if not is_admin(user_id):
        await message.answer("❌ У вас нет доступа.")
        return

    state = admin_states[user_id]

    # =========================
    # ДОБАВИТЬ АДМИНА
    # =========================

    if state == "add_admin":
        if not message.text.isdigit():
            await message.answer("❌ Введите числовой Telegram ID.")
            return

        new_admin_id = int(message.text)

        add_admin(new_admin_id)

        del admin_states[user_id]

        await message.answer(
            f"✅ Админ {new_admin_id} добавлен."
        )

    # =========================
    # УДАЛИТЬ АДМИНА
    # =========================

    elif state == "remove_admin":
        if not message.text.isdigit():
            await message.answer("❌ Введите числовой Telegram ID.")
            return

        remove_admin_id = int(message.text)

        remove_admin(remove_admin_id)

        del admin_states[user_id]

        await message.answer(
            f"✅ Админ {remove_admin_id} удалён."
        )

    # =========================
    # ИЗМЕНИТЬ ЦЕНУ
    # =========================

    elif state == "server_price":
        if not message.text.isdigit():
            await message.answer("❌ Введите цену числом.")
            return

        price = int(message.text)

        update_all_server_prices(price)

        del admin_states[user_id]

        await message.answer(
            f"✅ Цена изменена на {price}₽ за 1.000.000 виртов."
        )

    # =========================
    # ДОБАВИТЬ СЕРВЕР
    # =========================

    elif state == "server_add":
        name = message.text.strip()

        if len(name) < 2:
            await message.answer("❌ Название слишком короткое.")
            return

        new_id = add_server(name)

        del admin_states[user_id]

        if new_id is None:
            await message.answer(
                f"❌ Сервер {name} уже существует."
            )
            return

        await message.answer(
            f"✅ Сервер {name} [{new_id}] добавлен."
        )

    # =========================
    # УДАЛИТЬ СЕРВЕР
    # =========================

    elif state == "server_delete":
        name = message.text.strip()

        deleted = delete_server_by_name(name)

        del admin_states[user_id]

        if deleted:
            await message.answer(
                f"✅ Сервер {name} удалён."
            )
        else:
            await message.answer(
                f"❌ Сервер {name} не найден."
            )

    # =========================
    # РАССЫЛКА
    # =========================

    elif state == "send_message":
        text = message.text

        chat_ids = get_all_user_chat_ids()

        success = 0
        failed = 0

        for chat_id in chat_ids:
            try:
                await message.bot.send_message(
                    chat_id,
                    text
                )
                success += 1

            except Exception:
                failed += 1

        del admin_states[user_id]

        await message.answer(
            f"""
✅ Сообщение отправлено всем зарегистрированным пользователям!

Успешно: {success}
Не отправлено: {failed}
"""
        )

    # =========================
    # ИЗМЕНИТЬ НАЛИЧИЕ ВИРТОВ
    # =========================

    elif isinstance(state, dict) and state.get("step") == "server_stock":
        text = message.text.replace(" ", "")

        if not text.isdigit():
            await message.answer("❌ Введите количество числом.")
            return

        stock = int(text)
        server_key = state["server_key"]

        update_server_stock(server_key, stock)

        del admin_states[user_id]

        await message.answer(
            f"✅ Количество изменено на {stock} виртов."
        )