import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from telegram import *
from telegram.ext import *

import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

engine = create_async_engine(config.DB_DSN)


# async def gstart(update: Update, context: CallbackContext.DEFAULT_TYPE):
# await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def echo(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Вибачте, я вас не зрозумів :(")


async def unknown(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


async def start(update: Update, context: CallbackContext):
    context.user_data['is_menu'] = None
    buttons = [
        [KeyboardButton("Меню Закладу")],
        [KeyboardButton("Шо мені випити?")],
        [KeyboardButton("ЗАБРОНЮВАТИ САМОСИ!")],
    ]
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Вітаємо в Діджиталізованому Мускаті",
                                   reply_markup=ReplyKeyboardMarkup(buttons))


async def menu(update: Update, context: CallbackContext.DEFAULT_TYPE):
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    context.user_data['is_menu'] = True
    result = []
    async with async_session() as session:
        r = await session.execute('SELECT * FROM menu_item')
        results_as_dict = r.mappings().all()
        for r in results_as_dict:
            result.append(r['name'] + ': ' + str(r['price']) + ' uah')

    buttons = [
        [KeyboardButton("Кава"), KeyboardButton("Не тільки лиш кава")],
        [KeyboardButton("Десерти")],
        [KeyboardButton("Головне меню")],
    ]
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Виберіть розділ:",
                                   reply_markup=ReplyKeyboardMarkup(buttons))
    # await context.bot.send_message(chat_id=update.effective_chat.id,
    #                                text="\n".join(result),
    #                                reply_markup=ReplyKeyboardMarkup(buttons))


async def query_menu_items(sql_query):
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    result = []
    async with async_session() as session:
        r = await session.execute(sql_query)
        results_as_dict = r.mappings().all()
        for el in results_as_dict:
            card = f'Назва: {(el["name"])}\nЦіна: {(el["price"])}\n'
            result.append(card)

    return result


async def coffee(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if context.user_data['is_menu']:
        buttons = [
            [KeyboardButton("Назад до меню"), KeyboardButton("Головне меню")],
        ]

        result = await query_menu_items('SELECT * FROM menu_item where is_coffee = TRUE')

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="ось тобі меню:\n" + "\n".join(result),
                                       reply_markup=ReplyKeyboardMarkup(buttons))
    else:
        context.user_data['is_coffee'] = True
        buttons = [
            [KeyboardButton("З молоком"), KeyboardButton("Без молока")],
        ]

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=" ",
                                       reply_markup=ReplyKeyboardMarkup(buttons))


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TOKEN).build()

    start_handler = CommandHandler('start', start)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    menu_handler = MessageHandler(filters.Regex('Меню Закладу'), menu)
    main_menu_handler = MessageHandler(filters.Regex("Головне меню"), start)
    coffee_handler = MessageHandler(filters.Regex('Кава'), coffee)
    back_handler = MessageHandler(filters.Regex('Назад до меню'), menu)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(unknown_handler)
    application.add_handler(menu_handler)
    application.add_handler(main_menu_handler)
    application.add_handler(coffee_handler)
    application.add_handler(back_handler)
    application.add_handler(echo_handler)

    application.run_polling()
