from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.types import BotCommandScopeDefault
from aiogram.types import BotCommandScopeChat

from config import ADMIN_IDS


async def set_bot_commands(bot: Bot):
    # Команды для обычных пользователей
    user_commands = [
        BotCommand(
            command="start",
            description="Главное меню"
        )
    ]

    await bot.set_my_commands(
        commands=user_commands,
        scope=BotCommandScopeDefault()
    )

    # Команды для админов
    admin_commands = [
        BotCommand(
            command="start",
            description="Главное меню"
        ),
        BotCommand(
            command="adm",
            description="Админ-панель"
        ),
        BotCommand(
            command="adm_add",
            description="Добавить админа"
        )
    ]

    for admin_id in ADMIN_IDS:
        await bot.set_my_commands(
            commands=admin_commands,
            scope=BotCommandScopeChat(
                chat_id=admin_id
            )
        )