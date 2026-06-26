import random

from aiogram.types import FSInputFile
from utils.messages import safe_delete_message

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from utils.messages import edit_text_or_caption
from config import ADMIN_CHAT_ID
from data.user_data import user_data
from database import get_servers_from_db
from utils.session import set_session_expire, is_session_expired
from services.crypto_pay import create_crypto_invoice
from services.crypto_pay import get_crypto_invoice

from database import update_order_status

from database import create_order

from keyboards.payment import method_keyboard
from keyboards.payment import trade_method_keyboard
from keyboards.payment import bank_after_payment_keyboard
from keyboards.payment import trade_arrived_keyboard
from keyboards.payment import trade_receive_keyboard
from keyboards.servers import virts_keyboard
from keyboards.payment import admin_payment_check_keyboard
from keyboards.payment import support_keyboard
from keyboards.payment import account_admin_fail_keyboard
from keyboards.payment import (
    payment_methods_keyboard,
    payment_confirm_keyboard,
    card_payment_keyboard
)
from services.platega import create_platega_payment, get_platega_payment_status
from services.crypto_pay import create_crypto_invoice, get_crypto_invoice


router = Router()



@router.callback_query(lambda c: c.data == "method_bank")
async def method_bank(call: CallbackQuery):
    user_id = call.from_user.id

    if user_id not in user_data:
        await call.answer("Сессия устарела. Начните заново.", show_alert=True)
        return

    data = user_data[user_id]

    data["step"] = "waiting_bank"
    data["method"] = "bank"

    await call.message.edit_text(
        """
📝Введите номер вашего банковского счета. 
Если не знаете где его найти, обратитесь в <a href="https://t.me/ScoringPointsBot">Поддержку</a> 💬

⚠️Учтите, при передаче трейдом шанс бана будет меньше.
""",
        reply_markup=method_keyboard(),
        parse_mode="HTML"
    )

    await call.answer()

@router.callback_query(lambda c: c.data == "method_trade")
async def method_trade(call: CallbackQuery):
    user_id = call.from_user.id

    if user_id not in user_data:
        await call.answer("Сессия устарела. Начните заново.", show_alert=True)
        return

    data = user_data[user_id]

    data["step"] = "waiting_nick"
    data["method"] = "trade"

    await call.message.edit_text(
        """
<b>🎮 Введите ваш игровой никнейм, в формате — Nick_Name</b>

🚀Если хотите получить вирты быстрее, выберите получение через банк.🏦
""",
        reply_markup=trade_method_keyboard(),
        parse_mode="HTML"
    )

    await call.answer()

@router.callback_query(lambda c: c.data == "back_to_virts")
async def back_to_virts(call: CallbackQuery):
    user_id = call.from_user.id

    if user_id not in user_data:
        await call.answer("Сессия устарела. Начните заново.", show_alert=True)
        return

    data = user_data[user_id]

    data["step"] = "waiting_virts"
    data["input_mode"] = "virts"

    server_key = data["server"]
    servers = get_servers_from_db()
    server = servers[server_key]

    await call.message.edit_text(
        f"""
🎮Вы выбрали сервер <b>{server["name"]}</b>

💸Цена за 1.000.000 — {server["price"]}₽

<b>Напишите, сколько виртов вы хотите купить.</b>

500.000 — напишите «0.5» или «500000»
1.000.000 — напишите «1» или «1000000»
<b>И так далее...</b>

<b>⚠️Минимальная сумма для покупки — 500.000</b>
""",
        reply_markup=virts_keyboard(server_key),
        parse_mode="HTML"
    )

    await call.answer()


@router.callback_query(lambda c: c.data == "go_payment")
async def go_payment(call: CallbackQuery):
    user_id = call.from_user.id

    if user_id not in user_data:
        await call.answer("Сессия устарела. Начните заново.", show_alert=True)
        return

    data = user_data[user_id]

    if "order_id" not in data:
        data["order_id"] = random.randint(100000, 999999)

    order_id = data["order_id"]
    rubles = data["rubles"]

    data["step"] = "choose_payment_method"

    await call.message.edit_text(
        f"""
💸 <b>Выберите способ оплаты</b>

🆔 Заказ: <code>#{order_id}</code>
💰 Сумма к оплате: <b>{rubles}₽</b>

После оплаты нажмите кнопку:
<b>«Я оплатил ✅»</b>
""",
        reply_markup=payment_methods_keyboard(),
        parse_mode="HTML"
    )

    await call.answer()


@router.callback_query(lambda c: c.data == "pay_platega")
async def pay_platega(call: CallbackQuery):
    user_id = call.from_user.id

    if user_id not in user_data:
        await call.answer("Сессия устарела. Начните заново.", show_alert=True)
        return

    data = user_data[user_id]

    order_id = data["order_id"]
    rubles = data["rubles"]

    payment = await create_platega_payment(
        order_id=order_id,
        amount=rubles,
        description=f"Оплата заказа #{order_id}"
    )

    data["payment_method"] = "platega"
    data["platega_transaction_id"] = payment["transactionId"]
    data["platega_payment_url"] = payment["url"]

    await call.message.edit_text(
        f"""
🇷🇺 СБП [Platega]

🆔 Заказ: <code>{order_id}</code>
💰 Сумма: <b>{rubles}₽</b>

<b>Перед оплатой рекомендуем выключить VPN 🚫</b>

<b>📤 Нажмите кнопку «Перейти к оплате» и оплатите заказ на странице платежной системы ✨</b>
""",
        reply_markup=payment_confirm_keyboard(data["platega_payment_url"]),
        parse_mode="HTML"
    )

    await call.answer()


@router.callback_query(lambda c: c.data == "pay_card_tbank")
async def pay_card_tbank(call: CallbackQuery):
    user_id = call.from_user.id

    if user_id not in user_data:
        await call.answer("Сессия устарела. Начните заново.", show_alert=True)
        return

    data = user_data[user_id]

    order_id = data["order_id"]
    rubles = data["rubles"]

    data["payment_method"] = "card"
    data["card_bank"] = "tbank"
    data["step"] = "waiting_card_receipt"
    data["payment_message_id"] = call.message.message_id

    await call.message.edit_text(
        f"""
<code>{order_id}</code>
🏦 Оплатите <b>{rubles}₽</b> на карту:

💳 Номер: <b><code>2200 7021 8037 8700</code></b>
🏦 Банк: Т-Банк
👤 Получатель: Ярослав Ш.

<b>📤 После оплаты отправьте скриншот чека в этот чат</b>

<b>❗️ Важно: без подтверждения оплаты заказ не будет выполнен.</b>
""",
        reply_markup=card_payment_keyboard("tbank"),
        parse_mode="HTML"
    )

    await call.answer()

@router.callback_query(lambda c: c.data == "pay_card_sber")
async def pay_card_sber(call: CallbackQuery):
    user_id = call.from_user.id

    if user_id not in user_data:
        await call.answer("Сессия устарела. Начните заново.", show_alert=True)
        return

    data = user_data[user_id]

    order_id = data["order_id"]
    rubles = data["rubles"]

    data["payment_method"] = "card"
    data["card_bank"] = "sber"
    data["step"] = "waiting_card_receipt"
    data["payment_message_id"] = call.message.message_id

    await call.message.edit_text(
        f"""
<code>{order_id}</code>
🏦 Оплатите <b>{rubles}₽</b> на карту:

💳 Номер: <b><code>2202 2085 8610 1777</code></b>
🏦 Банк: Сбер
👤 Получатель: Ярослав Ш.

<b>📤 После оплаты отправьте скриншот чека в этот чат</b>

<b>❗️ Важно: без подтверждения оплаты заказ не будет выполнен.</b>
""",
        reply_markup=card_payment_keyboard("sber"),
        parse_mode="HTML"
    )

    await call.answer()

@router.callback_query(lambda c: c.data == "pay_crypto")
async def pay_crypto(call: CallbackQuery):
    user_id = call.from_user.id

    if user_id not in user_data:
        await call.answer("Сессия устарела. Начните заново.", show_alert=True)
        return

    data = user_data[user_id]

    order_id = data["order_id"]
    rubles = data["rubles"]

    invoice = await create_crypto_invoice(
        order_id=order_id,
        rubles=rubles,
        description=f"Оплата заказа #{order_id}"
    )

    data["payment_method"] = "crypto"
    data["crypto_invoice_id"] = invoice["invoice_id"]

    crypto_url = invoice.get("mini_app_invoice_url") or invoice.get("bot_invoice_url")

    await call.message.edit_text(
        f"""
🪙 CryptoBot (оплата криптой) 

🆔 Заказ: <code>{order_id}</code>
💰 Сумма: <b>{rubles}₽</b>

<b>⚡️Нажмите кнопку «Перейти к оплате» и оплатите заказ любой удобной криптовалютой в @send 💸</b>
""",
        reply_markup=payment_confirm_keyboard(crypto_url),
        parse_mode="HTML"
    )

    await call.answer()


@router.callback_query(lambda c: c.data == "back_to_payment_methods")
async def back_to_payment_methods(call: CallbackQuery):
    user_id = call.from_user.id

    if user_id not in user_data:
        await call.answer("Сессия устарела. Начните заново.", show_alert=True)
        return

    data = user_data[user_id]

    order_id = data.get("order_id")
    rubles = data.get("rubles")

    if not order_id or not rubles:
        await call.answer("Данные заказа не найдены. Начните заново.", show_alert=True)
        return

    # Очищаем выбранный способ оплаты
    data.pop("payment_method", None)
    data.pop("platega_transaction_id", None)
    data.pop("platega_payment_url", None)
    data.pop("crypto_invoice_id", None)

    data["step"] = "choose_payment_method"

    await call.message.edit_text(
        f"""
💸 <b>Выберите способ оплаты</b>

🆔 Заказ: <code>#{order_id}</code>
💰 Сумма к оплате: <b>{rubles}₽</b>

После выбора способа оплаты и перевода нажмите:
<b>«Я оплатил ✅»</b>
""",
        reply_markup=payment_methods_keyboard(),
        parse_mode="HTML"
    )

    await call.answer()

def format_virts(amount: int):
    return f"{amount:,}".replace(",", ".")


async def send_card_order_to_admin(message: Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        await message.answer("Сессия устарела. Начните покупку заново.")
        return

    data = user_data[user_id]

    if data.get("card_receipt_sent"):
        await message.answer("✅ Чек уже был отправлен администраторам.")
        return

    servers = get_servers_from_db()

    server_key = data["server"]
    server = servers[server_key]

    order_id = data["order_id"]
    virts = data["virts"]
    rubles = data["rubles"]

    username = message.from_user.username
    username_text = f"@{username}" if username else "Без username"

    card_bank_titles = {
        "tbank": "Т-Банк",
        "sber": "Сбер"
    }

    card_bank = card_bank_titles.get(data.get("card_bank"), "Не указан")

    order_type = data.get("type", "virts")

    try:
        create_order(
            order_id=order_id,
            user_tg_id=user_id,
            username=username_text,
            chat_id=user_id,
            server=server["name"],
            server_id=server["id"],
            virts=virts,
            rubles=rubles
        )
    except Exception as e:
        print("Не удалось создать заказ в БД или заказ уже существует:", e)

    if order_type == "account":
        admin_text = f"""
🛒 <b>Новый заказ аккаунта!</b>

🆔 Заказ: <code>#{order_id}</code>
💳 Способ оплаты: Карта
🏦 Банк: {card_bank}

👤 Покупатель: {username_text}
🆔 Telegram ID: <code>{user_id}</code>

🌐 Сервер: {server["name"]} [{server["id"]}]
💎 Вирты на аккаунте: {format_virts(virts)}
💰 Сумма: {rubles}₽

📎 Чек оплаты прикреплён к этому сообщению.

Если оплата пришла, отправьте данные покупателю сообщением в этот чат:
<code>#{order_id} логин пароль почта и другие данные</code>
"""

        reply_markup = account_admin_fail_keyboard(user_id, order_id)

    else:
        method = data.get("method")

        if method == "bank":
            delivery_text = f"""
📦 Способ получения: Банк
🏦 Номер счёта: <code>{data.get("bank", "Не указан")}</code>
"""
        else:
            delivery_text = f"""
📦 Способ получения: Трейд
👤 Никнейм: <code>{data.get("nick", "Не указан")}</code>
"""

        admin_text = f"""
🛒 <b>Новый заказ!</b>

🆔 Заказ: <code>#{order_id}</code>
💳 Способ оплаты: Карта
🏦 Банк: {card_bank}

👤 Покупатель: {username_text}
🆔 Telegram ID: <code>{user_id}</code>

🌐 Сервер: {server["name"]} [{server["id"]}]
💎 Вирты: {format_virts(virts)}
💰 Сумма: {rubles}₽

{delivery_text}

📎 Чек оплаты прикреплён к этому сообщению.
"""

        reply_markup = admin_payment_check_keyboard(user_id, order_id)

    admin_msg = await message.bot.copy_message(
        chat_id=ADMIN_CHAT_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
        caption=admin_text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

    data["admin_message_id"] = admin_msg.message_id
    data["card_receipt_sent"] = True
    data["step"] = "waiting_admin_payment_check"

    payment_message_id = data.get("payment_message_id")

    if payment_message_id:
        try:
            await message.bot.edit_message_text(
                chat_id=user_id,
                message_id=payment_message_id,
                text=f"""
    ✅ Чек принят.

    🆔 Заказ: <code>#{order_id}</code>
    💰 Сумма: <b>{rubles}₽</b>

    Администратор проверит оплату и продолжит выполнение заказа.
    """,
                parse_mode="HTML"
            )

            data["card_receipt_accept_message_id"] = payment_message_id

        except Exception as e:
            print("Не удалось изменить сообщение оплаты:", e)
            accept_msg = await message.answer(
                f"""
    ✅ Чек принят.

    🆔 Заказ: <code>#{order_id}</code>

    Администратор проверит оплату и продолжит выполнение заказа.
    """,
                parse_mode="HTML"
            )

            data["card_receipt_accept_message_id"] = accept_msg.message_id
    else:
        accept_msg = await message.answer(
            f"""
    ✅ Чек принят.

    🆔 Заказ: <code>#{order_id}</code>

    Администратор проверит оплату и продолжит выполнение заказа.
    """,
            parse_mode="HTML"
        )

        data["card_receipt_accept_message_id"] = accept_msg.message_id


    # Удаляем сам чек из чата покупателя после отправки админу
    try:
        await safe_delete_message(message)
    except Exception as e:
        print("Не удалось удалить чек покупателя:", e)
@router.callback_query(lambda c: c.data == "confirm_payment")
async def confirm_payment(call: CallbackQuery):
    user_id = call.from_user.id
    
    if user_id not in user_data:
        await call.answer(
            "Сессия устарела. Начните заново.",
            show_alert=True
        )
        return

    data = user_data[user_id]

    payment_method = data.get("payment_method")

    if not payment_method:
            await call.answer(
                "❌ Сначала выберите способ оплаты.",
                show_alert=True
                )
            return


    if payment_method == "platega":
        transaction_id = data.get("platega_transaction_id")

        if not transaction_id:
            await call.answer(
                "❌ Платёж не создан. Вернитесь назад и выберите оплату через банк заново.",
                show_alert=True
            )
            return

        try:
            payment_status = await get_platega_payment_status(transaction_id)
        except Exception as e:
            print("Ошибка проверки Platega:", e)
            await call.answer(
                "❌ Не удалось проверить оплату. Попробуйте ещё раз через несколько секунд.",
                show_alert=True
            )
            return

        status = payment_status.get("status")

        if status != "CONFIRMED":
            await call.answer(
                "❌ Оплата через банк пока не найдена.\n\nЕсли вы закрыли окно оплаты и не оплатили заказ — вернитесь назад и выберите способ оплаты заново.",
                show_alert=True
            )
            return


    elif payment_method == "crypto":
        invoice_id = data.get("crypto_invoice_id")

        if not invoice_id:
            await call.answer(
                "❌ Крипто-счёт не создан. Вернитесь назад и выберите оплату криптовалютой заново.",
                show_alert=True
            )
            return

        try:
            invoice = await get_crypto_invoice(invoice_id)
        except Exception as e:
            print("Ошибка проверки CryptoBot:", e)
            await call.answer(
                "❌ Не удалось проверить оплату. Попробуйте ещё раз через несколько секунд.",
                show_alert=True
            )
            return

        if not invoice or invoice.get("status") != "paid":
            await call.answer(
                "❌ Оплата криптовалютой пока не найдена.\n\nЕсли вы закрыли окно оплаты и не оплатили заказ — вернитесь назад и выберите способ оплаты заново.",
                show_alert=True
            )
            return


    elif payment_method == "card":
        await call.answer(
            "Для оплаты картой нужно отправить чек в чат.",
            show_alert=True
        )
        return


    else:
        await call.answer(
            "❌ Неизвестный способ оплаты. Вернитесь назад и выберите способ оплаты заново.",
            show_alert=True
        )
        return


    if user_id not in user_data:
        await call.answer("Сессия устарела. Начните заново.", show_alert=True)
        return

    data = user_data[user_id]
    crypto_invoice_id = data.get("crypto_invoice_id")

    if crypto_invoice_id:
        invoice = await get_crypto_invoice(crypto_invoice_id)

        if not invoice or invoice.get("status") != "paid":
            await call.answer(
                "❌ Оплата криптой пока не найдена. Если оплатили — подождите пару секунд и нажмите снова.",
                show_alert=True
            )
            return
    order_type = data.get("type", "virts")

    servers = get_servers_from_db()
    server_key = data["server"]
    server = servers[server_key]
    virts = data["virts"]
    rubles = data["rubles"]

    if "order_id" not in data:
        data["order_id"] = random.randint(100000, 999999)

    order_id = data["order_id"]

    payment_titles = {
    "platega": "Оплата через банк / Platega",
    "sbp": "СБП / реквизиты",
    "crypto": "Криптовалюта / CryptoBot"
    }

    payment_title = payment_titles.get(data.get("payment_method"), "Не указан")

    card_bank_titles = {
    "tbank": "Т-Банк",
    "sber": "Сбер"
    }

    card_bank = card_bank_titles.get(data.get("card_bank"))

    create_order(
        order_id=order_id,
        user_tg_id=user_id,
        username=call.from_user.username,
        chat_id=call.message.chat.id,
        server=server["name"],
        server_id=server["id"],
        virts=virts,
        rubles=rubles
    )

    

    username = call.from_user.username
    username_text = f"@{username}" if username else "Без username"

    # =========================
    # ПОКУПКА АККАУНТА С ВИРТАМИ
    # =========================

    if order_type == "account":
        admin_text = f"""
🛒 Новый заказ аккаунта!
📦 Тип заказа: <b>покупка аккаунта с виртами</b>
🆔 Заказ: <code>#{order_id}</code>

👤 Покупатель:
{username_text}
🆔 Telegram ID:
<code>{user_id}</code>
🌐 Сервер:
{server["name"]} [{server["id"]}]
💳 Способ оплаты: {payment_title}
{f"🏦 Банк: {card_bank}" if card_bank else ""}

💎 Вирты на аккаунте:
{virts}
💰 Сумма:
{rubles}₽

⭐️ Аккаунт:
3-5 игровой LVL
📍 Рег. данные:
дата и место регистрации
━━━━━━━━━━━━━━
Если оплата пришла, отправьте данные 
покупателю сообщением в этот чат:

<code>#{order_id}</code> логин пароль
"""

        admin_msg = await call.bot.send_message(
            ADMIN_CHAT_ID,
            admin_text,
            reply_markup=account_admin_fail_keyboard(user_id, order_id),
            parse_mode="HTML"
        )

        data["admin_message_id"] = admin_msg.message_id

        await call.message.edit_text(
            f"""
Администратор проверит оплату и продолжит выполнение заказа.

⏳ После проверки оплаты, данные от аккаунта
будут выданы вам в течение 5–30 минут.

⚠️ Внимание — НЕ перезапускайте бота (не нажимайте «/start»)
до завершения текущего заказа.

🆔 Заказ: <code>#{order_id}</code>
""",
            parse_mode="HTML"
        )

        await call.answer(
            "✅ Заказ аккаунта отправлен администрации!",
            show_alert=True
        )

        return

    # =========================
    # ОБЫЧНАЯ ПОКУПКА ВИРТОВ
    # =========================

    admin_text = f"""
🛒 Новый заказ ожидает проверку оплаты!

📦 Тип заказа: <b>покупка виртов</b>

🆔 Заказ: <code>#{order_id}</code>

👤 Покупатель:
{username_text}

🆔 Telegram ID:
<code>{user_id}</code>

🌐 Сервер:
{server["name"]} [{server["id"]}]

💎 Вирты:
{virts}
💳 Способ оплаты: {payment_title}
{f"🏦 Банк: {card_bank}" if card_bank else ""}

💰 Сумма:
{rubles}₽
"""

    if data["method"] == "bank":
        admin_text += f"""

🏦 Счёт:
<code>{data["bank"]}</code>
"""

    elif data["method"] == "trade":
        admin_text += f"""

👤 Никнейм:
<code>{data["nick"]}</code>
"""

    await call.bot.send_message(
        ADMIN_CHAT_ID,
        admin_text,
        reply_markup=admin_payment_check_keyboard(user_id, order_id),
        parse_mode="HTML"
    )

    await call.message.edit_text(
        f"""
Администратор проверит оплату и продолжит выполнение заказа.

⏳ После проверки оплаты, данные от аккаунта
будут выданы вам в течение 5–30 минут.

⚠️ Внимание — НЕ перезапускайте бота (не нажимайте «/start»)
до завершения текущего заказа.

🆔 Заказ: <code>#{order_id}</code>
""",
        parse_mode="HTML"
    )

    await call.answer("✅ Заказ отправлен на проверку оплаты!", show_alert=True)

@router.message(
    lambda message:
    message.from_user
    and message.from_user.id in user_data
    and user_data[message.from_user.id].get("step") == "waiting_card_receipt"
    and (message.photo or message.document)
)
async def receive_card_receipt(message: Message):
    await send_card_order_to_admin(message)

@router.message(
    lambda message:
    message.from_user
    and message.from_user.id in user_data
    and user_data[message.from_user.id].get("step") == "waiting_card_receipt"
)
async def wrong_card_receipt(message: Message):
    await message.answer(
        """
❌ Нужно отправить чек оплаты.

📸 Отправьте фото/скриншот чека
или
📄 отправьте чек файлом/PDF.
"""
    )

async def delete_card_accept_message(bot, buyer_id: int, data: dict):
    accept_message_id = data.get("card_receipt_accept_message_id")

    if not accept_message_id:
        return

    try:
        await bot.delete_message(
            chat_id=buyer_id,
            message_id=accept_message_id
        )
    except Exception as e:
        print("Не удалось удалить сообщение 'Чек принят':", e)

@router.callback_query(lambda c: c.data.startswith("admin_pay_ok_"))
async def admin_pay_ok(call: CallbackQuery):
    print("DEBUG admin_pay_ok нажата:", call.data)

    parts = call.data.split("_")

    try:
        buyer_id = int(parts[3])
        order_id = int(parts[4])
    except Exception as e:
        print("Ошибка разбора callback admin_pay_ok:", e)
        await call.answer("Ошибка данных кнопки.", show_alert=True)
        return

    if buyer_id not in user_data:
        await call.answer(
            "Заказ не найден в памяти бота. Возможно, бот был перезапущен.",
            show_alert=True
        )
        return

    data = user_data[buyer_id]

    await delete_card_accept_message(call.bot, buyer_id, data)

    print("DEBUG order data:", data)

    # Обновляем статус заказа в БД
    try:
        update_order_status(order_id, "🟡 Оплата подтверждена")
    except Exception as e:
        print("Не удалось обновить статус заказа:", e)

    # Обновляем сообщение админа: работает и с текстом, и с фото/файлом с caption
    old_text = call.message.text or call.message.caption or ""
    new_text = old_text + "\n\n✅ <b>ОПЛАТА ПОДТВЕРЖДЕНА</b>"

    try:
        if call.message.text:
            await call.message.edit_text(
                new_text,
                parse_mode="HTML",
                reply_markup=None
            )
        else:
            await call.message.edit_caption(
                caption=new_text,
                parse_mode="HTML",
                reply_markup=None
            )
    except Exception as e:
        print("Не удалось изменить сообщение админа:", e)

    method = data.get("method")

    if method == "bank":
        await call.bot.send_message(
            buyer_id,
            f"""
⏱️ Когда вам придут вирты, не забудьте нажать кнопку «Подтвердить получение».

Если в течение 5 минут вирты не поступят на баланс, обратитесь в поддержку. 🛠️

🆔 Заказ: <code>#{order_id}</code>
""",
            reply_markup=bank_after_payment_keyboard(),
            parse_mode="HTML"
        )

        data["step"] = "waiting_receive_confirm"

    elif method == "trade":
        nick = data.get("nick", "Не указан")

        await call.bot.send_message(
            buyer_id,
            f"""
Ждем вас, <code>{nick}</code>, на спавне города Арзамас.

Не забудьте нажать кнопку «Я приехал 🚗», когда будете на месте.

🆔 Заказ: <code>#{order_id}</code>
""",
            reply_markup=trade_arrived_keyboard(),
            parse_mode="HTML"
        )

        data["step"] = "waiting_arrive"

    else:
        await call.answer(
            "Оплата подтверждена, но способ получения не найден.",
            show_alert=True
        )
        print("ОШИБКА: method не найден в user_data:", data)
        return

    await call.answer(
        "✅ Оплата подтверждена. Покупателю отправлен следующий этап.",
        show_alert=True
    )

@router.callback_query(lambda c: c.data.startswith("admin_pay_fail_"))
async def admin_pay_fail(call: CallbackQuery):
    print("DEBUG admin_pay_fail нажата:", call.data)

    parts = call.data.split("_")

    try:
        buyer_id = int(parts[3])
        order_id = int(parts[4])
    except Exception as e:
        print("Ошибка разбора callback admin_pay_fail:", e)
        await call.answer("Ошибка данных кнопки.", show_alert=True)
        return

    if buyer_id not in user_data:
        await call.answer(
            "Заказ не найден в памяти бота. Возможно, бот был перезапущен.",
            show_alert=True
        )
        return

    data = user_data[buyer_id]

    await delete_card_accept_message(call.bot, buyer_id, data)

    try:
        update_order_status(order_id, "🔴 Отменен")
    except Exception as e:
        print("Не удалось обновить статус заказа:", e)

    old_text = call.message.text or call.message.caption or ""
    new_text = old_text + "\n\n❌ <b>ОПЛАТА НЕ ПРИШЛА</b>"

    try:
        if call.message.text:
            await call.message.edit_text(
                new_text,
                parse_mode="HTML",
                reply_markup=None
            )
        else:
            await call.message.edit_caption(
                caption=new_text,
                parse_mode="HTML",
                reply_markup=None
            )
    except Exception as e:
        print("Не удалось изменить сообщение админа:", e)

    await call.bot.send_message(
        buyer_id,
        f"""
❌ Оплата не подтверждена.

🆔 Заказ: <code>#{order_id}</code>

Если вы уверены, что оплатили заказ —
обратитесь в поддержку.
""",
        reply_markup=support_keyboard(),
        parse_mode="HTML"
    )

    if buyer_id in user_data:
        del user_data[buyer_id]

    await call.answer(
        "❌ Покупателю отправлено сообщение, что оплата не пришла.",
        show_alert=True
    )

@router.callback_query(lambda c: c.data == "arrived_trade")
async def arrived_trade(call: CallbackQuery):
    user_id = call.from_user.id

    if user_id not in user_data:
        await call.answer("Сессия устарела. Начните заново.", show_alert=True)
        return

    data = user_data[user_id]

    if is_session_expired(data):
        del user_data[user_id]

        await call.answer(
            "Сессия устарела. Создайте заказ заново.",
            show_alert=True
        )

        return

    order_id = data.get("order_id", "без номера")
    nick = data.get("nick", "не указан")

    await call.bot.send_message(
        ADMIN_CHAT_ID,
        f"""
🚗 Клиент прибыл и ожидает трейд.

🆔 Заказ: #{order_id}
👤 Никнейм: {nick}
🆔 Telegram ID: {user_id}
"""
    )

    await call.message.edit_text(
        """
Ожидайте, в течении 5-10 минут к вам подойдут и отправят трейд. ⏳

<b>Не уезжайте и не выходите с игры.🖥️</b>

<b>⚠️ После получения валюты не забудьте нажать кнопку «Подтвердить получение»</b>
""",
        reply_markup=trade_receive_keyboard(),
        parse_mode="HTML"
    )

    await call.answer("Администрация уведомлена ✅", show_alert=True)