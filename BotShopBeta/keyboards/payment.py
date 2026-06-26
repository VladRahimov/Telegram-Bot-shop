from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SUPPORT_BOT


def bank_method_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎁 Получить трейдом",
                    callback_data="method_trade"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад к вводу суммы",
                    callback_data="back_to_virts"
                )
            ]
        ]
    )


def trade_method_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏦 Получить через банк",
                    callback_data="method_bank"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад к вводу суммы",
                    callback_data="back_to_virts"
                )
            ]
        ]
    )


def method_keyboard():
    return bank_method_keyboard()


def order_confirm_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Да, перейти к оплате 🚀",
                    callback_data="go_payment"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Нет, вернуться назад ⬅️",
                    callback_data="back_to_virts"
                )
            ]
        ]
    )


def account_order_confirm_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Да, перейти к оплате 🚀",
                    callback_data="go_payment"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Нет, вернуться назад ⬅️",
                    callback_data="back_to_account_amount"
                )
            ]
        ]
    )

def payment_methods_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="1. СБП [Platega] 🇷🇺",
                    callback_data="pay_platega"
                )
            ],
            [
                InlineKeyboardButton(
                    text="2. Карта РФ 💳",
                    callback_data="pay_card_tbank"
                )
            ],
            [
                InlineKeyboardButton(
                    text="3. CryptoBot 🪙",
                    callback_data="pay_crypto"
                )
            ],
        ]
    )

def card_payment_keyboard(bank: str = "tbank"):
    buttons = []

    if bank == "tbank":
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Оплатить на Сбер🟢",
                    callback_data="pay_card_sber"
                )
            ]
        )
    else:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Оплатить в Т-Банк⚫️",
                    callback_data="pay_card_tbank"
                )
            ]
        )


    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Вернуться назад",
                callback_data="back_to_payment_methods"
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def payment_confirm_keyboard(payment_url: str | None = None):
    buttons = []

    if payment_url:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="💸 Перейти к оплате",
                    url=payment_url
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="Я оплатил ✅",
                callback_data="confirm_payment"
            )
        ]
    )
    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Вернуться назад",
                callback_data="back_to_payment_methods"
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def bank_after_payment_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить получение",
                    callback_data="confirm_receive"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🛠️ Поддержка",
                    url=SUPPORT_BOT
                )
            ]
        ]
    )


def trade_arrived_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Я приехал 🚗",
                    callback_data="arrived_trade"
                )
            ]
        ]
    )


def trade_receive_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить получение",
                    callback_data="confirm_receive"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🛠️ Поддержка",
                    url=SUPPORT_BOT
                )
            ]
        ]
    )

def admin_payment_check_keyboard(user_id: int, order_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Клиент оплатил",
                    callback_data=f"admin_pay_ok_{user_id}_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Оплата не пришла",
                    callback_data=f"admin_pay_fail_{user_id}_{order_id}"
                )
            ]
        ]
    )


def support_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛠️ Поддержка",
                    url=SUPPORT_BOT
                )
            ]
        ]
    )

def account_admin_fail_keyboard(user_id: int, order_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Оплата не пришла",
                    callback_data=f"admin_pay_fail_{user_id}_{order_id}"
                )
            ]
        ]
    )


def account_receive_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить получение",
                    callback_data="confirm_receive"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🛠️ Поддержка",
                    url=SUPPORT_BOT
                )
            ]
        ]
    )