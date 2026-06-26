from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import FSInputFile
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.mainmenu import main_menu_keyboard

from database import add_or_update_user

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    add_or_update_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        chat_id=message.chat.id
    )
    photo = FSInputFile("assets/mainmenu.jpg")

    await message.answer_photo(

        photo=photo,

        caption="""
<b>Привет! 👋</b>

У нас ты можешь купить игровую валюту в <b>Black Russia</b> по лучшему курсу 💰

<b>Автоматическая выдача</b> на всех серверах 🚀
Вирты поступают в течении <b>5 минут ⏱️</b>

<b>Удачных заказов! 🍀</b>
""",

        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(lambda c: c.data == "back_main_menu")
async def back_main_menu(call: CallbackQuery):
    photo = FSInputFile("assets/mainmenu.jpg")

    await call.message.delete()

    await call.message.answer_photo(
        photo=photo,
        caption="""
<b>Привет! 👋</b>

У нас ты можешь купить игровую валюту в <b>Black Russia</b> по лучшему курсу 💰

<b>Автоматическая выдача</b> на всех серверах 🚀
Вирты поступают в течении <b>5 минут ⏱️</b>

<b>Удачных заказов! 🍀</b>
""",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )

    await call.answer()

@router.callback_query(lambda c: c.data == "information")
async def info(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📄 Политика конфиденциальности",
                    url="https://telegra.ph/Politika-konfidencialnosti-04-01-26"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📑 Пользовательское соглашение",
                    url="https://telegra.ph/Polzovatelskoe-soglashenie-04-01-19"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад в меню",
                    callback_data="back_main_menu"
                )
            ]
        ]
    )

    await call.message.delete()

    await call.message.answer(
        """
ℹ️ Информация

Ознакомьтесь с документами:
""",
        reply_markup=keyboard
    )

    await call.answer()