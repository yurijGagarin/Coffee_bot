import random
from copy import deepcopy
from datetime import date, timedelta

from models import User as UserModel

ROLL_BUTTON = "🎲"
HOME_BUTTON = "🏠"
HOME_REPLY_WITH_RANDOM = "Сподіваюсь тобі сподобається ☺️"
HOME_REPLY = [
    HOME_REPLY_WITH_RANDOM,
    "Давай спробуємо знову 😁",
    "А ти вже дивився наше сезоне меню?🤔",
    "Може по еклерчику? 🤤",
]
HELP_BUTTON = "Допомога"
BACK_TEXT = "Назад"
CHOOSE_BUTTONS = ["Оберіть розділ:", "⬇️", "⤵️", "➡️", "🔽"]
WELCOME_TEXT = ["👋 Вітаємо в діджиталізованому Мускаті 🙂",
                "👋 Раді тебе бачити!",
                "👋 Давай підберемо тобі щось смачненьке 🤗"]
MISUNDERSTOOD_TEXT = "Вибачте, не зрозумів вас"
DEFAULT_TEXTS = ["🙂", "😊", "🙃"]
HELP_TEXT = """Вітаємо, це словничок скорочень Мускат Бота.
<b>[Б/Л]</b> --> Замість звичайного молока використовується безлактозне.
<b>[Р]</b> --> Замість звичайного молока використовується рослинне.
<b>Іммерсія</b> --> Спосіб заварювання, шляхом постійного контакту води з тим, що ти заварюєш.
"""


def get_random_menu_item_btn():
    return {
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


def get_social_networks():
    return {
        "title": "Ми в соціальних мережах",
        "row": 2,
        "callback": "social_networks",
    }


def get_drinks():
    return {
        "title": "🥤 Напої",
        "row": 0,
        "reply": random.choice(CHOOSE_BUTTONS),
        "children": {
            "black_coffee": {
                "title": "☕ Чорна кава",
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
                "title": "♨ Какао",
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


def get_deserts():
    return {
        "title": "🧁 Десерти",
        "row": 1,
        "reply": "Тут ви зможете ознайомитись з тим, які десерти в нас бувають. ",
        "callback_data": {"is_deserts": True, "skip_defaults": True, "available": True},
        "callback": "get_menu_items",
    }


def get_season_menu():
    return {
        "title": "🍹 Сезоне меню",
        "row": 0,
        "children": {
            "coffee": {
                "title": "☕ На каві",
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


def get_main_menu_definition():
    return {
        "reply": random.choice(HOME_REPLY),
        "children": {
            "social_networks": get_social_networks(),
            "drinks": get_drinks(),
            "deserts": get_deserts(),
            "season": get_season_menu(),
            "random": get_random_menu_item_btn(),
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
    menu = deepcopy(get_main_menu_definition())

    def samos_order_btn():
        return {
            "title": "Бронювання самосів",
            "row": 2,
            "reply": random.choice(CHOOSE_BUTTONS),
            "callback": "order_samos",
        }

    def verification_user_btn():
        return {
            "title": "Верифікувати юзера",
            "row": 2,
            "reply": " Оберіть юзернейм",
            "callback": "unverified_users",
        }

    if user.is_verified and samos_button_reveal():
        # menu['children']['menu']['children']['drinks']['children'] = {"secret": {
        #     "title": "Speak easy 😏",
        #     "reply": "😏",
        # }}

        menu["children"]["order_samos"] = samos_order_btn()

    if user.is_admin:
        menu["children"]["user_verification"] = verification_user_btn()
        # if not can_order:
        #     del menu['buttons'][2]

    return menu
