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


async def unknown(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Вибачте, я вас не зрозумів :(")


async def start(update: Update, context: CallbackContext):
    context.user_data['is_menu'] = True
    print("def start this is context.user.data", context.user_data)
    buttons = [
        [KeyboardButton("Меню Закладу")],
        [KeyboardButton("Шо мені випити?")],
        [KeyboardButton("ЗАБРОНЮВАТИ САМОСИ!")],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons)
    text = "Вітаємо в Діджиталізованому Мускаті"
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text,
                                   reply_markup=reply_markup)


async def menu(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if context.user_data.get("is_menu"):
        buttons = [
            [KeyboardButton("Напої")],
            [KeyboardButton("Десерти")],
            [KeyboardButton("Головне меню")],
        ]
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Виберіть розділ:",
                                       reply_markup=ReplyKeyboardMarkup(buttons))
    elif context.user_data.get('is_random'):
        ...
    else:
        return await start(update, context)


async def drinks(update: Update, context: CallbackContext.DEFAULT_TYPE):
    print('def drinks')
    if context.user_data.get("is_menu"):
        context.user_data["is_cold"] = None
        buttons = [
            [KeyboardButton("Так")],
            [KeyboardButton("Ні")],
            [KeyboardButton("Головне меню")]
        ]
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Тобі спекотно:",
                                       reply_markup=ReplyKeyboardMarkup(buttons))
    elif context.user_data.get('is_random'):
        ...
    else:
        return await start(update, context)


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


async def coffee(update: Update, context: CallbackContext):
    print('def coffee', context.user_data["is_cold"])
    if context.user_data.get("is_menu"):
        buttons = [
            [KeyboardButton("Кава")],
            [KeyboardButton("Інше")],
            [KeyboardButton("Головне меню")],
        ]
        if update.message['text'] == 'Так':
            context.user_data["is_cold"] = True
            print('this is true')
        elif update.message['text'] == 'Ні':
            context.user_data["is_cold"] = False
            print('this is false')

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Кава чи не Кава:",  # \n" + "\n".join(result),
                                       reply_markup=ReplyKeyboardMarkup(buttons))
    elif context.user_data.get('is_random'):
        ...
    else:
        return await start(update, context)


# defaults = {
#     'parent_id': None,
# }


def build_menu_item_query(options):
    sql = 'SELECT * FROM menu_item where '
    conditions = []

    for k, v in options.items():
        if v is None:
            s = "is NULL"
        elif v is True:
            s = "= True"
        else:
            s = "= False"
        conditions.append(f'{k} {s}')
    return sql + ' AND '.join(conditions)


async def coffee_or_not(update: Update, context: CallbackContext.DEFAULT_TYPE):
    print('def coffee+or_not')
    if context.user_data.get('is_menu'):
        buttons = [
            [KeyboardButton("Меню Закладу")],
            [KeyboardButton("Головне меню")],
        ]

        check_data_cold = context.user_data["is_cold"]
        is_coffee = update.message['text'] == 'Кава'

        print(check_data_cold, is_coffee)

        sql = build_menu_item_query({
            'is_coffee': is_coffee,
            'parent_id': None,
            'is_cold': check_data_cold,
        })
        print("this  is SQL:", sql)
        result = await query_menu_items(sql)

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="str\n" + "\n".join(result),
                                       reply_markup=ReplyKeyboardMarkup(buttons))

    elif context.user_data.get('is_random'):
        ...
    else:
        return await start(update, context)

if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TOKEN).build()

    start_handler = CommandHandler('start', start)
    menu_handler = MessageHandler(filters.Regex('Меню Закладу'), menu)
    main_menu_handler = MessageHandler(filters.Regex("Головне меню"), start)
    coffee_handler = MessageHandler(filters.Regex('Так'), coffee)
    coffee_2_handler = MessageHandler(filters.Regex('Ні'), coffee)
    coffee_or_not_handler = MessageHandler(filters.Regex('Кава'), coffee_or_not)
    coffee_or_not_handler2 = MessageHandler(filters.Regex('Інше'), coffee_or_not)
    back_handler = MessageHandler(filters.Regex('Назад до меню'), menu)
    drinks_handler = MessageHandler(filters.Regex('Напої'), drinks)
    unknown_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), unknown)

    application.add_handler(start_handler)
    application.add_handler(menu_handler)
    application.add_handler(drinks_handler)
    application.add_handler(main_menu_handler)
    application.add_handler(coffee_handler)
    application.add_handler(coffee_2_handler)
    application.add_handler(coffee_or_not_handler)
    application.add_handler(coffee_or_not_handler2)
    application.add_handler(back_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
