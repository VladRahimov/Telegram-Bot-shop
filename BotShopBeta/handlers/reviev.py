from aiogram import Router
from aiogram.types import CallbackQuery

from config import ADMIN_CHAT_ID
from data.user_data import user_data
from utils.session import is_session_expired
from utils.messages import edit_text_or_caption

from database import update_order_status

from keyboards.reviev import rating_keyboard, review_input_keyboard


router = Router()


@router.callback_query(lambda c: c.data == "confirm_receive")
async def confirm_receive(call: CallbackQuery):
    user_id = call.from_user.id

    if user_id not in user_data:
        await call.answer(
            "Сессия устарела. Создайте заказ заново.",
            show_alert=True
        )
        return

    data = user_data[user_id]

    # защита от двойного нажатия
    if data.get("receive_confirmed"):
        await call.answer(
            "Получение уже подтверждено.",
            show_alert=True
        )
        return

    data["receive_confirmed"] = True

    order_id = data["order_id"]

    update_order_status(
        order_id=order_id,
        status="🟢 Выполнен"
    )

    # =========================
    # ЕСЛИ ЭТО ПОКУПКА АККАУНТА
    # =========================

    if data.get("type") == "account":
        admin_message_id = data.get("admin_message_id")

        if admin_message_id:
            await edit_text_or_caption(
                bot=call.bot,
                chat_id=ADMIN_CHAT_ID,
                message_id=data["admin_message_id"],
                text=f"""
        ✅ Заказ <code>#{order_id}</code> выполнен.

        Статус: <b>ЗАКАЗ ЗАВЕРШЁН</b>
        """,
                parse_mode="HTML"
            )


        done_text = "Выдача завершена! ✅"

    # =========================
    # ЕСЛИ ЭТО ОБЫЧНАЯ ПОКУПКА ВИРТОВ
    # =========================

    else:
        await call.bot.send_message(
            ADMIN_CHAT_ID,
            f"✅ Заказ #{order_id} выполнен."
        )

        done_text = "Перевод завершён! ✔️"

    await call.message.edit_text(
        f"""
Заказ: #{order_id}

{done_text}

Спасибо за покупку! 💖

⭐️ Пожалуйста, оцените нас:
""",
        reply_markup=rating_keyboard()
    )

    await call.answer()


@router.callback_query(lambda c: c.data.startswith("rate_"))
async def rate_order(call: CallbackQuery):
    user_id = call.from_user.id

    if user_id not in user_data:
        await call.answer("Сессия устарела. Начните заказ заново.", show_alert=True)
        return

    rating = call.data.replace("rate_", "")
    stars = "⭐" * int(rating)

    user_data[user_id]["rating"] = stars
    user_data[user_id]["step"] = "waiting_review"

    order_id = user_data[user_id]["order_id"]

    await call.answer(
        """🙏 Напишите в чат пару слов — что вам понравилось, а что не очень. Для нас это очень важно.
""",
        show_alert=True,
        parse_mode="HTML"
    )

    await call.message.edit_text(
    f"""
Заказ: #{order_id}

<b>😊 Благодарим за оценку!
✍️ Оставьте, пожалуйста, отзыв прямо в этот чат — нам важно знать, что вам понравилось. Читаем всё, без исключений!</b>
""",
    reply_markup=review_input_keyboard(),
    parse_mode="HTML"
)

    