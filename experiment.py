import asyncio
import logging
import prettytable as pt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from telegram import *
from telegram.constants import ParseMode, ChatAction
from telegram.ext import *
from functools import wraps
import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG if config.DEBUG else logging.INFO
)

engine = create_async_engine(config.DB_URI)

BACK_TEXT = 'Назад'
DEFAULT_TEXT = "Вибачте, не зрозумів вас"

MENU_DEFINITION = {
    "message": "Вітаємо",
    "buttons": [
        {
            "title": "Меню",
            # "context_key": "is_menu",
            "reply": "Оберіть розділ",
            "has_back": True,
            "buttons": [
                {
                    "title": "Напої",
                    # "context_key": "is_drink"
                    "reply": "Оберіть",
                    "has_back": True,
                    "buttons": [
                        {
                            "title": "Кава",
                            "context_key": "",
                            "reply": "Оберіть",
                            "has_back": True,
                            "buttons": [
                                {
                                    "title": "Холодна",
                                    "reply": "Оберіть",
                                    "context_key": "",
                                    "has_back": True,
                                    "buttons": [
                                        {
                                            "title": "Чорна кава",
                                            "reply": "Оберіть",
                                            "context_key": "",
                                            "has_back": True,
                                            "callback_data": {
                                                "is_coffee": True,
                                                "is_cold": True,
                                                "is_black_coffee": True,
                                                "is_milk": False,
                                            },
                                            "callback": "get_menu_items",
                                        },
                                        {
                                            "title": "Молочна кава",
                                            "context_key": "",
                                        },
                                        {
                                            "title": "Альтернативно-молочна кава",
                                            "context_key": "",
                                        },
                                        {
                                            "title": "На фреші",
                                            "context_key": "",

                                        },
                                    ]
                                },
                                {
                                    "title": "Гаряча",
                                    "context_key": "",
                                    "buttons": [

                                    ],
                                },
                            ]
                        },
                        {
                            "title": "Інше",
                            "context_key": "",
                            "buttons": [
                                {
                                    "title": "Холодне",
                                    "context_key": "",
                                    "buttons": [
                                        {
                                            "title": "З молоком",
                                            "context_key": "",
                                        },
                                        {
                                            "title": "З альтернативним молоком",
                                            "context_key": "",
                                        },
                                        {
                                            "title": "На фреші",
                                            "context_key": "",

                                        },
                                    ]
                                },
                                {
                                    "title": "Гаряче",
                                    "context_key": "",
                                    "buttons": [

                                    ]
                                },
                            ]
                        },
                        {
                            "title": "Десерти",
                            "buttons": [

                            ],
                        },
                    ]
                },
            ]
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
    ],
}


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

    result = await query_menu_items(sql)
    args['text'] = 'Тримай Друже☺️:\n\n\n' f'```{result}```'
    args['parse_mode'] = ParseMode.MARKDOWN_V2

    return args


def get_random_item(data, args):
    sql = build_menu_item_query(data) + ' ORDER BY RANDOM() LIMIT 1'

    result = await query_menu_items(sql)
    args['text'] = 'Тримай Друже☺️:\n\n\n' f'```{result}```'
    args['parse_mode'] = ParseMode.MARKDOWN_V2

    return args


async def handler(update: Update, context: CallbackContext):
    session_context = context.user_data.get('session_context') or []
    print('session_context:', session_context)

    message = update.message.text

    active_item = MENU_DEFINITION

    if message == BACK_TEXT:
        session_context = session_context[:-1]

        for index in session_context:
            active_item = active_item['buttons'][index]

        selected_button = active_item
    else:

        for index in session_context:
            active_item = active_item['buttons'][index]

        selected_button = None
        selected_index = None
        for i in range(len(active_item['buttons'])):
            button = active_item['buttons'][i]
            if message == button['title']:
                selected_button = button
                selected_index = i
                break

        session_context.append(selected_index)

    if selected_button is None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=DEFAULT_TEXT)
        return await start(update, context)

    context.user_data['session_context'] = session_context

    buttons = []
    if 'buttons' in selected_button:
        buttons = [[KeyboardButton(item['title'])] for item in selected_button['buttons']]

    if 'has_back' in selected_button:
        buttons.append([KeyboardButton(BACK_TEXT)])

    args = {
        'chat_id': update.effective_chat.id,
        'text': selected_button.get('reply') or DEFAULT_TEXT,
    }

    if "callback" in selected_button:
        if selected_button["callback"] == "get_menu_items":
            args = await get_menu_items(selected_button.get("callback_data"), args)
        elif selected_button["callback"] == "get_random_item":
            args = await get_random_item(selected_button.get("callback_data"), args)

    args['reply_markup'] = ReplyKeyboardMarkup(buttons)

    return await context.bot.send_message(**args)


async def start(update: Update, context: CallbackContext):
    print("def start this is context.user.data", context.user_data)

    context.user_data['session_context'] = []

    buttons = [[KeyboardButton(item['title'])] for item in MENU_DEFINITION['buttons']]

    reply_markup = ReplyKeyboardMarkup(buttons)
    text = "Вітаємо в Діджиталізованому Мускаті"
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text,
                                   reply_markup=reply_markup)


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handler))

    application.run_polling()
