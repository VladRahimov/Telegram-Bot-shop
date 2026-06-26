from aiogram import Router
from aiogram.types import CallbackQuery

from database import get_user_orders
from keyboards.orders import orders_keyboard
from utils.messages import safe_delete_message


router = Router()


@router.callback_query(lambda c: c.data == "orders")
async def my_orders(call: CallbackQuery):
    user_id = call.from_user.id

    orders = get_user_orders(user_id)

    await safe_delete_message(call.message)

    if not orders:
        await call.message.answer(
            """
🧾 Ваша история покупок

У вас пока нет покупок.
""",
            reply_markup=orders_keyboard()
        )

        await call.answer()
        return

    text = "🧾Ваша история покупок: (новейшие покупки отображаются сверху)\n\n"

    for order in orders:
        order_id, status, server, server_id, virts, rubles, created_at = order

        if created_at is None:
            created_at = "Не указано"

        text += f"""
🆔 Заказ: #{order_id}
📅 Дата: {created_at}
Статус: {status}
Сервер: {server} [{server_id}]
Вирты: {virts}
Сумма: {rubles}₽

━━━━━━━━━━━━━━
"""

    await call.message.answer(
        text,
        reply_markup=orders_keyboard()
    )

    await call.answer()