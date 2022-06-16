import logging
import random

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
    level=logging.DEBUG if config.DEBUG else logging.INFO
)

engine = create_async_engine(config.DB_URI)

HOME_BUTTON = '🏠'
BACK_TEXT = 'Назад'
MISUNDERSTOOD_TEXT = "Вибачте, не зрозумів вас"
DEFAULT_TEXTS = [':)', '😊']
NOT_NULL = "not Null"
MENU_DEFINITION = {
    "reply": "Вітаємо в Діджиталізованому Мускаті",
    "buttons": [
        {
            "title": "Меню",
            "reply": "Оберіть розділ",
            "buttons": [
                {
                    "title": "Напої",
                    "reply": "Оберіть",
                    "buttons": [
                        {
                            "title": "Кава",
                            "reply": "Оберіть",
                            "buttons": [
                                {
                                    "title": "Холодна",
                                    "reply": "Оберіть",
                                    "buttons": [
                                        {
                                            "title": "Чорна кава",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_coffee": True,
                                                "is_cold": True,
                                                "is_black_coffee": True,
                                            },
                                            "callback": "get_menu_items",
                                        },
                                        {
                                            "title": "Молочна кава",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_coffee": True,
                                                "is_cold": True,
                                                "is_milk": True,
                                            },
                                            "callback": "get_menu_items",
                                        },
                                        {
                                            "title": "Альтернативно-молочна кава",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_coffee": True,
                                                "is_cold": True,
                                                "is_milk": True,
                                                "is_lact_free": True,
                                                "parent_id": NOT_NULL,
                                            },
                                            "callback": "get_menu_items",
                                        },
                                        {
                                            "title": "На фреші",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_coffee": True,
                                                "is_cold": True,
                                                "is_fresh": True,
                                            },
                                            "callback": "get_menu_items",

                                        },
                                    ]
                                },
                                {
                                    "title": "Гаряча",
                                    "reply": "Оберіть",
                                    "buttons": [
                                        {
                                            "title": "Чорна кава",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_coffee": True,
                                                "is_black_coffee": True,

                                            },
                                            "callback": "get_menu_items",
                                        },
                                        {
                                            "title": "Молочна кава",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_coffee": True,
                                                "is_milk": True,
                                            },
                                            "callback": "get_menu_items",
                                        },
                                        {
                                            "title": "Альтернативно-молочна кава",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_coffee": True,
                                                "is_milk": True,
                                                "is_lact_free": True,
                                            },
                                            "callback": "get_menu_items",
                                        },
                                        {
                                            "title": "На фреші",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_coffee": True,
                                                "is_fresh": True,
                                            },
                                            "callback": "get_menu_items",

                                        },
                                    ]
                                },
                            ]
                        },
                        {
                            "title": "Матча",
                            "reply": "Оберіть",
                            "buttons": [
                                {
                                    "title": "Холодна",
                                    "reply": "Оберіть",
                                    "buttons": [
                                        {
                                            "title": "Без молока",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_matcha": True,
                                                "is_cold": True,
                                            },
                                            "callback": "get_menu_items",
                                        },
                                        {
                                            "title": "З молоком",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_matcha": True,
                                                "is_cold": True,
                                                "is_milk": True,
                                            },
                                            "callback": "get_menu_items",
                                        },
                                        {
                                            "title": "Альтернативно-молочна матча",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_matcha": True,
                                                "is_cold": True,
                                                "is_milk": True,
                                                "is_lact_free": True,
                                            },
                                            "callback": "get_menu_items",
                                        },
                                        {
                                            "title": "На фреші",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_matcha": True,
                                                "is_cold": True,
                                                "is_fresh": True,
                                            },
                                            "callback": "get_menu_items",

                                        },
                                    ]
                                },
                                {
                                    "title": "Гаряча",
                                    "reply": "Оберіть",
                                    "buttons": [
                                        {
                                            "title": "Без молока",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_matcha": True,

                                            },
                                            "callback": "get_menu_items",
                                        },
                                        {
                                            "title": "З молоком",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_matcha": True,
                                                "is_milk": True,
                                            },
                                            "callback": "get_menu_items",
                                        },
                                        {
                                            "title": "Альтернативно-молочна матча",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_matcha": True,
                                                "is_milk": True,
                                                "is_lact_free": True,
                                            },
                                            "callback": "get_menu_items",
                                        },
                                        {
                                            "title": "На фреші",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_matcha": True,
                                                "is_fresh": True,
                                            },
                                            "callback": "get_menu_items",

                                        },
                                    ]
                                },
                            ]
                        },
                        {
                            "title": "Чай",
                            "reply": "Оберіть",
                            "callback_data": {
                                "is_tea": True,

                            },
                            "callback": "get_menu_items",
                        },
                        {
                            "title": "Інше",
                            "reply": "Оберіть",
                            "callback_data": {
                                "is_other": True,
                                "skip_defaults": True
                            },
                            "callback": "get_menu_items",

                        },

                    ]
                },
                {
                    "title": "Десерти",
                    "reply": '''
                    РОЗДІЛ В РОЗРОБЦІ
Вибачте за незручності.
Слідкуйте за новинами нашого бота щоб бути в курсі новин.
                                ''',
                    "buttons": [

                    ],
                },

            ],
        },
        {
            "title": "Шо мені випити?",
            "buttons": [
                {
                    "title": "Вибір",
                    "context_key": "is_random",
                },
            ]
        },
    ]
}


def build_menu_item_query(options):
    options = options.copy()
    sql = 'SELECT * FROM menu_item where '
    conditions = []

    skip_defaults = False
    if "skip_defaults" in options:
        del options['skip_defaults']
        skip_defaults = True

    defaults = {} if skip_defaults else {
        "is_coffee": False,
        "is_milk": False,
        "is_lact_free": False,
        "is_tea": False,
        "is_matcha": False,
        "is_cold": False,
        "is_black_coffee": False,
        "is_fresh": False,
    }
    for k, v in (defaults | options).items():
        if v is None:
            s = "is NULL"
        elif v is True:
            s = "= True"
        elif v == NOT_NULL:
            s = "is not NULL"
        else:
            s = "= False"
        conditions.append(f'{k} {s}')
    return sql + ' AND '.join(conditions)


async def query_menu_items(sql_query):
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    result = []
    print('parsing result', result)
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


async def get_menu_items(data, args):
    sql = build_menu_item_query(data)
    print("this is query:", sql)
    result = await query_menu_items(sql)
    args['text'] = 'Тримай Друже☺️:\n\n\n' f'```{result}```'
    args['parse_mode'] = ParseMode.MARKDOWN_V2

    return args


async def get_random_item(data, args):
    sql = build_menu_item_query(data) + ' ORDER BY RANDOM() LIMIT 1'

    result = await query_menu_items(sql)
    args['text'] = 'Тримай Друже☺️:\n\n\n' f'```{result}```'
    args['parse_mode'] = ParseMode.MARKDOWN_V2

    return args


async def get_active_item(update: Update, context: CallbackContext):
    session_context = context.user_data.get('session_context') or []
    print('session_context:', session_context)
    active_item = MENU_DEFINITION
    for index in session_context:
        active_item = active_item['buttons'][index]
    # print('active item:', active_item['reply'])

    message = update.message.text

    if message == HOME_BUTTON:
        context.user_data['session_context'] = []
        active_item = MENU_DEFINITION.copy()
        active_item['reply'] = 'Давай спробуємо знову 😁'
        return active_item

    elif message == BACK_TEXT and len(session_context):
        session_context = session_context[:-1]
        context.user_data['session_context'] = session_context
        new_item = MENU_DEFINITION
        for index in session_context:
            new_item = new_item['buttons'][index]
        return new_item
    else:
        for i in range(len(active_item['buttons'])):
            button = active_item['buttons'][i]
            if message == button['title']:
                session_context.append(i)
                context.user_data['session_context'] = session_context
                return button

        await context.bot.send_message(chat_id=update.effective_chat.id, text=MISUNDERSTOOD_TEXT)
        return active_item


async def reply(update: Update, context: CallbackContext, active_item):
    session_context = context.user_data.get('session_context') or []

    buttons = []
    if 'buttons' in active_item:
        buttons = [[KeyboardButton(item['title'])] for item in active_item['buttons']]

    if len(session_context) > 0:
        additional_buttons = [KeyboardButton(BACK_TEXT)]
        if len(session_context) > 1:
            additional_buttons.append(KeyboardButton(HOME_BUTTON))
        buttons.append(additional_buttons)

    args = {
        'chat_id': update.effective_chat.id,
        'text': active_item.get('reply') or random.choice(DEFAULT_TEXTS),
    }

    if "callback" in active_item:
        if active_item["callback"] == "get_menu_items":
            args = await get_menu_items(active_item.get("callback_data"), args)
        elif active_item["callback"] == "get_random_item":
            args = await get_random_item(active_item.get("callback_data"), args)

    args['reply_markup'] = ReplyKeyboardMarkup(buttons)

    return await context.bot.send_message(**args)


async def handler(update: Update, context: CallbackContext):
    active_item = await get_active_item(update=update, context=context)

    print(active_item.get('reply'))

    return await reply(update=update, context=context, active_item=active_item)


async def start(update: Update, context: CallbackContext):
    print("def start this is context.user.data", context.user_data)

    context.user_data['session_context'] = []

    await reply(update, context, MENU_DEFINITION)


# async def start_2(update: Update, context: CallbackContext):
#     print("def start this is context.user.data", context.user_data)
#
#     context.user_data['session_context'] = []
#
#     buttons = [[KeyboardButton(item['title'])] for item in MENU_DEFINITION['buttons']]
#
#     reply_markup = ReplyKeyboardMarkup(buttons)
#     text = "😁"
#     await context.bot.send_message(chat_id=update.effective_chat.id,
#                                    text=text,
#                                    reply_markup=reply_markup)


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handler))
    # application.add_handler(MessageHandler(filters.ALL, handler))

    application.run_polling()
