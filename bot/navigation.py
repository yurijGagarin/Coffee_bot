import random
from copy import deepcopy
from datetime import date, timedelta

from models import User as UserModel

ROLL_BUTTON = "🎲"
HOME_BUTTON = "🏠"
HOME_REPLY = ["Давай спробуємо знову 😁",
              "Не знаєш що хочеш? Давай може я щось запропоною? 🎲",
              "А ти вже дивився наше сезоне меню?🤔",
              "Може по еклерчику? 🤤"]
HELP_BUTTON = "Допомога"
BACK_TEXT = "Назад"
CHOOSE_BUTTONS = ["Оберіть розділ:", "⬇️", "⤵️", "➡️", "🔽"]
WELCOME_TEXT = ["👋 Вітаємо в діджиталізованому Мускаті 🙂",
                "👋 Раді тебе бачити!",
                "👋 Привіт! Давай підберемо тобі щось смачненьке 🤗"]
MISUNDERSTOOD_TEXT = "Вибачте, не зрозумів вас"
DEFAULT_TEXTS = ["🙂", "😊", "🙃"]
HELP_TEXT = """Вітаємо, це словничок скорочень Мускат Бота.
<b>[Б/Л]</b> --> Замість звичайного молока використовується безлактозне.
<b>[Р]</b> --> Замість звичайного молока використовується рослинне.
<b>Іммерсія</b> --> Спосіб заварювання, шляхом постійного контакту води з тим, що ти заварюєш.
"""
RANDOM_MENU_ITEM = {
    "title": "🎲 Що мені випити?",
    "show_help": True,
    "row": 1,
    "callback_data": {"skip_defaults": True, "is_deserts": False, "available": True},
    "callback": "get_random_item",
    "children": {
        "roll": {
            "row": 1,
            "title": ROLL_BUTTON,
        },
    },
}
DRINKS = {
    "title": "🥤 Напої",
    "row": 0,
    "reply": random.choice(CHOOSE_BUTTONS),
    "children": {
        "black_coffee": {
            "title": "♨ Чорна кава",
            "row": 0,
            "reply": random.choice(CHOOSE_BUTTONS),
            "show_help": True,
            "callback_data": {
                "is_coffee": True,
                "is_black_coffee": True,
            },
            "callback": "get_menu_items",
        },
        "coffee_with_milk": {
            "title": "🥛 Кава з молоком",
            "row": 0,
            "reply": random.choice(CHOOSE_BUTTONS),
            "show_help": True,
            "callback_data": {
                "is_coffee": True,
                "is_season": False,
                "is_milk": True,
                "skip_defaults": True,
                "available": True,
            },
            "callback": "get_menu_items",
        },
        "coffee_with_juice": {
            "title": "🍹 На фреші",
            "row": 0,
            "reply": random.choice(CHOOSE_BUTTONS),
            "show_help": True,
            "callback_data": {
                "is_coffee": True,
                "is_fresh": True,
            },
            "callback": "get_menu_items",
        },
        "matcha": {
            "title": "🍵 Матча",
            "row": 2,
            "reply": random.choice(CHOOSE_BUTTONS),
            "show_help": True,
            "callback_data": {
                "is_matcha": True,
                "is_season": False,
                "skip_defaults": True,
                "available": True,
            },
            "callback": "get_menu_items",
        },
        "tea": {
            "title": "🫖 Чай",
            "row": 2,
            "reply": random.choice(CHOOSE_BUTTONS),
            "show_help": True,
            "callback_data": {
                "is_tea": True,
            },
            "callback": "get_menu_items",
        },
        "other": {
            "title": "☕ Какао",
            "row": 2,
            "reply": random.choice(CHOOSE_BUTTONS),
            "show_help": True,
            "callback_data": {
                "is_other": True,
                "skip_defaults": True,
                "available": True,
            },
            "callback": "get_menu_items",
        },
    },
}
DESERTS = {
    "title": "🧁 Десерти",
    "row": 1,
    "reply": random.choice(CHOOSE_BUTTONS),
    "callback_data": {"is_deserts": True, "skip_defaults": True, "available": True},
    "callback": "get_menu_items",
}
SEASON = {
    "title": "🍹 Сезонне меню",
    "row": 0,
    "reply": random.choice(CHOOSE_BUTTONS),
    "children": {
        "coffee": {
            "title": "♨ На каві",
            "row": 0,
            "reply": random.choice(CHOOSE_BUTTONS),
            "show_help": True,
            "callback_data": {
                "is_coffee": True,
                "skip_defaults": True,
                "is_season": True,
                "available": True,
            },
            "callback": "get_menu_items",
        },
        "matcha": {
            "title": "🍵 На матчі",
            "row": 0,
            "reply": random.choice(CHOOSE_BUTTONS),
            "show_help": True,
            "callback_data": {
                "is_matcha": True,
                "skip_defaults": True,
                "is_season": True,
                "available": True,
            },
            "callback": "get_menu_items",
        },
        "other": {
            "title": "🧋 Інше",
            "reply": random.choice(CHOOSE_BUTTONS),
            "show_help": True,
            "row": 0,
            "callback_data": {
                "is_other": True,
                "skip_defaults": True,
                "is_season": True,
                "available": True,
            },
            "callback": "get_menu_items",
        },
    },
}

MENU_DEFINITION = {
    "reply": random.choice(WELCOME_TEXT),
    "children": {
        "drinks": DRINKS,
        "deserts": DESERTS,
        "season": SEASON,
        "random": RANDOM_MENU_ITEM,
    },
}


def get_next_saturday():
    d = date.today()
    t = timedelta((7 + 5 - d.weekday()) % 7)
    return d + t


def samos_button_reveal():
    today = date.today()
    available_days = [0, 1, 2, 3, 6]
    can_order = False
    if today.weekday() in available_days:
        can_order = True
    return can_order


async def get_menu_definition(user: UserModel):
    menu = deepcopy(MENU_DEFINITION)

    if user.is_verified:
        # menu['children']['menu']['children']['drinks']['children'] = {"secret": {
        #     "title": "Speak easy 😏",
        #     "reply": "😏",
        # }}

        menu["children"]["order_samos"] = {
            "title": "Бронювання самосів",
            "row": 2,
            "reply": random.choice(CHOOSE_BUTTONS),
            "callback": "order_samos",
        }

    if user.is_admin:
        menu["children"]["user_verification"] = {
            "title": "Верифікувати юзера",
            "row": 2,
            "reply": " Оберіть юзернейм",
            "callback": "unverified_users",
        }
        # if not can_order:
        #     del menu['buttons'][2]

    return menu
