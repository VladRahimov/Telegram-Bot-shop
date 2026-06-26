import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_servers_from_db


SERVERS_PER_PAGE = 22


def servers_keyboard(page: int = 1, mode: str = "virts"):
    servers = get_servers_from_db()
    server_items = list(servers.items())
    total_pages = math.ceil(len(server_items) / SERVERS_PER_PAGE)

    if page < 1:
        page = total_pages

    if page > total_pages:
        page = 1

    start_index = (page - 1) * SERVERS_PER_PAGE
    end_index = start_index + SERVERS_PER_PAGE

    page_servers = server_items[start_index:end_index]

    buttons = []
    row = []

    if mode == "virts":
        callback_prefix = "s"
        page_prefix = "servers_page"

    elif mode == "account":
        callback_prefix = "acc_s"
        page_prefix = "acc_servers_page"

    elif mode == "stock":
        callback_prefix = "stock_s"
        page_prefix = "stock_servers_page"

    for key, server in page_servers:
        row.append(
            InlineKeyboardButton(
                text=f'{server["name"]} [{server["id"]}]',
                callback_data=f"{callback_prefix}_{key}"
            )
        )

        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append(
        [
            InlineKeyboardButton(
                text="<",
                callback_data=f"{page_prefix}_{page - 1}"
            ),
            InlineKeyboardButton(
                text=f"Стр. {page} из {total_pages}",
                callback_data="page_info"
            ),
            InlineKeyboardButton(
                text=">",
                callback_data=f"{page_prefix}_{page + 1}"
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад в меню",
                callback_data="back_main_menu"
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def virts_keyboard(server_key):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💸 Перевести в рубли",
                    callback_data=f"transferRub_{server_key}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ К списку серверов",
                    callback_data="returnToServ"
                )
            ]
        ]
    )


def rub_keyboard(server_key):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💎 Перевести в вирты",
                    callback_data=f"transferVirt_{server_key}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ К списку серверов",
                    callback_data="returnToServ"
                )
            ]
        ]
    )


def account_amount_keyboard(server_key):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💸 Ввести в реальных рублях",
                    callback_data=f"acc_transferRub_{server_key}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад к списку серверов",
                    callback_data="account_returnToServ"
                )
            ]
        ]
    )


def account_rub_keyboard(server_key):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💎 Ввести в виртах",
                    callback_data=f"acc_transferVirt_{server_key}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад к списку серверов",
                    callback_data="account_returnToServ"
                )
            ]
        ]
    )