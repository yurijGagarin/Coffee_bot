import json
import logging
import random

import prettytable as pt
import telegram
from prettytable import ALL
from telegram import *
from telegram.constants import ParseMode
from telegram.ext import *

import config
from bot.user_notifications import send_message_to_active_user
from constants import PRODUCTS
from db import (
    query_menu_items,
    get_user,
    verify_user,
    get_verified_user,
    update_booking_qty,
    get_booking_for_user,
)
from models import User as UserModel
from navigation import (
    get_menu_definition,
    HOME_BUTTON,
    HOME_REPLY_WITH_RANDOM,
    BACK_TEXT,
    ROLL_BUTTON,
    get_random_menu_item_btn,
    HELP_BUTTON,
    MISUNDERSTOOD_TEXT,
    DEFAULT_TEXTS,
    HELP_TEXT, HOME_REPLY, WELCOME_TEXT,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG if config.DEBUG else logging.INFO,
)

NOT_NULL = "not Null"
SOCIAL_NETWORK_GIF = "CgACAgIAAxkBAAIrjGLZrt-12f_XNhD9Jb6kGPx6c382AAKfHQAC2onRSon3dI6yX2JGKQQ"


def build_menu_item_query(options):
    options = options.copy()
    sql = "SELECT * FROM menu_item where "
    conditions = []

    skip_defaults = False
    if "skip_defaults" in options:
        del options["skip_defaults"]
        skip_defaults = True

    defaults = (
        {}
        if skip_defaults
        else {
            "is_coffee": False,
            "is_milk": False,
            "is_lact_free_milk": False,
            "is_vegan_milk": False,
            "is_tea": False,
            "is_matcha": False,
            "is_season": False,
            "is_black_coffee": False,
            "is_fresh": False,
            "available": True,
        }
    )
    for k, v in (defaults | options).items():
        if v is None:
            s = "is NULL"
        elif v is True:
            s = "= True"
        elif v == NOT_NULL:
            s = "is not NULL"
        else:
            s = "= False"
        conditions.append(f"{k} {s}")

    return sql + " AND ".join(conditions)


def format_table(results_as_dict):
    table = pt.PrettyTable(["Назва", "Ціна"], hrules=ALL)
    table.align["Назва"] = "l"
    table.align["Ціна"] = "r"

    for el in results_as_dict:
        name = el["name"]
        price = str(el["price"])
        alt_prices = el.get("alt_prices")
        alt_prices_dict = json.loads(alt_prices)
        if alt_prices_dict:
            name += "\n" + "\n".join(alt_prices_dict.keys())
            price += "\n" + "\n".join(map(str, alt_prices_dict.values()))
        table.add_row([name, price])

    return table


async def get_menu_items(data, args):
    sql = build_menu_item_query(data)
    result = await query_menu_items(sql)
    result = format_table(result)
    smile = random.choice(['☺️', '😉', '🙂'])
    args["text"] = f"Тримай Друже {smile}\n\n" f"```{result}```"
    args["parse_mode"] = ParseMode.MARKDOWN_V2

    return args


async def get_random_item(data, args):
    print("data", data)
    print("args", args)
    sql = build_menu_item_query(data) + " ORDER BY RANDOM() LIMIT 1"
    result = await query_menu_items(sql)
    item = result[0]
    text = [
        [f'Друже, спробуй \n<b>{item["name"]}</b> | {item["price"]} грн'],
        [],
        [f'\n{item["description"]} \n<b>{item["volume"]}</b> '],
    ]
    alt_price = json.loads(item["alt_prices"])
    if alt_price:
        prices = [f"{k}: {v} грн" for k, v in alt_price.items()]
        text.insert(1, f' | {" | ".join(prices)}')
    args["text"] = "".join("".join(ele) for ele in text)
    args["parse_mode"] = ParseMode.HTML

    return args


async def random_button_inline(update, context, active_item):
    keyboard = [
        [
            InlineKeyboardButton(
                ROLL_BUTTON + " Натисни мене " + ROLL_BUTTON,
                callback_data=json.dumps({"method": "random"}),
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        update.message.chat.id,
        text="Не знаєш, що хочеш?\nДавай може я щось запропоную?",
        reply_markup=reply_markup)
    return active_item


async def get_active_item(update: Update, context: CallbackContext, user: UserModel):
    session_context = context.user_data.get("session_context") or []
    menu_definition = await get_menu_definition(user)
    active_item = menu_definition
    for index in session_context:
        active_item = active_item["children"][index]

    message_text = update.message.text

    if message_text == HOME_BUTTON:
        context.user_data["session_context"] = []
        active_item = menu_definition

        return active_item

    elif message_text == BACK_TEXT and len(session_context):
        session_context = session_context[:-1]
        context.user_data["session_context"] = session_context
        new_item = menu_definition
        for index in session_context:
            new_item = new_item["children"][index]
        return new_item
    elif (message_text == ROLL_BUTTON or update.message.dice) and len(session_context):
        return get_random_menu_item_btn()
    elif message_text == HELP_BUTTON:
        return await help_command(update, context)
    else:
        for key, button in active_item["children"].items():
            if message_text == button["title"]:
                session_context.append(key)
                context.user_data["session_context"] = session_context
                return button
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=MISUNDERSTOOD_TEXT
        )

        if active_item == get_random_menu_item_btn():
            context.user_data["session_context"] = []
            return menu_definition

        return active_item


async def unverified_users(args, update: Update, context: CallbackContext):
    users = await get_verified_user(False)

    keyboard = []
    for row in users:
        keyboard.append(
            [
                InlineKeyboardButton(
                    row.User.nickname,
                    callback_data=json.dumps(
                        {
                            "method": "verify",
                            "id": row.User.id,
                        }
                    ),
                )
            ]
        )

    reply_markup = InlineKeyboardMarkup(keyboard, resize_keyboard=True)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Unverified users:",
        reply_markup=reply_markup,
    )
    args["text"] = "Please select user to verify"

    return args


async def social_network_buttons(args):
    keyboard = [
        [
            InlineKeyboardButton(
                "INSTAGRAM",
                url="https://instagram.com/muscat_coffeeshop?igshid=YmMyMTA2M2Y=",
            )
        ],
        [
            InlineKeyboardButton(
                "TELEGRAM", url="https://t.me/muscat_coffee_people_chat"
            )
        ],
    ]
    args['animation'] = SOCIAL_NETWORK_GIF
    args['reply_markup'] = InlineKeyboardMarkup(keyboard)

    return args


async def get_samos_response(user_id):
    booking = await get_booking_for_user(user_id)

    text = []
    for key, val in booking.items():
        if val.qty > 0:
            text.append(
                f'{PRODUCTS[val.product_type]["plural_name"]}: <b>{val.qty}</b>'
            )

    if len(text):
        text = "\n".join(text)
    else:
        text = "Забронювати самоси:"

    keyboard = []
    for key, val in PRODUCTS.items():
        keyboard.append(
            [
                InlineKeyboardButton(
                    f'+1 {val["single_name"]}',
                    callback_data=json.dumps(
                        {
                            "method": "order",
                            "action": "+",
                            "type": key,
                        }
                    ),
                )
            ]
        )
    keyboard_index = 0
    for key, val in PRODUCTS.items():
        if key in booking and booking[key].qty:
            keyboard[keyboard_index].insert(
                0,
                InlineKeyboardButton(
                    f'-1 {val["single_name"]}',
                    callback_data=json.dumps(
                        {
                            "method": "order",
                            "action": "-",
                            "type": key,
                        }
                    ),
                ),
            )
        keyboard_index += 1

    reply_markup = InlineKeyboardMarkup(keyboard)
    return {
        "reply_markup": reply_markup,
        "text": text,
    }


async def order_samos(args, update: Update, context: CallbackContext):
    r = await get_samos_response(update.effective_user.id)

    context.user_data["session_context"] = []
    args["text"] = r["text"]
    args["reply_markup"] = r["reply_markup"]
    args["parse_mode"] = ParseMode.HTML

    return args


async def reply(update: Update, context: CallbackContext, active_item):
    session_context = context.user_data.get("session_context") or []
    buttons = []
    if "children" in active_item:
        row_values = []
        for k, val in active_item["children"].items():
            if "row" in val:
                row_values.append(val["row"])
        for i in range(max(row_values) + 1):
            buttons.append([])
        for item in active_item["children"].values():
            if "row" in item:
                buttons[item["row"]].append(KeyboardButton(item["title"]))
            else:
                buttons.append(KeyboardButton(item["title"]))
    if len(session_context) > 0:
        additional_buttons = [KeyboardButton(BACK_TEXT)]
        if len(session_context) > 1:
            additional_buttons.append(KeyboardButton(HOME_BUTTON))
        if "show_help" in active_item:
            additional_buttons.append(KeyboardButton(HELP_BUTTON))
        buttons.append(additional_buttons)

    args = {
        "chat_id": update.effective_chat.id,
        "text": active_item.get("reply") or random.choice(DEFAULT_TEXTS),
    }

    if "callback" in active_item:
        if active_item["callback"] == "get_menu_items":
            args = await get_menu_items(active_item.get("callback_data"), args)
        elif active_item["callback"] == "get_random_item":
            args = await get_random_item(active_item.get("callback_data"), args)
        elif active_item["callback"] == "unverified_users":
            args = await unverified_users(args, update, context)
        elif active_item["callback"] == "order_samos":
            args = await order_samos(args, update, context)
        elif active_item["callback"] == "social_networks":
            args = await social_network_buttons(args)

    if "reply_markup" not in args:
        args["reply_markup"] = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    if "animation" in args:
        del args['text']
        context.user_data["session_context"] = []
        return await context.bot.sendAnimation(**args)
    return await context.bot.send_message(**args)


async def handler(update: Update, context: CallbackContext):
    user = await get_user(update)

    active_item = await get_active_item(update=update, context=context, user=user)
    try:
        if active_item["reply"] == HOME_REPLY_WITH_RANDOM:
            await random_button_inline(update, context, active_item)
    except KeyError:
        pass

    if active_item:
        await reply(update=update, context=context, active_item=active_item)


async def start(update: Update, context: CallbackContext):
    context.user_data["session_context"] = []

    user = await get_user(update)
    menu_definition = await get_menu_definition(user)
    active_item = menu_definition
    active_item['reply'] = random.choice(WELCOME_TEXT)

    await reply(update, context, menu_definition)


async def help_command(update: Update, context: CallbackContext):
    context.user_data["session_context"] = context.user_data.get("session_context")
    await update.message.reply_text(HELP_TEXT, parse_mode=ParseMode.HTML)


async def random_command(update: Update, context: CallbackContext):
    await reply(update, context, active_item=get_random_menu_item_btn())


async def keyboard_callback(update, context):
    query = update.callback_query

    payload: dict = json.loads(query.data)
    if payload:
        method = payload.get("method")
        if method:
            if method == "verify":
                user_id = payload.get("id")
                await verify_user(user_id)
                await query.answer(f"Verified")
            elif method == "order":
                product_type = payload.get("type")
                user_id = update.effective_user.id
                action = payload.get("action")
                await booking(product_type, user_id, action, update)
            elif method == "random":
                context.user_data['session_context'] = ['random']
                await reply(update, context, get_random_menu_item_btn())


async def booking(product_type, user_id, action, update):
    query = update.callback_query

    await update_booking_qty(user_id, product_type, action)

    r = await get_samos_response(update.effective_user.id)
    await query.edit_message_text(
        text=r["text"], reply_markup=r["reply_markup"], parse_mode=ParseMode.HTML
    )


def main():
    logging.info("Starting...")
    application = ApplicationBuilder().token(config.TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("random", random_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler((filters.TEXT | filters.Dice.DICE) & (~filters.COMMAND), handler)
    )

    application.add_handler(CallbackQueryHandler(keyboard_callback))

    application.run_polling()


if __name__ == "__main__":
    main()
