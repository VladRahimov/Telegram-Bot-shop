from aiogram.exceptions import TelegramBadRequest


async def safe_delete_message(message):
    try:
        await message.delete()
    except TelegramBadRequest as e:
        print(f"Не удалось удалить сообщение: {e}")
    except AttributeError as e:
        print(f"Сообщение недоступно для удаления: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка при удалении сообщения: {e}")

from aiogram.exceptions import TelegramBadRequest


async def edit_text_or_caption(
    bot,
    chat_id: int,
    message_id: int,
    text: str,
    reply_markup=None,
    parse_mode: str = "HTML"
):
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
    except TelegramBadRequest as e:
        if "there is no text in the message to edit" in str(e):
            await bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message_id,
                caption=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
        else:
            raise