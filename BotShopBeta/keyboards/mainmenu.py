from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from config import SUPPORT_BOT
from config import REVIEWS_CHANNEL


def main_menu_keyboard():

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="Купить вирты",
                    callback_data="buy_virt"
                )
            ],

            [
                InlineKeyboardButton(
                    text="Купить аккаунт с виртами",
                    callback_data="buy_account"
                )
            ],

            [
                InlineKeyboardButton(
                    text="Наличие виртов",
                    callback_data="balance"
                ),

                InlineKeyboardButton(
                    text="Мои покупки",
                    callback_data="orders"
                )
            ],

            [
                InlineKeyboardButton(
                    text="Информация",
                    callback_data="information"
                )
            ],

            [
                InlineKeyboardButton(
                    text="Поддержка",
                    url=SUPPORT_BOT
                ),

                InlineKeyboardButton(
                    text="Отзывы",
                    url=REVIEWS_CHANNEL
                )
            ]
        ]
    )

    return keyboard