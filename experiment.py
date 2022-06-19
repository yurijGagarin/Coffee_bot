import logging
import random

import prettytable as pt
from prettytable import HEADER, ALL
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
ROLL_BUTTON = '🎲'
HOME_BUTTON = '🏠'
BACK_TEXT = 'Назад'
MISUNDERSTOOD_TEXT = "Вибачте, не зрозумів вас"
DEFAULT_TEXTS = ['🙂', '😊', '🙃']
NOT_NULL = "not Null"
HELP_TEXT = '''Вітаємо, це словничок скорочень Мускат Бота.
[Б/Л] --> Замість звичайного молока використовується безлактозне.
[Р] --> Замість звичайного молока використовується рослинне.
Іммерсія --> Спосіб заварювання, шляхом постійного контакту води з тим, що ти заварюеєшь.
        '''

RANDOM_MENU_ITEM = {
    "title": "Що мені випити?",
    "callback_data": {
        "skip_defaults": True,
        "is_deserts": False
    },
    "callback": "get_random_item",
    "buttons": [
        {
            "title": ROLL_BUTTON,
        },
    ]
}

MENU_DEFINITION = {
    "reply": "👋 Вітаємо в діджиталізованому Мускаті 🙂",
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
                                            "title": "Без молока",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_coffee": True,
                                                "is_black_coffee": True,
                                                "is_cold": True

                                            },
                                            "callback": "get_menu_items",
                                        },
                                        {
                                            "title": "З молоком",
                                            "reply": "Оберіть",
                                            "buttons": [
                                                {
                                                    "title": "Звичайне",
                                                    "reply": "Оберіть",
                                                    "callback_data": {
                                                        "is_coffee": True,
                                                        "is_milk": True,
                                                        "is_cold": True

                                                    },
                                                    "callback": "get_menu_items",
                                                },
                                                {
                                                    "title": "Безлактозне",
                                                    "reply": "Оберіть",
                                                    "callback_data": {
                                                        "is_coffee": True,
                                                        "is_lact_free_milk": True,
                                                        "is_cold": True

                                                    },
                                                    "callback": "get_menu_items",
                                                },
                                                {
                                                    "title": "Рослинне",
                                                    "reply": "Оберіть",
                                                    "callback_data": {
                                                        "is_coffee": True,
                                                        "is_vegan_milk": True,
                                                        "is_cold": True

                                                    },
                                                    "callback": "get_menu_items",
                                                },
                                            ]
                                        },
                                        {
                                            "title": "На фреші",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_coffee": True,
                                                "is_fresh": True,
                                                "is_cold": True
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
                                            "title": "З молоком",
                                            "reply": "Оберіть",
                                            "buttons": [
                                                {
                                                    "title": "Звичайне",
                                                    "reply": "Оберіть",
                                                    "callback_data": {
                                                        "is_coffee": True,
                                                        "is_milk": True,

                                                    },
                                                    "callback": "get_menu_items",
                                                },
                                                {
                                                    "title": "Безлактозне",
                                                    "reply": "Оберіть",
                                                    "callback_data": {
                                                        "is_coffee": True,
                                                        "is_lact_free_milk": True,

                                                    },
                                                    "callback": "get_menu_items",
                                                },
                                                {
                                                    "title": "Рослинне",
                                                    "reply": "Оберіть",
                                                    "callback_data": {
                                                        "is_coffee": True,
                                                        "is_vegan_milk": True,

                                                    },
                                                    "callback": "get_menu_items",
                                                },
                                            ]
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
                                            "buttons": [
                                                {
                                                    "title": "Звичайне",
                                                    "reply": "Оберіть",
                                                    "callback_data": {
                                                        "is_matcha": True,
                                                        "is_milk": True,
                                                        "is_cold": True

                                                    },
                                                    "callback": "get_menu_items",
                                                },
                                                {
                                                    "title": "Безлактозне",
                                                    "reply": "Оберіть",
                                                    "callback_data": {
                                                        "is_matcha": True,
                                                        "is_lact_free_milk": True,
                                                        "is_cold": True

                                                    },
                                                    "callback": "get_menu_items",
                                                },
                                                {
                                                    "title": "Рослинне",
                                                    "reply": "Оберіть",
                                                    "callback_data": {
                                                        "is_matcha": True,
                                                        "is_vegan_milk": True,
                                                        "is_cold": True

                                                    },
                                                    "callback": "get_menu_items",
                                                },
                                            ]
                                        },
                                        {
                                            "title": "На фреші",
                                            "reply": "Оберіть",
                                            "callback_data": {
                                                "is_matcha": True,
                                                "is_fresh": True,
                                                "is_cold": True
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
                                            "buttons": [
                                                {
                                                    "title": "Звичайне",
                                                    "reply": "Оберіть",
                                                    "callback_data": {
                                                        "is_matcha": True,
                                                        "is_milk": True,

                                                    },
                                                    "callback": "get_menu_items",
                                                },
                                                {
                                                    "title": "Безлактозне",
                                                    "reply": "Оберіть",
                                                    "callback_data": {
                                                        "is_matcha": True,
                                                        "is_lact_free_milk": True,

                                                    },
                                                    "callback": "get_menu_items",
                                                },
                                                {
                                                    "title": "Рослинне",
                                                    "reply": "Оберіть",
                                                    "callback_data": {
                                                        "is_matcha": True,
                                                        "is_vegan_milk": True,

                                                    },
                                                    "callback": "get_menu_items",
                                                },
                                            ]
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
                    # "reply": "Тут ви зможете ознайомитись з тим, які десерти в нас бувають. ",
                    "buttons": [

                    ],
                    "callback_data": {
                        "is_deserts": True,
                        "skip_defaults": True
                    },
                    "callback": "get_menu_items",
                },

            ],
        },
        RANDOM_MENU_ITEM,
    ],
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
        "is_lact_free_milk": False,
        "is_vegan_milk": False,
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
    async with async_session() as session:
        r = await session.execute(sql_query)
        results_as_dict = r.mappings().all()

    return results_as_dict


def format_table(results_as_dict):
    table = pt.PrettyTable(['Назва', 'Ціна'], hrules=ALL)
    print(table)
    table.align['Назва'] = 'l'
    table.align['Ціна'] = 'r'

    for el in results_as_dict:
        name = el["name"]
        price = el["price"]
        table.add_row([name, price])
    return table


async def get_menu_items(data, args):
    sql = build_menu_item_query(data)
    print("this is query:", sql)
    result = await query_menu_items(sql)
    result = format_table(result)
    args['text'] = 'Тримай Друже☺️:\n' f'```{result}```'
    args['parse_mode'] = ParseMode.MARKDOWN_V2

    return args


async def get_random_item(data, args):
    sql = build_menu_item_query(data) + ' ORDER BY RANDOM() LIMIT 1'
    print("this is query:", sql)
    result = await query_menu_items(sql)
    item = result[0]

    args['text'] = f'Друже, спробуй \n<b>{item["name"]}</b> ({item["price"]} грн)'
    args['parse_mode'] = ParseMode.HTML

    return args


async def get_active_item(update: Update, context: CallbackContext):
    session_context = context.user_data.get('session_context') or []
    print('session_context:', session_context)
    active_item = MENU_DEFINITION
    for index in session_context:
        active_item = active_item['buttons'][index]

    message_text = update.message.text

    print('dice:', update.message.dice)
    if message_text == HOME_BUTTON:
        context.user_data['session_context'] = []
        active_item = MENU_DEFINITION.copy()
        active_item['reply'] = 'Давай спробуємо знову 😁'
        return active_item

    elif message_text == BACK_TEXT and len(session_context):
        session_context = session_context[:-1]
        context.user_data['session_context'] = session_context
        new_item = MENU_DEFINITION
        for index in session_context:
            new_item = new_item['buttons'][index]
        return new_item
    elif (message_text == ROLL_BUTTON or update.message.dice) and len(session_context):
        return RANDOM_MENU_ITEM
    else:
        for i in range(len(active_item['buttons'])):
            button = active_item['buttons'][i]
            if message_text == button['title']:
                session_context.append(i)
                context.user_data['session_context'] = session_context
                return button
        await context.bot.send_message(chat_id=update.effective_chat.id, text=MISUNDERSTOOD_TEXT)

        if active_item == RANDOM_MENU_ITEM:
            context.user_data['session_context'] = []
            return MENU_DEFINITION

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


async def help_command(update: Update, context: CallbackContext):

    context.user_data['session_context'] = context.user_data.get('session_context')

    await update.message.reply_text(HELP_TEXT)



if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(MessageHandler((filters.TEXT | filters.Dice.DICE) & (~filters.COMMAND), handler))
    # application.add_handler(MessageHandler(filters.ALL, handler))

    application.run_polling()
