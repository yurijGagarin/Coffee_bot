import random
from copy import deepcopy
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from bot import config
from models import User as UserModel

ROLL_BUTTON = '🎲'
HOME_BUTTON = '🏠'
HELP_BUTTON = 'Допомога'
BACK_TEXT = 'Назад'
CHOOSE_BUTTONS = ['Оберіть:', '⬇️', '⤵️', '➡️', '🔽']
MISUNDERSTOOD_TEXT = "Вибачте, не зрозумів вас"
DEFAULT_TEXTS = ['🙂', '😊', '🙃']
HELP_TEXT = '''Вітаємо, це словничок скорочень Мускат Бота.
<b>[Б/Л]</b> --> Замість звичайного молока використовується безлактозне.
<b>[Р]</b> --> Замість звичайного молока використовується рослинне.
<b>Іммерсія</b> --> Спосіб заварювання, шляхом постійного контакту води з тим, що ти заварюєш.
'''
RANDOM_MENU_ITEM = {
    "title": "Що мені випити?",
    "show_help": True,
    "callback_data": {
        "skip_defaults": True,
        "is_deserts": False
    },
    "callback": "get_random_item",
    "children": {
        "roll": {
            "title": ROLL_BUTTON,
        },
    }
}

MENU_DEFINITION = {
    "reply": "👋 Вітаємо в діджиталізованому Мускаті 🙂",
    "children": {
        "menu": {
            "title": "Меню",
            "reply": "Оберіть розділ",
            "children": {
                "drinks": {
                    "title": "Напої",
                    "reply": random.choice(CHOOSE_BUTTONS),
                    "children": {
                        "coffee": {
                            "title": "Кава",
                            "reply": random.choice(CHOOSE_BUTTONS),
                            "children": {
                                "cold": {
                                    "title": "Холодна",
                                    "reply": random.choice(CHOOSE_BUTTONS),
                                    "children": {
                                        "no_milk": {
                                            "title": "Без молока",
                                            "reply": random.choice(CHOOSE_BUTTONS),
                                            "show_help": True,
                                            "callback_data": {
                                                "is_coffee": True,
                                                "is_black_coffee": True,
                                                "is_cold": True

                                            },
                                            "callback": "get_menu_items",
                                        },
                                        "milk": {
                                            "title": "З молоком",
                                            "reply": random.choice(CHOOSE_BUTTONS),
                                            "children": {
                                                "cow_milk": {
                                                    "title": "Звичайне",
                                                    "reply": random.choice(CHOOSE_BUTTONS),
                                                    "show_help": True,
                                                    "callback_data": {
                                                        "is_coffee": True,
                                                        "is_milk": True,
                                                        "is_cold": True

                                                    },
                                                    "callback": "get_menu_items",
                                                },
                                                "lactose_free_milk": {
                                                    "title": "Безлактозне",
                                                    "reply": random.choice(CHOOSE_BUTTONS),
                                                    "show_help": True,
                                                    "callback_data": {
                                                        "is_coffee": True,
                                                        "is_lact_free_milk": True,
                                                        "is_cold": True

                                                    },
                                                    "callback": "get_menu_items",
                                                },
                                                "vegan_milk": {
                                                    "title": "Рослинне",
                                                    "reply": random.choice(CHOOSE_BUTTONS),
                                                    "show_help": True,
                                                    "callback_data": {
                                                        "is_coffee": True,
                                                        "is_vegan_milk": True,
                                                        "is_cold": True

                                                    },
                                                    "callback": "get_menu_items",
                                                }, }

                                        },
                                        "juice": {
                                            "title": "На фреші",
                                            "reply": random.choice(CHOOSE_BUTTONS),
                                            "show_help": True,
                                            "callback_data": {
                                                "is_coffee": True,
                                                "is_fresh": True,
                                                "is_cold": True
                                            },
                                            "callback": "get_menu_items",

                                        }, }

                                },
                                "hot": {
                                    "title": "Гаряча",
                                    "reply": random.choice(CHOOSE_BUTTONS),
                                    "children": {
                                        "no_milk": {
                                            "title": "Чорна кава",
                                            "reply": random.choice(CHOOSE_BUTTONS),
                                            "show_help": True,
                                            "callback_data": {
                                                "is_coffee": True,
                                                "is_black_coffee": True,

                                            },
                                            "callback": "get_menu_items",
                                        },
                                        "milk": {
                                            "title": "З молоком",
                                            "reply": random.choice(CHOOSE_BUTTONS),
                                            "children": {
                                                "cow_milk": {
                                                    "title": "Звичайне",
                                                    "reply": random.choice(CHOOSE_BUTTONS),
                                                    "show_help": True,
                                                    "callback_data": {
                                                        "is_coffee": True,
                                                        "is_milk": True,

                                                    },
                                                    "callback": "get_menu_items",
                                                },
                                                "lactose_free_milk": {
                                                    "title": "Безлактозне",
                                                    "reply": random.choice(CHOOSE_BUTTONS),
                                                    "show_help": True,
                                                    "callback_data": {
                                                        "is_coffee": True,
                                                        "is_lact_free_milk": True,

                                                    },
                                                    "callback": "get_menu_items",
                                                },
                                                "vegan_milk": {
                                                    "title": "Рослинне",
                                                    "reply": random.choice(CHOOSE_BUTTONS),
                                                    "show_help": True,
                                                    "callback_data": {
                                                        "is_coffee": True,
                                                        "is_vegan_milk": True,

                                                    },
                                                    "callback": "get_menu_items",
                                                }, }
                                        },
                                        "juice": {
                                            "title": "На фреші",
                                            "reply": random.choice(CHOOSE_BUTTONS),
                                            "show_help": True,
                                            "callback_data": {
                                                "is_coffee": True,
                                                "is_fresh": True,
                                            },
                                            "callback": "get_menu_items",

                                        }, }
                                },
                            },

                        },
                        "matcha": {
                            "title": "Матча",
                            "reply": random.choice(CHOOSE_BUTTONS),
                            "children": {
                                "cold": {
                                    "title": "Холодна",
                                    "reply": random.choice(CHOOSE_BUTTONS),
                                    "show_help": True,
                                    "callback_data": {
                                        "is_matcha": True,
                                        "is_cold": True,
                                        "skip_defaults": True
                                    },
                                    "callback": "get_menu_items",
                                },
                                "hot": {
                                    "title": "Гаряча",
                                    "reply": random.choice(CHOOSE_BUTTONS),
                                    "show_help": True,
                                    "callback_data": {
                                        "is_matcha": True,
                                        "is_cold": False,
                                        "skip_defaults": True
                                    },
                                    "callback": "get_menu_items",
                                },
                            },
                        },
                        "tea": {
                            "title": "Чай",
                            "reply": random.choice(CHOOSE_BUTTONS),
                            "show_help": True,
                            "callback_data": {
                                "is_tea": True,

                            },
                            "callback": "get_menu_items",
                        },
                        "other": {
                            "title": "Інше",
                            "reply": random.choice(CHOOSE_BUTTONS),
                            "show_help": True,
                            "callback_data": {
                                "is_other": True,
                                "skip_defaults": True
                            },
                            "callback": "get_menu_items",

                        },
                    }
                },
                "deserts": {
                    "title": "Десерти",
                    "reply": "Тут ви зможете ознайомитись з тим, які десерти в нас бувають. ",
                    "callback_data": {
                        "is_deserts": True,
                        "skip_defaults": True
                    },
                    "callback": "get_menu_items",
                },

            },
        },
        "random": RANDOM_MENU_ITEM
    }
}


def get_current_date():
    today = date.today()
    samosy_day = date(2022, 6, 25)
    available_days = [0, 1, 2, 3, 6]
    samosy_when = samosy_day - today
    next_saturday = timedelta(7)
    can_order = False
    unload_bd = False
    if samosy_when < timedelta(1):
        samosy_day += next_saturday
    if today.weekday() in available_days:
        can_order = True
    if today.weekday == 4:
        unload_bd = True
    return samosy_day, can_order, unload_bd


async def get_menu_definition(user: UserModel):
    menu = deepcopy(MENU_DEFINITION)

    if user.is_verified:
        # menu['children']['menu']['children']['drinks']['children'] = {"secret": {
        #     "title": "Speak easy 😏",
        #     "reply": "😏",
        # }}

        menu['children']['order_samos'] = {
            "title": "Бронювання самосів",
            "reply": random.choice(CHOOSE_BUTTONS),
            "children": {
                "order": {
                    "title": "Забронювати самоси",
                    "reply": "Яка кількість?",
                    "callback": 'quantity',
                }}
        }

        if user.salty > 0 or user.sweet > 0:
            menu['children']['order_samos']['children']['booking_info'] = {
                "title": "Мої заброньовані самоси",
                "reply": "Ти забронював:",
                "callback": 'booking_info',
            }

    if user.is_admin:
        menu['children']['user_verification'] = {
            "title": "Верифікувати юзера",
            "reply": " Оберіть юзернейм",
            "callback": 'unverified_users',

        }
        # if not can_order:
        #     del menu['buttons'][2]

    return menu
