from aiogram import Router
from aiogram.types import Message
import re

from data.user_data import user_data
from database import get_servers_from_db

from keyboards.payment import method_keyboard
from keyboards.payment import order_confirm_keyboard

from config import REVIEW_CHAT_ID
from keyboards.reviev import after_review_keyboard
from keyboards.servers import account_amount_keyboard, account_rub_keyboard
from config import ADMIN_CHAT_ID
from utils.messages import safe_delete_message
from keyboards.payment import account_order_confirm_keyboard
from keyboards.payment import trade_method_keyboard


router = Router()



@router.message()
async def handle_text(message: Message):

    if message.chat.id == ADMIN_CHAT_ID:
        return

    if message.text and message.text.startswith("#"):
        return

    

    user_id = message.from_user.id

    if user_id not in user_data:
        return

    data = user_data[user_id]

    step = data["step"]

    servers = get_servers_from_db()

    # =========================
    # ВВОД СУММЫ
    # =========================

    if step == "waiting_virts":

        text = message.text.replace(",", ".")

        servers = get_servers_from_db()
        server_key = data["server"]
        server = servers[server_key]
        mode = data["input_mode"]

        # =========================
        # Если ввели не число
        # =========================

        try:
            value = float(text)

        except ValueError:
            await safe_delete_message(message)

            if mode == "virts":
                from keyboards.servers import virts_keyboard

                await message.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=data["message_id"],
                    text=f"""
❌ Введите число.

🎮 Вы выбрали сервер <b>{server["name"]}</b>

💸 Цена за 1.000.000 — {server["price"]}₽

<b>Напишите, сколько виртов вы хотите купить.</b>

500.000 — напишите «0.5» или «500000»
1.000.000 — напишите «1» или «1000000»
<b>И так далее...</b>

<b>⚠️ Минимальная сумма для покупки — 500.000</b>
""",
                    reply_markup=virts_keyboard(data["server"]),
                    parse_mode="HTML"
                )

            else:
                from keyboards.servers import rub_keyboard

                await message.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=data["message_id"],
                    text=f"""
<b>❌ Введите число.</b>

🎮 Вы выбрали сервер <b>{server["name"]}</b>

💸 Цена за 1.000.000 — {server["price"]}₽

Укажите сумму в рублях, на которую хотите купить вирты.

<b>⚠️ Минимальная сумма для покупки — 35₽</b>
""",
                    reply_markup=rub_keyboard(data["server"]),
                    parse_mode="HTML"
                )

            return

        # =========================
        # Ввод в виртах
        # =========================

        if mode == "virts":

            # Если человек пишет 0.5 / 1 / 2 — считаем это миллионами
            if value < 201:
                value = value * 1000000

            

            virts = int(value)

            if virts < 500000:
                await safe_delete_message(message)

                from keyboards.servers import virts_keyboard

                await message.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=data["message_id"],
                    text=f"""
❌ Минимальная сумма: <b>500.000 виртов.</b>

🎮 Вы выбрали сервер <b>{server["name"]}</b>

💸 Цена за 1.000.000 — {server["price"]}₽

<b>Напишите, сколько виртов вы хотите купить.</b>

500.000 — напишите «0.5» или «500000»
1.000.000 — напишите «1» или «1000000»
<b>И так далее...</b>

<b>⚠️ Минимальная сумма для покупки — 500.000</b>
""",
                    reply_markup=virts_keyboard(data["server"]),
                    parse_mode="HTML"
                )

                return


            if virts > 200000000:
                await safe_delete_message(message)
                from keyboards.servers import virts_keyboard
                await message.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=data["message_id"],
                    text=f"""
❌ Максимальная сумма: <b>200.000.000 виртов.</b>

🎮 Вы выбрали сервер <b>{server["name"]}</b>

💸 Цена за 1.000.000 — {server["price"]}₽

<b>Напишите, сколько виртов вы хотите купить.</b>

500.000 — напишите «0.5» или «500000»
1.000.000 — напишите «1» или «1000000»
<b>И так далее...</b>

<b>⚠️ Минимальная сумма для покупки — 500.000</b>
""",
                    reply_markup=virts_keyboard(data["server"]),
                    parse_mode="HTML"
                )

                return

            rubles = round((virts / 1000000) * server["price"])

        # =========================
        # Ввод в рублях
        # =========================

        else:

            rubles = int(value)

            if rubles < 1:
                await safe_delete_message(message)

                from keyboards.servers import rub_keyboard

                await message.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=data["message_id"],
                    text=f"""
❌ Минимальная сумма: <b>35₽.</b>

🎮 Вы выбрали сервер <b>{server["name"]}</b>

💸 Цена за 1.000.000 — {server["price"]}₽

Укажите сумму в рублях, на которую хотите купить вирты.

<b>⚠️ Минимальная сумма для покупки — 35₽</b>
""",
                    reply_markup=rub_keyboard(data["server"]),
                    parse_mode="HTML"
                )

                return

            if rubles > 14000:
                await safe_delete_message(message)
                from keyboards.servers import rub_keyboard
                await message.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=data["message_id"],
                    text=f"""
❌ Максимальная сумма: <b>14.000₽.</b>

🎮 Вы выбрали сервер <b>{server["name"]}</b>

💸 Цена за 1.000.000 — {server["price"]}₽

Укажите сумму в рублях, на которую хотите купить вирты.

<b>⚠️ Минимальная сумма для покупки — 35₽</b>
""",
                    reply_markup=rub_keyboard(data["server"]),
                    parse_mode="HTML"
                )

                return

            virts = round((rubles / server["price"]) * 1000000)

        data["virts"] = virts
        data["rubles"] = rubles
        data["step"] = "waiting_bank"

        await safe_delete_message(message)

        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["message_id"],
            text="""
<b>📝Введите номер вашего банковского счета.</b>

Если не знаете где его найти, обратитесь в <a href="https://t.me/ScoringPointsBot">Поддержку</a>:
 💬

<b>⚠️Учтите, при передаче трейдом шанс бана будет меньше.</b>
""",
            reply_markup=method_keyboard(),
            parse_mode="HTML"
        )


    elif step == "waiting_account_amount":

        text = message.text.replace(",", ".")

        servers = get_servers_from_db()
        server_key = data["server"]
        server = servers[server_key]
        price = server["price"] + 30
        mode = data["input_mode"]

        try:
            value = float(text)

        except ValueError:
            await safe_delete_message(message)

            await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=data["message_id"],
                text=f"""
    ❌ Введите число.

    🎮 Вы выбрали сервер {server["name"]} [{server["id"]}]

    💸 Цена за 1.000.000 на аккаунте — {price}₽

    Напишите сумму корректно.
    """,
                reply_markup=account_amount_keyboard(data["server"])
            )

            return

        if mode == "virts":

            if value < 201:
                value = value * 1000000

            virts = int(value)

            if virts < 500000:
                await safe_delete_message(message)

                await message.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=data["message_id"],
                    text=f"""
    ❌ Минимальная сумма: 500.000 виртов.

    🎮 Вы выбрали сервер {server["name"]} [{server["id"]}]

    💸 Цена за 1.000.000 на аккаунте — {price}₽
    """,
                    reply_markup=account_amount_keyboard(data["server"])
                )

                return

            if virts > 200000000:
                await safe_delete_message(message)

                await message.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=data["message_id"],
                    text=f"""
    ❌ Максимальная сумма: 200.000.000 виртов.

    🎮 Вы выбрали сервер {server["name"]} [{server["id"]}]

    💸 Цена за 1.000.000 на аккаунте — {price}₽
    """,
                    reply_markup=account_amount_keyboard(data["server"])
                )

                return

            rubles = round((virts / 1000000) * price)

        else:

            rubles = int(value)

            if rubles < 35:
                await safe_delete_message(message)

                await message.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=data["message_id"],
                    text=f"""
    ❌ Минимальная сумма: 35₽.

    🎮 Вы выбрали сервер {server["name"]} [{server["id"]}]

    💸 Цена за 1.000.000 на аккаунте — {price}₽
    """,
                    reply_markup=account_rub_keyboard(data["server"])
                )

                return

            if rubles > 14000:
                await safe_delete_message(message)

                await message.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=data["message_id"],
                    text=f"""
    ❌ Максимальная сумма: 14.000₽.

    🎮 Вы выбрали сервер {server["name"]} [{server["id"]}]

    💸 Цена за 1.000.000 на аккаунте — {price}₽
    """,
                    reply_markup=account_rub_keyboard(data["server"])
                )

                return

            virts = round((rubles / price) * 1000000)

        data["virts"] = virts
        data["rubles"] = rubles

        await safe_delete_message(message)

        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["message_id"],
            text=f"""
<b>📦 Заказ #{data["order_id"]}</b>

🌐 Сервер: {server["name"]} [{server["id"]}]
💎 Кол-во виртов: {virts}
💰 Сумма к оплате: {rubles}₽
⭐️ Аккаунт: 3-5 игровой LVL
📍 Рег. данные: дата и место регистрации

Все верно? ✅
    """,
            reply_markup=account_order_confirm_keyboard(),
            parse_mode="HTML"
        )

    elif step == "waiting_bank":

        bank = message.text.strip()

        if not bank.isdigit() or len(bank) != 6:
            await safe_delete_message(message)

            await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=data["message_id"],
                text="""
❌ Неверный номер банковского счёта.

<b>Банковский счёт должен состоять ровно из 6 цифр.</b>

<b>📝Введите номер вашего банковского счета.</b>

Если не знаете где его найти, обратитесь в <a href="https://t.me/ScoringPointsBot">Поддержку</a>

<b>⚠️Учтите, при передаче трейдом шанс бана будет меньше.</b>
""",
                reply_markup=method_keyboard(),
                parse_mode="HTML"
            )

            return

        bank = message.text

        data["method"] = "bank"
        data["bank"] = bank

        servers = get_servers_from_db()
        server_key = data["server"]
        server = servers[server_key]
        virts = data["virts"]
        rubles = data["rubles"]

        await safe_delete_message(message)

        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["message_id"],
            text=f"""
📦 Ваш заказ.

🌐 Сервер: {server["name"]}
💎 Кол-во виртов: {virts}
💰 Сумма к оплате: {rubles}₽

🏦 Ваш счет: {bank}

Все верно? ✅
""",
            reply_markup=order_confirm_keyboard()
        )

    elif step == "waiting_nick":

        nick = message.text.strip()

        if not re.fullmatch(r"[A-Za-zА-Яа-я]+_[A-Za-zА-Яа-я]+", nick):
            await safe_delete_message(message)

            await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=data["message_id"],
                text="""
        ❌ Никнейм указан неверно.

        🎮 Введите ваш игровой никнейм в формате:

        <code>Nick_Name</code>

        Пример:
        <code>Ivan_Ivanov</code>
        """,
                reply_markup=trade_method_keyboard(),
                parse_mode="HTML"
            )

            return

        data["method"] = "trade"
        data["nick"] = nick

        servers = get_servers_from_db()
        server_key = data["server"]
        server = servers[server_key]
        virts = data["virts"]
        rubles = data["rubles"]

        await safe_delete_message(message)

        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["message_id"],
            text=f"""
📦 Ваш заказ.

🌐 Сервер: {server["name"]}
💎 Кол-во виртов: {virts}
💰 Сумма к оплате: {rubles}₽

👤 Ваш никнейм: {nick}

Все верно? ✅
""",
            reply_markup=order_confirm_keyboard()
        )

    elif step == "waiting_review":

        review = message.text

        order_id = data["order_id"]
        rubles = data["rubles"]
        stars = data["rating"]

        await message.bot.send_message(
            REVIEW_CHAT_ID,
            f"""
Заказ: #{order_id}
Сумма: {rubles}₽
Оценка: {stars}
Отзыв: {review}
"""
        )

        await message.answer(
            f"""
📦 Заказ #{order_id}

Спасибо за отзыв! ⭐
""",
            reply_markup=after_review_keyboard()
        )

        del user_data[user_id]