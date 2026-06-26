from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def orders_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад в меню",
                    callback_data="back_main_menu"
                )
            ]
        ]
    )