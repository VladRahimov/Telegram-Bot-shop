from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import random
import asyncio


TOKEN = "8726680377:AAGzATeya8iBHq30Lr_9WmUcHgNG58-hFoM"

bot = Bot(token=TOKEN)
dp = Dispatcher()
ADMIN_CHAT_ID = -5059908754
servers = {
    "RED": {"id": 1, "name": "RED [1]", "price": 100},
    "GREEN": {"id": 2, "name": "GREEN [2]", "price": 100},
    "BLUE": {"id": 3, "name": "BLUE [3]", "price": 100},
    "YELLOW": {"id": 4, "name": "YELLOW [4]", "price": 100},
    "ORANGE": {"id": 5, "name": "ORANGE [5]", "price": 100},
    "PURPLE": {"id": 6, "name": "PURPLE [6]", "price": 100},
    "LIME": {"id": 7, "name": "LIME [7]", "price": 100},
    "PINK": {"id": 8, "name": "PINK [8]", "price": 100},
    "CHERRY": {"id": 9, "name": "CHERRY [9]", "price": 100},
    "Black": {"id": 10, "name": "BLACK [10]", "price": 100},
    "Indigo": {"id": 11, "name": "INDIGO [11]", "price": 100},
    "White": {"id": 12, "name": "WHITE [12]", "price": 100},
    "Magenta": {"id": 13, "name": "MAGENTA [13]", "price": 100},
    "Crimson": {"id": 14, "name": "CRIMSON [14]", "price": 100},
    "Gold": {"id": 15, "name": "GOLD [15]", "price": 100},
    "Azure": {"id": 16, "name": "AZURE [16]", "price": 100},
    "Platinum": {"id": 17, "name": "PLATINUM [17]", "price": 100},
    "Aqua": {"id": 18, "name": "Aqua", "price": 100},
    "Gray": {"id": 19, "name": "Gray", "price": 100},
    "Ice": {"id": 20, "name": "Ice", "price": 100},
    "Chilli": {"id": 21, "name": "Chilli", "price": 100},
    "Choco": {"id": 22, "name": "Choco", "price": 100},
    "Moscow": {"id": 23, "name": "Moscow", "price": 100},
    "Spb": {"id": 24, "name": "SPB", "price": 100},
    "Ufa": {"id": 25, "name": "UFA", "price": 100},
    "Sochi": {"id": 26, "name": "Sochi", "price": 100},
    "Kazan": {"id": 27, "name": "Kazan", "price": 100},
    "Samara": {"id": 28, "name": "Samara", "price": 100},
    "Rostov": {"id": 29, "name": "Rostov", "price": 100},
    "Anapa": {"id": 30, "name": "Anapa", "price": 100},
    "Ekb": {"id": 31, "name": "EKB", "price": 100},
    "Krasnodar": {"id": 32, "name": "Krasnodar", "price": 100},
    "Arzamas": {"id": 33, "name": "Arzamas", "price": 100},
    "Novosib": {"id": 34, "name": "Novosib", "price": 100},
    "Grozny": {"id": 35, "name": "Grozny", "price": 100},
    "Saratov": {"id": 36, "name": "Saratov", "price": 100},
    "Omsk": {"id": 37, "name": "Omsk", "price": 100},
    "Irkutsk": {"id": 38, "name": "Irkutsk", "price": 100},
    "Volgograd": {"id": 39, "name": "Volgograd", "price": 100},
    "Voronezh": {"id": 40, "name": "Voronezh", "price": 100},
    "Belgorod": {"id": 41, "name": "Belgorod", "price": 100},
    "Makhachkala": {"id": 42, "name": "Makhachkala", "price": 100},
    "Vladikavkaz": {"id": 43, "name": "Vladikavkaz", "price": 100},
    "Vladivostok": {"id": 44, "name": "Vladivostok", "price": 100},
    "Kaliningrad": {"id": 45, "name": "Kaliningrad", "price": 100},
    "Chelyabinsk": {"id": 46, "name": "Chelyabinsk", "price": 100},
    "Krasnoyarsk": {"id": 47, "name": "Krasnoyarsk", "price": 100},
    "Cheboksary": {"id": 48, "name": "Cheboksary", "price": 100},
    "Khabarovsk": {"id": 49, "name": "Khabarovsk", "price": 100},
    "Perm": {"id": 50, "name": "Perm", "price": 100},
    "Tula": {"id": 51, "name": "Tula", "price": 100},
    "Ryazan": {"id": 52, "name": "Ryazan", "price": 100},
    "Murmansk": {"id": 53, "name": "Murmansk", "price": 100},
    "Penza": {"id": 54, "name": "Penza", "price": 100},
    "Kursk": {"id": 55, "name": "Kursk", "price": 100},
    "Arkhangelsk": {"id": 56, "name": "Arkhangelsk", "price": 100},
    "Orenburg": {"id": 57, "name": "Orenburg", "price": 100},
    "Kirov": {"id": 58, "name": "Kirov", "price": 100},
    "Kemerovo": {"id": 59, "name": "Kemerovo", "price": 100},
    "Tyumen": {"id": 60, "name": "Tyumen", "price": 100},
    "Tolyatti": {"id": 61, "name": "Tolyatti", "price": 100},
    "Ivanovo": {"id": 62, "name": "Ivanovo", "price": 100},
    "Stavropol": {"id": 63, "name": "Stavropol", "price": 100},
    "Smolensk": {"id": 64, "name": "Smolensk", "price": 100},
    "Pskov": {"id": 65, "name": "Pskov", "price": 100},
    "Bryansk": {"id": 66, "name": "Bryansk", "price": 100},
    "Orel": {"id": 67, "name": "Orel", "price": 100},
    "Yaroslavl": {"id": 68, "name": "Yaroslavl", "price": 100},
    "Barnaul": {"id": 69, "name": "Barnaul", "price": 100},
    "Lipetsk": {"id": 70, "name": "Lipetsk", "price": 100},
    "Ulyanovsk": {"id": 71, "name": "Ulyanovsk", "price": 100},
    "Yakutsk": {"id": 72, "name": "Yakutsk", "price": 100},
    "Tambov": {"id": 73, "name": "Tambov", "price": 100},
    "Bratsk": {"id": 74, "name": "Bratsk", "price": 100},
    "Astrakhan": {"id": 75, "name": "Astrakhan", "price": 100},
    "Chita": {"id": 76, "name": "Chita", "price": 100},
    "Kostroma": {"id": 77, "name": "Kostroma", "price": 100},
    "Vladimir": {"id": 78, "name": "Vladimir", "price": 100},
    "Kaluga": {"id": 79, "name": "Kaluga", "price": 100},
    "N.novgorod": {"id": 80, "name": "N.Novgorod", "price": 100},
    "Taganrog": {"id": 81, "name": "Taganrog", "price": 100},
    "Vologda": {"id": 82, "name": "Vologda", "price": 100},
    "Tver": {"id": 83, "name": "Tver", "price": 100},
    "Tomsk": {"id": 84, "name": "Tomsk", "price": 100},
    "Izhevsk": {"id": 85, "name": "Izhevsk", "price": 100},
    "Surgut": {"id": 86, "name": "Surgut", "price": 100},
    "Podolsk": {"id": 87, "name": "Podolsk", "price": 100},
    "Magadan": {"id": 88, "name": "Magadan", "price": 100},
    "Cherepovets": {"id": 89, "name": "Cherepovets", "price": 100},
    "Norilsk": {"id": 90, "name": "Norilsk", "price": 100},
    "Astana": {"id": 91, "name": "Astana", "price": 100}
}

user_data = {}

#@dp.message()
#async def get_channel_id(message: Message):

#    print(message.chat.id)


@dp.message(Command("start"))   #старт
async def start(message: Message):
    print("DEBUG: старт")
    
    photo = FSInputFile("mainmenu.jpg")

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
                    text="Поддержка",
                    url="https://t.me/ScoringPointsBot"
                ),
                InlineKeyboardButton(
                    text="Отзывы",
                    url="https://t.me/OtzivyShadowBR"
                )
            ]
        ]
    )

    await message.answer_photo(
        photo=photo,
        caption="""
Привет! 👋

У нас ты можешь купить игровую валюту в Black Russia по лучшему курсу 💰.

Автоматическая выдача на всех серверах 🚀, средства поступают в течение 5 минут ⏱️.

При задержках обращайся в поддержку 24/7 🛠️.

Удачных заказов! 🍀
        """,
        
        reply_markup=keyboard
        
    )

@dp.callback_query(lambda c: c.data == "buy_virt")
async def buy_virt(call: CallbackQuery):

    buttons = []
    row = []

    for key, server in servers.items():

        row.append(
            InlineKeyboardButton(
                text=server["name"],
                callback_data=f"s_{key}"
            )
        )

        if len(row) == 3:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append(
        [
            InlineKeyboardButton(
                text="Назад в главное меню",
                callback_data="back_main_menu"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await call.message.delete()

    await call.message.answer(
        text="🌐 Выберете сервер, на котором хотите купить игровую валюту.",
        reply_markup=keyboard
    )

    await call.answer()

@dp.callback_query(lambda c: c.data.startswith("s_"))
async def server_picked(call: CallbackQuery):

    server_key = call.data.replace("s_", "")

    server = servers[server_key]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Перевести в рубли",
                    callback_data=f"transferRub_{server_key}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Вернуться к списку серверов",
                    callback_data="returnToServ"
                )
            ]
        ]
    )

    

    await call.message.delete()

    msg = await call.message.answer(
    f"""
🎮Вы выбрали сервер {server["name"]}

💸Цена за 1.000.000 — {server["price"]}₽

Напишите, сколько виртов вы ходите купить.

500.000 — напишите «0.5» или «500000»
1.000.000 — напишите «1» или «1000000»

⚠️Минимальная сумма для покупки — 500.000
    """,
    reply_markup=keyboard
    )
    
    user_data[call.from_user.id] = {
        "server": server_key,
        "step": "waiting_virts",
        "message_id": msg.message_id,
        "input_mode": "virts"
    }

    await call.answer()


@dp.callback_query(lambda c: c.data == "returnToServ") #вернуться от кол-во виртов к серверам
async def Back_to_servers(call: CallbackQuery):
    buttons = []
    row = []

    for key, server in servers.items():

        row.append(
            InlineKeyboardButton(
                text=server["name"],
                callback_data=f"s_{key}"
            )
        )

        if len(row) == 3:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append(
        [
            InlineKeyboardButton(
                text="Назад в главное меню",
                callback_data="back_main_menu"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await call.message.delete()

    await call.message.answer(
        text="🎮 Выбери сервер:",
        reply_markup=keyboard
    )

    await call.answer()

@dp.callback_query(lambda c: c.data == "back_main_menu") #вернуться от списка серверов в главное
async def back_main(call: CallbackQuery):
    photo = FSInputFile("mainmenu.jpg")

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
                    text="Поддержка",
                    url="https://t.me/ScoringPointsBot"
                ),
                InlineKeyboardButton(
                    text="Отзывы",
                    url="https://t.me/+2FO3ZwxO3hozNzA6"
                )
            ]
        ]
    )

    await call.message.delete()

    await call.message.answer_photo(
        photo=photo,
        caption="""
Привет! 👋

У нас ты можешь купить игровую валюту в Black Russia по лучшему курсу 💰.

Автоматическая выдача на всех серверах 🚀, средства поступают в течение 5 минут ⏱️.

При задержках обращайся в поддержку 24/7 🛠️.

Удачных заказов! 🍀
        """,
        
        reply_markup=keyboard
        
    )

@dp.callback_query(lambda c: c.data.startswith("transferRub_"))
async def transferRub(call: CallbackQuery):

    server_key = call.data.replace("transferRub_", "")

    server = servers[server_key]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Перевести в вирты",
                    callback_data=f"transferVirt_{server_key}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Вернуться к списку серверов",
                    callback_data="returnToServ"
                )
            ]
        ]
    )

    await call.message.delete()

    await call.message.answer(
        f"""
🎮Вы выбрали сервер {server["name"]}

Цена за 1.000.000 — 70₽
Укажите сумму в реальных рублях, на которую ходите купить вирты.

⚠️Минимальная сумма для покупки — 35₽
""",
        reply_markup=keyboard
    )

    await call.answer()

@dp.callback_query(lambda c: c.data.startswith("transferVirt_"))
async def transferRub(call: CallbackQuery):

    server_key = call.data.replace("transferVirt_", "")
    
    server = servers[server_key]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Перевести в рубли",
                    callback_data=f"transferRub_{server_key}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Вернуться к списку серверов",
                    callback_data="returnToServ"
                )
            ]
        ]
    )

    await call.message.delete()

    await call.message.answer(
        f"""
🎮Вы выбрали сервер {server["name"]} 

💸Цена за 1.000.000 — {server["price"]}₽
Напишите, сколько виртов вы ходите купить.

500.000 — напишите «0.5» или «500000»
1.000.000 — напишите «1» или «1000000»

⚠️Минимальная сумма для покупки — 500.000

""",
        reply_markup=keyboard
    )

    await call.answer()

@dp.message()
async def handle_text(message: Message):

    user_id = message.from_user.id

    if user_id not in user_data:
        return

    step = user_data[user_id]["step"]

    # =========================
    # Ввод количества виртов
    # =========================

    if step == "waiting_virts":

        if not message.text.isdigit():

            await message.answer(
                "❌ Введите число."
            )

            return

        value = int(message.text)

        mode = user_data[user_id]["input_mode"]

        server = servers[user_data[user_id]["server"]]

    # =========================
    # Ввод в виртах
    # =========================

        if mode == "virts":

            if value < 500000:

                await message.answer(
                    "❌ Минимальная сумма: 500000 виртов"
                )

                return

            virts = value

            rubles = round((virts / 1000000) * server["price"])

    # =========================
    # Ввод в рублях
    # =========================

        else:

            if value < 35:

                await message.answer(
                    "❌ Минимальная сумма: 35₽"
                )

                return

            rubles = value

            virts = round((rubles / server["price"]) * 1000000)

        user_data[user_id]["virts"] = virts
        user_data[user_id]["rubles"] = rubles

        user_data[user_id]["step"] = "waiting_bank"

        keyboard = InlineKeyboardMarkup(
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

        msg_id = user_data[user_id]["message_id"]

        await message.delete()

        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg_id,
            text="""
📝Введите номер вашего банковского счета.

Если не знаете где его найти, обратитесь в Поддержку:
https://t.me/ScoringPointsBot 💬

⚠️Учтите, при передаче трейдом шанс бана будет меньше.
            """,
            reply_markup=keyboard
        )

    elif step == "waiting_bank":

        bank = message.text

        user_data[user_id]["method"] = "bank"

        user_data[user_id]["bank"] = bank

        server = servers[user_data[user_id]["server"]]

        virts = user_data[user_id]["virts"]

        rubles = round((virts / 1000000) * server["price"])

        keyboard = InlineKeyboardMarkup(
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

        msg_id = user_data[user_id]["message_id"]

        await message.delete()

        user_data[user_id]["step"] = "waiting_bank"
        user_data[user_id]["method"] = "bank"


        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg_id,
            text=f"""
📦 Ваш заказ.

🌐 Сервер: {server["name"]} [{server["id"]}]
💎 Кол-во виртов: {virts}
💰 Сумма к оплате: {rubles}₽

🏦 Ваш счет: {bank}

Все верно? ✅
""",
            reply_markup=keyboard
        )

    elif step == "waiting_nick":

        nick = message.text

        user_data[user_id]["method"] = "trade"

        user_data[user_id]["nick"] = nick

        server = servers[user_data[user_id]["server"]]

        virts = user_data[user_id]["virts"]

        rubles = round((virts / 1000000) * server["price"])

        keyboard = InlineKeyboardMarkup(
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

        msg_id = user_data[user_id]["message_id"]

        await message.delete()

        user_data[user_id]["step"] = "waiting_bank"
        user_data[user_id]["method"] = "bank"

        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg_id,
            text=f"""
📦 Ваш заказ.

🌐 Сервер: {server["name"]} [{server["id"]}]
💎 Кол-во виртов: {virts}
💰 Сумма к оплате: {rubles}₽

👤 Ваш никнейм: {nick}

Все верно? ✅
""",
            reply_markup=keyboard
        )

    elif step == "waiting_review":

        review = message.text

        data = user_data[user_id]

        order_id = data["order_id"]

        server = servers[data["server"]]

        virts = data["virts"]

        rubles = round((virts / 1000000) * server["price"])

        stars = data["rating"]

        REVIEW_CHAT_ID = -1003722615392

        await bot.send_message(
            REVIEW_CHAT_ID,
            f"""
📦 Заказ: #{order_id}

💰 Сумма: {rubles}₽

⭐ Оценка:
{stars}

✍️ Отзыв:
{review}
"""
        )

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🏠 Главное меню",
                        callback_data="back_main_menu"
                    )
                ]
            ]
        )

        await message.answer(
            f"""
📦 Заказ #{order_id}

Спасибо за отзыв! ⭐
    """,
            reply_markup=keyboard
        )

        del user_data[user_id]

@dp.callback_query(lambda c: c.data == "back_to_virts")
async def back_to_virts(call: CallbackQuery):

    user_id = call.from_user.id

    user_data[user_id]["step"] = "waiting_virts"

    server = servers[user_data[user_id]["server"]]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💸 Перевести в рубли",
                    callback_data="transferRub"
                )
            ]
        ]
    )

    msg_id = user_data[user_id]["message_id"]

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=msg_id,
        text=f"""
🌐 Сервер: {server["name"]} [{server["id"]}]

💰 Цена за 1кк: {server["price"]}₽

Введите количество виртов:

Минимум: 500000
""",
        reply_markup=keyboard
    )

    await call.answer()


@dp.callback_query(lambda c: c.data == "method_trade")
async def method_trade(call: CallbackQuery):

    user_id = call.from_user.id

    user_data[user_id]["step"] = "waiting_nick"
    user_data[user_id]["method"] = "trade"

    keyboard = InlineKeyboardMarkup(
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

    msg_id = user_data[user_id]["message_id"]

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=msg_id,
        text="""
🎮 Введите ваш игровой никнейм, в формате — Nick_Name

🚀Если хотите получить вирты быстрее, выберите получение через банк.🏦
""",
        reply_markup=keyboard
    )

    await call.answer()

@dp.callback_query(lambda c: c.data == "confirm_payment")
async def confirm_payment(call: CallbackQuery):

    user_id = call.from_user.id

    data = user_data[user_id]

    server = servers[data["server"]]

    virts = data["virts"]

    rubles = round((virts / 1000000) * server["price"])

    order_id = random.randint(100000, 999999)

    data["order_id"] = order_id

    # =========================
    # Текст админу
    # =========================

    admin_text = f"""
🛒 Новый заказ!

🆔 Заказ: #{order_id}

👤 @{call.from_user.username}

🌐 Сервер: {server["name"]} [{server["id"]}]
💎 Вирты: {virts}
💰 Сумма: {rubles}₽
"""

    if "bank" in data:

        admin_text += f"""

🏦 Счёт:
{data["bank"]}
"""

    if "nick" in data:

        admin_text += f"""

👤 Ник:
{data["nick"]}
"""

    await bot.send_message(
        ADMIN_CHAT_ID,
        admin_text
    )

    # =========================
    # BANK
    # =========================

    if data["method"] == "bank":

        keyboard = InlineKeyboardMarkup(
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
                        url="https://t.me/ScoringPointsBot"
                    )
                ]
            ]
        )

        text = """
⏱️Когда вам придут вирты не забудьте нажать на кнопку «Подтвердить получение»

Если в течении 5 минут вирты не поступят на баланс, обратитесь в поддержку.🛠️
"""

    # =========================
    # TRADE
    # =========================

    else:

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🚗 Я приехал",
                        callback_data="arrived_trade"
                    )
                ]
            ]
        )

        text = f"""
Ждем вас, {data["nick"]}, на спавне города Арзамас.

Не забудьте нажать на кнопку «Я приехал 🚗», когда будете на месте.
"""

    msg_id = data["message_id"]

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=msg_id,
        text=text,
        reply_markup=keyboard
    )

    await call.answer()

@dp.callback_query(lambda c: c.data == "arrived_trade")
async def arrived_trade(call: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
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
                    url="https://t.me/ScoringPointsBot"
                )
            ]
        ]
    )

    await call.message.edit_text(
        """
Ожидайте, в течении 5-10 минут к вам подойдут и отправят трейд. ⏳

Не уезжайте и не выходите с игры.🖥️

⚠️ После получения валюты не забудьте нажать кнопку «Подтвердить получение»
""",
        reply_markup=keyboard
    )

    await call.answer()


@dp.callback_query(lambda c: c.data == "confirm_receive")
async def confirm_receive(call: CallbackQuery):

    user_id = call.from_user.id

    data = user_data[user_id]

    order_id = data["order_id"]

    await bot.send_message(
        ADMIN_CHAT_ID,
        f"✅ Заказ #{order_id} выполнен."
    )

    keyboard = InlineKeyboardMarkup(
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

    await call.message.edit_text(
        f"""
Заказ: #{order_id}

Перевод завершён! ✔️

Спасибо за покупку! 💖

⭐️ Пожалуйста, оцените нас:
""",
        reply_markup=keyboard
    )

    await call.answer()

@dp.callback_query(lambda c: c.data.startswith("success_"))
async def success_order(call: CallbackQuery):

    user_id = int(call.data.replace("success_", ""))

    await call.message.edit_reply_markup(
        reply_markup=None
    )

    text = call.message.text

    await call.message.edit_text(
        text + "\n\n✅ ЗАКАЗ ВЫПОЛНЕН"
    )

    lines = text.split("\n")

    await bot.send_message(
        user_id,
        f"""
✅ Ваш заказ выполнен!

{chr(10).join(lines[2:])}

Проверьте поступление виртов.
"""
    )

    await call.answer(
        "Пользователь уведомлен"
    )


@dp.callback_query(lambda c: c.data.startswith("failed_"))
async def failed_order(call: CallbackQuery):

    user_id = int(call.data.replace("failed_", ""))

    await call.message.edit_reply_markup(
        reply_markup=None
    )

    text = call.message.text

    await call.message.edit_text(
        text + "\n\n❌ ОПЛАТА НЕ НАЙДЕНА"
    )

    lines = text.split("\n")

    await bot.send_message(
        user_id,
        f"""
❌ Оплата по заказу не найдена!

{chr(10).join(lines[2:])}

Если вы уверены что оплатили заказ —
обратитесь в поддержку.
"""
    )

    await call.answer(
        "Пользователь уведомлен"
    )

@dp.callback_query(lambda c: c.data == "go_payment")
async def go_payment(call: CallbackQuery):

    user_id = call.from_user.id

    server = servers[user_data[user_id]["server"]]

    virts = user_data[user_id]["virts"]

    rubles = round((virts / 1000000) * server["price"])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Я оплатил ✅",
                    callback_data="confirm_payment"
                )
            ]
        ]
    )

    msg_id = user_data[user_id]["message_id"]

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=msg_id,
        text=f"""
Оплатите сумму {rubles}₽ по следующим реквизитам 💸

СБП (На Т-Банк)🏦:
+7 (910) 153 36-99
(Ярослав Ш. 👤)

Или по номеру карты💳 на Сбер🏦:
2202 2085 8610 1777

После перевода обязательно нажмите кнопку
«Я оплатил ✅»
""",
        reply_markup=keyboard
    )

    await call.answer()

@dp.callback_query(lambda c: c.data.startswith("rate_"))
async def rate_order(call: CallbackQuery):

    user_id = call.from_user.id

    rating = call.data.replace("rate_", "")

    stars = "⭐" * int(rating)

    user_data[user_id]["rating"] = stars
    user_data[user_id]["step"] = "waiting_review"

    order_id = user_data[user_id]["order_id"]

    await call.answer(
        "🙏 Напишите пару слов о заказе",
        show_alert=True
    )

    await call.message.edit_text(
        f"""
Заказ: #{order_id}

😊 Благодарим за оценку!

✍️ Оставьте, пожалуйста, отзыв прямо в этот чат — нам важно знать, что вам понравилось.
"""
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())