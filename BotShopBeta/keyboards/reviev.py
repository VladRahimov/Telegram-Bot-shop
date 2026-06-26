from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def rating_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⭐⭐⭐⭐⭐",
                    callback_data="rate_5"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⭐⭐⭐⭐",
                    callback_data="rate_4"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⭐⭐⭐",
                    callback_data="rate_3"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⭐⭐",
                    callback_data="rate_2"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⭐",
                    callback_data="rate_1"
                )
            ]
        ]
    )


def review_input_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏠 Главное меню",
                    callback_data="back_main_menu"
                )
            ]
        ]
    )


def after_review_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏠 Главное меню",
                    callback_data="back_main_menu"
                )
            ]
        ]
    )
