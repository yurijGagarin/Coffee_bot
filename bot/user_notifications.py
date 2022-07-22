from typing import List

import telegram
from telegram import ReplyKeyboardMarkup
from telegram._bot import BT

from bot.db import get_admin_users, async_session
from bot.models import User
from bot.navigation import get_menu_definition, build_buttons


async def send_message_to_users(bot: BT, users: List[int], text: str):
    for user_id in users:
        print("msg", text)
        print("user_id", user_id)

        try:
            async with async_session() as session:
                user = await session.get(User, user_id)
            buttons = await build_buttons(await get_menu_definition(user))
            await bot.send_message(
                chat_id=user_id,
                text=text,
                reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            )
        except telegram.error.Forbidden:
            error_text = f"Користувач з id: {user_id} припинив роботу бота. Відправка повідомлення до нього неможлива."
            admin_users = await get_admin_users()
            for admin in admin_users:
                await bot.send_message(chat_id=admin.User.id, text=error_text)
