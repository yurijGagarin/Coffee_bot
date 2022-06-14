import logging
import prettytable as pt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from telegram import *
from telegram.constants import ParseMode
from telegram.ext import *

import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

engine = create_async_engine(config.DB_DSN)


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


async def query_menu_items(sql_query):
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    result = []
    print('parsing result',  result)
    table = pt.PrettyTable(['Назва', 'Ціна'])
    table.align['Назва'] = 'l'
    table.align['Ціна'] = 'r'

    async with async_session() as session:
        r = await session.execute(sql_query)
        results_as_dict = r.mappings().all()
        for el in results_as_dict:
            name = el["name"]
            price = el["price"]
            table.add_row([name, price])
    return table


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
    context.user_data['is_random'] = False
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
    context.user_data['is_menu'] = False
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
    context.user_data["is_cold"] = False
    context.user_data["is_black_coffee"] = False
    context.user_data["is_lact_free"] = False
    context.user_data["is_milk"] = False
    context.user_data["is_coffee"] = False

    if context.user_data.get("is_menu") or context.user_data.get("is_random"):
        buttons = [
            [KeyboardButton("Кава")],
            [KeyboardButton("Інше")],
            [KeyboardButton("🏠")]
        ]
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Кава чи не Кава:",
                                       reply_markup=ReplyKeyboardMarkup(buttons))
    else:
        return await start(update, context)


async def cold(update: Update, context: CallbackContext):
    if update.message['text'] == 'Кава':
        context.user_data["is_coffee"] = True
    if context.user_data.get("is_menu") or context.user_data.get("is_random"):
        buttons = [
            [KeyboardButton("Бажаю холодний")],
            [KeyboardButton("Бажаю гарячий")],
            [KeyboardButton("🏠")],
        ]

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Холодний напій чи гарячий:",
                                       reply_markup=ReplyKeyboardMarkup(buttons))
    else:
        return await start(update, context)


async def milk(update: Update, context: CallbackContext):
    if update.message['text'] == "Бажаю холодний":
        context.user_data["is_cold"] = True

    buttons = [
        [KeyboardButton("Нічого проти молока не маю."), KeyboardButton("Лактоза не для мене.")],
        [KeyboardButton("🏠")],
    ]
    if context.user_data["is_coffee"]:
        buttons = [
            [KeyboardButton("Хочу просто чорної кави.")],
            [KeyboardButton("Нічого проти молока не маю."), KeyboardButton("Лактоза не для мене.")],
            [KeyboardButton("🏠")],
        ]

    if context.user_data.get("is_menu") or context.user_data.get("is_random"):

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="З молоком чи ні:",
                                       reply_markup=ReplyKeyboardMarkup(buttons))

    else:
        return await start(update, context)


async def final_step(update: Update, context: CallbackContext.DEFAULT_TYPE):
    print('def coffee+or_not')
    if update.message['text'] == 'Хочу просто чорної кави.':
        context.user_data["is_black_coffee"] = True
    elif update.message['text'] == 'Нічого проти молока не маю.':
        context.user_data["is_milk"] = True
    elif update.message['text'] == 'Лактоза не для мене.':
        context.user_data["is_lact_free"] = True

    if context.user_data.get('is_menu'):
        buttons = [
            [KeyboardButton("Меню Закладу")],
            [KeyboardButton("🏠")],
        ]

        sql = build_menu_item_query({
            'is_coffee': context.user_data["is_coffee"],
            'parent_id': None,
            'is_cold': context.user_data["is_cold"],
            'is_black_coffee': context.user_data["is_black_coffee"],
            'is_milk': context.user_data["is_milk"],
            'is_lact_free': context.user_data["is_lact_free"],
        })
        print("this  is SQL:", sql)
        result = await query_menu_items(sql)
        print("this is result_last", result)

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Тримай Друже☺️:\n\n\n' f'```{result}```',  # "\n".join(result),
                                       reply_markup=ReplyKeyboardMarkup(buttons),
                                       parse_mode=ParseMode.MARKDOWN_V2
                                       )

    elif context.user_data.get('is_random'):
        buttons = [
            [KeyboardButton("Меню Закладу")],
            [KeyboardButton("Спробувати ще раз")],
            [KeyboardButton("🏠")],
        ]

        sql = build_random_item_query({
            'is_coffee': context.user_data["is_coffee"],
            'is_cold': context.user_data["is_cold"],
            'is_black_coffee': context.user_data["is_black_coffee"],
            'is_milk': context.user_data["is_milk"],
            'is_lact_free': context.user_data["is_lact_free"],
        })
        print("this  is SQL:", sql)
        result = await query_menu_items(sql)
        print("this is result_last", result)

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'```{result}```',  # "\n".join(result),
                                       reply_markup=ReplyKeyboardMarkup(buttons),
                                       parse_mode=ParseMode.MARKDOWN_V2
                                       )
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
    application.add_handler(MessageHandler(filters.Regex("Бажаю холодний"), milk))
    application.add_handler(MessageHandler(filters.Regex("Бажаю гарячий"), milk))
    application.add_handler(MessageHandler(filters.Regex('Хочу просто чорної кави.'), final_step))
    application.add_handler(MessageHandler(filters.Regex('Нічого проти молока не маю.'), final_step))
    application.add_handler(MessageHandler(filters.Regex('Лактоза не для мене'), final_step))
    application.add_handler(MessageHandler(filters.Regex('Кава'), cold))
    application.add_handler(MessageHandler(filters.Regex('Інше'), cold))
    application.add_handler(MessageHandler(filters.Regex('Назад до меню'), menu))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), unknown))

    application.run_polling()
