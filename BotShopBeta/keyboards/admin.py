import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_servers_from_db


SERVERS_PER_PAGE = 22


def admin_servers_keyboard(page: int = 1):
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

    for key, server in page_servers:
        row.append(
            InlineKeyboardButton(
                text=f'{server["name"]} [{server["id"]}]',
                callback_data=f"admin_stock_s_{key}"
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
                callback_data=f"admin_stock_page_{page - 1}"
            ),
            InlineKeyboardButton(
                text=f"Стр. {page} из {total_pages}",
                callback_data="page_info"
            ),
            InlineKeyboardButton(
                text=">",
                callback_data=f"admin_stock_page_{page + 1}"
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )