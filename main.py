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
    context.user_data['is_menu'] = True
    if context.user_data.get("is_menu"):
        buttons = [
            [KeyboardButton("Напої")],
            [KeyboardButton("Десерти")],
            [KeyboardButton("🏠")],
        ]
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Виберіть розділ:",
                                       reply_markup=ReplyKeyboardMarkup(buttons))
    elif context.user_data.get('is_random'):
        ...
    else:
        return await start(update, context)


async def random(update: Update, context: CallbackContext.DEFAULT_TYPE):
    context.user_data['is_random'] = True
    buttons = [
        [KeyboardButton("Готовий")],
        [KeyboardButton("🏠")]
    ]
    text = '''
        Перед тобою твій персональний ДІДЖИТАЛІЗОВАНИЙ бариста.
        Якщо ти втомився від мук вибору:
        —"Що ж мені випити сьогодні"
        Або хочешь поєксперементувати то u're welcome!
        В іншому випадку тисни на 🏠
        '''

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text,
                                   reply_markup=ReplyKeyboardMarkup(buttons))


async def drinks(update: Update, context: CallbackContext.DEFAULT_TYPE):
    print('def drinks')
    print(context.user_data)
    if context.user_data.get("is_menu"):
        context.user_data["is_cold"] = None
        buttons = [
            [KeyboardButton("Так")],
            [KeyboardButton("Ні")],
            [KeyboardButton("🏠")]
        ]
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Тобі спекотно:",
                                       reply_markup=ReplyKeyboardMarkup(buttons))
    elif context.user_data.get('is_random'):
        context.user_data["is_cold"] = None
        buttons = [
            [KeyboardButton("Так")],
            [KeyboardButton("Ні")],
            [KeyboardButton("🏠")]
        ]
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Тобі спекотно:",
                                       reply_markup=ReplyKeyboardMarkup(buttons))
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
    if update.message['text'] == 'Так':
        context.user_data["is_cold"] = True
        print('this is true')
    elif update.message['text'] == 'Ні':
        context.user_data["is_cold"] = False
        print('this is false')
    if context.user_data.get("is_menu"):
        buttons = [
            [KeyboardButton("Кава")],
            [KeyboardButton("Інше")],
            [KeyboardButton("🏠")],
        ]

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Кава чи не Кава:",
                                       reply_markup=ReplyKeyboardMarkup(buttons))
    elif context.user_data.get('is_random'):
        buttons = [
            [KeyboardButton("Кава")],
            [KeyboardButton("Інше")],
            [KeyboardButton("🏠")],
        ]

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Кава чи не Кава:",
                                       reply_markup=ReplyKeyboardMarkup(buttons))
    else:
        return await start(update, context)


# defaults = {
#     'parent_id': None,
# }
def build_random_item_query(options):
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
    return sql + ' AND '.join(conditions) + ' ORDER BY RANDOM() LIMIT 1'


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
    check_data_cold = context.user_data["is_cold"]
    is_coffee = update.message['text'] == 'Кава'
    if context.user_data.get('is_menu'):
        buttons = [
            [KeyboardButton("Меню Закладу")],
            [KeyboardButton("🏠")],
        ]

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
        buttons = [
            [KeyboardButton("Меню Закладу")],
            [KeyboardButton("Спробувати ще раз")],
            [KeyboardButton("🏠")],
        ]

        print(check_data_cold, is_coffee)

        sql = build_random_item_query({
            'is_coffee': is_coffee,
            'is_cold': check_data_cold,
        })
        print("this  is SQL:", sql)
        result = await query_menu_items(sql)

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="str\n" + "\n".join(result),
                                       reply_markup=ReplyKeyboardMarkup(buttons))
    else:
        return await start(update, context)


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.Regex('🏠'), start))
    application.add_handler(MessageHandler(filters.Regex('Меню Закладу'), menu))
    application.add_handler(MessageHandler(filters.Regex('Напої'), drinks))
    application.add_handler(MessageHandler(filters.Regex('Готовий'), drinks))
    application.add_handler(MessageHandler(filters.Regex('Шо мені випити'), random))
    application.add_handler(MessageHandler(filters.Regex('Спробувати ще раз'), drinks))
    application.add_handler(MessageHandler(filters.Regex('Так'), coffee))
    application.add_handler(MessageHandler(filters.Regex('Ні'), coffee))
    application.add_handler(MessageHandler(filters.Regex('Кава'), coffee_or_not))
    application.add_handler(MessageHandler(filters.Regex('Інше'), coffee_or_not))
    application.add_handler(MessageHandler(filters.Regex('Назад до меню'), menu))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), unknown))

    application.run_polling()
