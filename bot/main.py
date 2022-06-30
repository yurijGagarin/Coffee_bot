import json
import logging
import random

import prettytable as pt
from prettytable import ALL
from telegram import *
from telegram.constants import ParseMode
from telegram.ext import *

import config
from navigation import get_menu_definition, \
    HOME_BUTTON, BACK_TEXT, ROLL_BUTTON, RANDOM_MENU_ITEM, HELP_BUTTON, MISUNDERSTOOD_TEXT, DEFAULT_TEXTS, HELP_TEXT
from models import User as UserModel

from db import getting_users_from_session, query_menu_items, get_user, verify_user, \
    samos_order, get_user_by_id, get_verified_user

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG if config.DEBUG else logging.INFO
)

NOT_NULL = "not Null"


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
    args['text'] = f'Друже, спробуй \n<b>{item["name"]}</b> ({item["price"]} грн)\n' \
                   f'{item["description"]} \n<b>{item["volume"]}</b> '
    args['parse_mode'] = ParseMode.HTML

    return args


async def get_active_item(update: Update, context: CallbackContext, user: UserModel):
    session_context = context.user_data.get('session_context') or []
    print('session_context:', session_context)
    menu_definition = await get_menu_definition(user)
    active_item = menu_definition
    for index in session_context:
        print("index", index)
        print("active_item", active_item)
        active_item = active_item['children'][index]
        print("active_item2", active_item)

    message_text = update.message.text

    if message_text == HOME_BUTTON:
        context.user_data['session_context'] = []
        active_item = menu_definition
        active_item['reply'] = 'Давай спробуємо знову 😁'
        return active_item

    elif message_text == BACK_TEXT and len(session_context):
        session_context = session_context[:-1]
        context.user_data['session_context'] = session_context
        new_item = menu_definition
        for index in session_context:
            new_item = new_item['children'][index]
        return new_item
    elif (message_text == ROLL_BUTTON or update.message.dice) and len(session_context):
        return RANDOM_MENU_ITEM
    elif message_text == HELP_BUTTON:
        return await help_command(update, context)
    else:
        for key, button in active_item['children'].items():
            if message_text == button['title']:
                session_context.append(key)
                context.user_data['session_context'] = session_context
                return button
        await context.bot.send_message(chat_id=update.effective_chat.id, text=MISUNDERSTOOD_TEXT)

        if active_item == RANDOM_MENU_ITEM:
            context.user_data['session_context'] = []
            return menu_definition

        return active_item


async def unverified_users(args, update: Update, context: CallbackContext):
    users = await get_verified_user(False)

    keyboard = []
    for row in users:
        keyboard.append([InlineKeyboardButton(row.User.nickname, callback_data=json.dumps({
            'method': 'verify', 'id': row.User.id,
        }))])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Unverified users:',
        reply_markup=reply_markup
    )
    args['text'] = 'Please select user to verify'

    return args


async def quantity_add(args, update: Update, context: CallbackContext):
    await booking_info(args, update, context)
    keyboard = [[InlineKeyboardButton(
        f'-1', callback_data=json.dumps({'method': "order",
                                         'math': "decrease",
                                         'samos': "sweet"})),
        InlineKeyboardButton(
            f'+1', callback_data=json.dumps({'method': "order",
                                             'math': "increase",
                                             'samos': "sweet"}))
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='СОЛОДКІ:',
        reply_markup=reply_markup
    )

    second_keyboard = [[InlineKeyboardButton(
        f'-1', callback_data=json.dumps({'method': "order",
                                         'math': "decrease",
                                         'samos': "salty"})),
        InlineKeyboardButton(
            f'+1', callback_data=json.dumps({'method': "order",
                                             'math': "increase",
                                             'samos': "salty"}))
    ]]

    reply_markup = InlineKeyboardMarkup(second_keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='СОЛОНІ:',
        reply_markup=reply_markup
    )
    return args


async def booking_info(args, update: Update, context: CallbackContext):
    booking = await get_user_by_id(update.effective_user.id)
    print("booking", booking)
    args['text'] = f'Солоних самосів: <b>{booking.User.salty}</b>\n' \
                   f'Солодких самосів: <b>{booking.User.sweet}</b>'
    args['parse_mode'] = ParseMode.HTML

    return args


async def reply(update: Update, context: CallbackContext, active_item):
    session_context = context.user_data.get('session_context') or []
    print('session_context', session_context)
    print('active_item', active_item)
    buttons = []
    if 'children' in active_item:
        buttons = [[KeyboardButton(item['title'])] for item in active_item['children'].values()]

    if len(session_context) > 0:
        additional_buttons = [KeyboardButton(BACK_TEXT)]
        if len(session_context) > 1:
            additional_buttons.append(KeyboardButton(HOME_BUTTON))
        buttons.append(additional_buttons)

    if 'show_help' in active_item:
        buttons.append([KeyboardButton(HELP_BUTTON)])
    args = {
        'chat_id': update.effective_chat.id,
        'text': active_item.get('reply') or random.choice(DEFAULT_TEXTS),
    }

    if "callback" in active_item:
        if active_item["callback"] == "get_menu_items":
            args = await get_menu_items(active_item.get("callback_data"), args)
        elif active_item["callback"] == "get_random_item":
            args = await get_random_item(active_item.get("callback_data"), args)
        elif active_item["callback"] == "unverified_users":
            args = await unverified_users(args, update, context)
        elif active_item["callback"] == "quantity":
            args = await quantity_add(args, update, context)
        elif active_item["callback"] == "booking_info":
            args = await booking_info(args, update, context)

    if 'reply_markup' not in args:
        args['reply_markup'] = ReplyKeyboardMarkup(buttons)

    return await context.bot.send_message(**args)


async def handler(update: Update, context: CallbackContext):
    user = await get_user(update)

    active_item = await get_active_item(update=update, context=context, user=user)

    if active_item:
        await reply(update=update, context=context, active_item=active_item)


async def start(update: Update, context: CallbackContext):
    print("def start this is context.user.data", context.user_data)

    context.user_data['session_context'] = []

    user = await get_user(update)
    menu_definition = await get_menu_definition(user)

    await reply(update, context, menu_definition)


async def help_command(update: Update, context: CallbackContext):
    context.user_data['session_context'] = context.user_data.get('session_context')

    await update.message.reply_text(HELP_TEXT, parse_mode=ParseMode.HTML)


async def random_command(update: Update, context: CallbackContext):
    await reply(update, context, active_item=RANDOM_MENU_ITEM)


async def keyboard_callback(update, context, args):
    query = update.callback_query
    print('query:', query)

    payload: dict = json.loads(query.data)
    if payload:
        method = payload.get('method')
        if method:
            if method == 'verify':
                print('Verify')
                user_id = payload.get('id')
                print('id:', user_id)
                await verify_user(user_id)
                await query.answer(f'Verified')
            elif method == 'order':
                type_of_samos = payload.get('samos')
                user_id = update.effective_user.id
                math = payload.get('math')
                await samos_order(type_of_samos, user_id, math)
                await quantity_add(args=args, update=update, context=context)


def main():
    application = ApplicationBuilder().token(config.TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('random', random_command))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(MessageHandler((filters.TEXT | filters.Dice.DICE) & (~filters.COMMAND), handler))

    application.add_handler(CallbackQueryHandler(keyboard_callback))

    application.run_polling()


if __name__ == '__main__':
    main()
