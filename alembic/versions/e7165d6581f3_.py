"""empty message

Revision ID: e7165d6581f3
Revises: 
Create Date: 2022-06-09 14:03:40.916846

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e7165d6581f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    table = op.create_table(
        'menu_item',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('price', sa.DECIMAL, nullable=False),
        sa.Column('is_coffee', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_milk', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_lact_free_milk', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_vegan_milk', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_tea', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_matcha', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_cold', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_black_coffee', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_fresh', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_other', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_deserts', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('description', sa.Text, nullable=False, server_default=' '),
        sa.Column('volume', sa.String(50), nullable=False, server_default=' '),

    )

    menu_items = [
        {'name': 'Еспресо', 'price': 35, 'is_coffee': True, 'is_black_coffee': True,
         'description':
             "Концентрована чорна кава, яка готується під великим тиском в еспресо машині.",
         'volume': '25 мл'},
        {'name': 'Подвійний еспресо', 'price': 35, 'is_coffee': True, 'is_black_coffee': True,
         'description':
             "Концентрована чорна кава, яка готується під великим тиском в еспресо машині.",
         'volume': '50 мл'},
        {'name': 'Фільтр Кава', 'price': 40, 'is_coffee': True, 'is_black_coffee': True,
         'description':
             "Різновид чорної кави, яка готується в крапельній кавоварці."
             " Легкий, питкий напій.",
         'volume': '250 мл'},

        {'name': 'Клевер', 'price': 65, 'is_coffee': True, 'is_black_coffee': True,
         'description':
             "Різновид фільтр кави, який готується методом імерсїї, у девайсі під назвою 'Clever'."
             " Є можливість обрати каву на свій смак.",
         'volume': '290 мл'
         },

        {'name': 'Октошторм', 'price': 65, 'is_coffee': True, 'is_black_coffee': True,
         'description':
             "Різновид фільтр кави, який готується методом пуровер, у девайсі під назвою 'Octostorm'."
             " Є можливість обрати каву на свій смак.",
         'volume': '290 мл'},
        {'name': 'V-60', 'price': 65, 'is_coffee': True, 'is_black_coffee': True,
         'description':
             "Різновид фільтр кави, який готується методом пуровер, у девайсі під назвою 'V-60'."
             " Є можливість обрати каву на свій смак.",
         'volume': '290 мл'},
        {'name': 'Свіч', 'price': 65, 'is_coffee': True, 'is_black_coffee': True,
         'description':
             "Різновид фільтр кави, який готується методом імерсїї, у девайсі під назвою 'Switch'."
             " Є можливість обрати каву на свій смак.",
         'volume': '240 мл'},
        {'name': 'Аеропресс', 'price': 65, 'is_coffee': True, 'is_black_coffee': True,
         'description':
             "Різновид фільтр кави, який готується методом імерсїї, у девайсі під назвою 'Aeropress'."
             " Є можливість обрати каву на свій смак.",
         'volume': '230 мл'},
        {'name': 'Дельтер', 'price': 65, 'is_coffee': True, 'is_black_coffee': True,
         'description':
             "Різновид фільтр кави, який готується методом пуровер, у девайсі під назвою 'Delter'."
             " Є можливість обрати каву на свій смак.",
         'volume': '220 мл'},

        {'name': 'Капучино', 'price': 40, 'is_coffee': True, 'is_milk': True,
         'description':
             "Кавово-молочний напій на основі еспресо,"
             " з ідеальним балансом кави та молока.",
         'volume': '180 мл'},
        {'name': 'Капучино [Б/Л]', 'price': 50, 'is_coffee': True,
         'is_lact_free_milk': True,
         'description':
             "Кавово-молочний напій на основі еспресо,"
             " з ідеальним балансом кави та молока.",
         'volume': '180 мл'},
        {'name': 'Капучино [Р]', 'price': 60, 'is_coffee': True,
         'is_vegan_milk': True,
         'description':
             "Кавово-молочний напій на основі еспресо,"
             " з ідеальним балансом кави та молока.",
         'volume': '180 мл'},
        {'name': 'Лате', 'price': 45, 'is_coffee': True, 'is_milk': True,
         'description':
             "Кавово-молочний напій на основі еспресо,"
             " з балансом зміщенним в сторону молока.",
         'volume': '300 мл'},
        {'name': 'Айс Лате', 'price': 45, 'is_coffee': True, 'is_milk': True, 'is_cold': True,
         'description':
             "Класичний напій у холодному виконанні. Смак улюбленої кави у поєднанні з ніжним смаком молока.",
         'volume': '330 мл'},
        {'name': 'Айс Беррі Лате', 'price': 55, 'is_coffee': True, 'is_milk': True, 'is_cold': True,
         'description':
             "Айс Лате з додаванням ягідного пюре.",
         'volume': '330 мл'},
        {'name': 'Айс Беррі Лате [Б/Л]', 'price': 65, 'is_coffee': True,
         'is_lact_free_milk': True, 'is_cold': True,
         'description':
             "Айс Лате з додаванням ягідного пюре.",
         'volume': '330 мл'},
        {'name': 'Айс Беррі Лате [Р]', 'price': 75, 'is_coffee': True,
         'is_vegan_milk': True, 'is_cold': True,
         'description':
             "Айс Лате з додаванням ягідного пюре.",
         'volume': '330 мл'},
        {'name': 'Лате [Б/Л]', 'price': 55, 'is_coffee': True,
         'is_lact_free_milk': True,
         'description':
             "Кавово-молочний напій на основі еспресо,"
             " з балансом зміщенним в сторону молока.",
         'volume': '300 мл'},
        {'name': 'Айс Лате [Б/Л]', 'price': 55, 'is_coffee': True,
         'is_lact_free_milk': True, 'is_cold': True,
         'description':
             "Класичний напій у холодному виконанні. Смак улюбленої кави у поєднанні з ніжним смаком молока.",
         'volume': '330 мл'},
        {'name': 'Лате [Р]', 'price': 65, 'is_coffee': True,
         'is_vegan_milk': True,
         'description':
             "Кавово-молочний напій на основі еспресо,"
             " з балансом зміщенним в сторону молока.",
         'volume': '300 мл'},
        {'name': 'Айс Лате [Р]', 'price': 65, 'is_coffee': True,
         'is_vegan_milk': True, 'is_cold': True,
         'description':
             "Класичний напій у холодному виконанні. Смак улюбленої кави у поєднанні з ніжним смаком молока.",
         'volume': '330 мл'},
        {'name': 'Флет Уайт', 'price': 45, 'is_coffee': True, 'is_milk': True,
         'description':
             "Кавово-молочний напій на основі подвійного еспресо,"
             " з балансом зміщенним в сторону кави.",
         'volume': '180 мл'},
        {'name': 'Флет Уайт [Б/Л]', 'price': 55, 'is_coffee': True,
         'is_lact_free_milk': True,
         'description':
             "Кавово-молочний напій на основі подвійного еспресо,"
             " з балансом зміщенним в сторону кави.",
         'volume': '180 мл'},
        {'name': 'Флет Уайт [Р]', 'price': 65, 'is_coffee': True,
         'is_vegan_milk': True,
         'description':
             "Кавово-молочний напій на основі подвійного еспресо,"
             " з балансом зміщенним в сторону кави.",
         'volume': '180 мл'},
        {'name': 'Подвійний Капучино', 'price': 50, 'is_coffee': True, 'is_tea': False, 'is_milk': True,
         'description':
             "Кавово-молочний напій на основі подвійного еспресо,"
             " зі збереженним балансом кави та молока та більшим об'ємом ніж класичний капучино.",
         'volume': '300 мл'},
        {'name': 'Подвійний Капучино [Б/Л]', 'price': 60, 'is_coffee': True,
         'is_lact_free_milk': True,
         'description':
             "Кавово-молочний напій на основі подвійного еспресо,"
             " зі збереженним балансом кави та молока та більшим об'ємом ніж класичний капучино.",
         'volume': '300 мл'},
        {'name': 'Подвійний Капучино [Р]', 'price': 70, 'is_coffee': True, 'is_milk': True,
         'is_vegan_milk': True,
         'description':
             "Кавово-молочний напій на основі подвійного еспресо,"
             " зі збереженним балансом кави та молока та більшим об'ємом ніж класичний капучино.",
         'volume': '300 мл'},
        {'name': 'Раф', 'price': 65, 'is_coffee': True, 'is_milk': True,
         'description':
             "Гарячий кавово-вершковий напій з додаванням ванільного цукру. Вершковий та солодкий смак.",
         'volume': '330 мл'},
        {'name': 'Айс Раф', 'price': 65, 'is_coffee': True, 'is_milk': True, 'is_cold': True,
         'description':
             "Твій улюблений раф, який ще допоможе побороти спеку",
         'volume': '330 мл'},
        {'name': 'Раф [Б/Л]', 'price': 75, 'is_coffee': True,
         'is_lact_free_milk': True,
         'description':
             "Гарячий кавово-вершковий напій з додаванням ванільного цукру. Вершковий та солодкий смак.",
         'volume': '330 мл'},
        {'name': 'Айс Раф [Б/Л]', 'price': 75, 'is_coffee': True,
         'is_cold': True, 'is_lact_free_milk': True,
         'description':
             "Твій улюблений раф, який ще допоможе побороти спеку",
         'volume': '330 мл'},
        {'name': 'Раф [Р]', 'price': 85, 'is_coffee': True,
         'is_vegan_milk': True,
         'description':
             "Гарячий кавово-вершковий напій з додаванням ванільного цукру. Вершковий та солодкий смак.",
         'volume': '330 мл'},
        {'name': 'Айс Раф [Р]', 'price': 85, 'is_coffee': True,
         'is_cold': True, 'is_vegan_milk': True,
         'description':
             "Твій улюблений раф, який ще допоможе побороти спеку",
         'volume': '330 мл'},
        {'name': 'Капуоранж', 'price': 70, 'is_coffee': True, 'is_fresh': True,
         'description':
             "Це як капучино, в якому замість молока-свіжовичавлений апельсиновий фреш",
         'volume': '180 мл'},
        {'name': 'Бамбл', 'price': 70, 'is_coffee': True, 'is_fresh': True, 'is_cold': True,
         'description':
             "Кава, апельсиновий фреш  та лід. Допомагає побороти спеку",
         'volume': '330 мл'},

        {'name': 'Какао', 'price': 55, 'is_other': True, 'is_milk': True,
         'description':
             "В нас є як гіркий так і солодкий.  Обирай що тобі до смаку.",
         'volume': '330 мл'},
        {'name': 'Айс Какао', 'price': 55, 'is_other': True, 'is_milk': True, 'is_cold': True,
         'description':
             "Холодний Какао",
         'volume': '330 мл'},
        {'name': 'Какао [Б/Л]', 'price': 65, 'is_other': True, 'is_lact_free_milk': True,
         'description':
             "В нас є як гіркий так і солодкий.  Обирай що тобі до смаку.",
         'volume': '330 мл'},
        {'name': 'Айс Какао [Б/Л]', 'price': 65, 'is_other': True,
         'is_lact_free_milk': True, 'is_cold': True,
         'description':
             "Холодний Какао",
         'volume': '330 мл'},
        {'name': 'Какао [Р]', 'price': 75, 'is_other': True, 'is_vegan_milk': True,
         'description':
             "В нас є як гіркий так і солодкий.  Обирай що тобі до смаку.",
         'volume': '330 мл'},
        {'name': 'Айс Какао [Р]', 'price': 75, 'is_other': True, 'is_vegan_milk': True,
         'is_cold': True,
         'description':
             "Холодний Какао",
         'volume': '330 мл'},

        {'name': 'Колд Брю', 'price': 60, 'is_coffee': True, 'is_cold': True,
         'is_black_coffee': True,
         'description':
             "Чорна кава, яка готується методом імерсії протягом 20 годин",
         'volume': '330 мл'},
        {'name': 'Колд Брю Колада', 'price': 75, 'is_coffee': True, 'is_vegan_milk': True,
         'is_cold': True,
         'description':
             "Якщо колд брю то занудно для тебе, то спробуй це."
             " В основі колд брю та два вида рослинного молока",
         'volume': '330 мл'},
        {'name': 'Колд Брю Тонік', 'price': 60, 'is_coffee': True, "is_black_coffee": True,
         'is_cold': True,
         'description':
             "Колд брю та тонік, класика сьогодення, що допомагає побороти спеку.",
         'volume': '330 мл'},
        {'name': 'Еспресо Тонік', 'price': 60, 'is_coffee': True, "is_black_coffee": True,
         'is_cold': True,
         'description':
             "Еспресо та тонік, класика сьогодення, що допомагає побороти спеку.",
         'volume': '330 мл'},

        {'name': 'Габа Улун', 'price': 50, 'is_tea': True,
         'description':
             "Чай. Різновиду темний улун."
             " Заварюємо в спеціальному 'Ті-поті', щоб б ти мав можливість насолодитися чаєм",
         'volume': '300 мл'},
        {'name': 'Гречаний', 'price': 50, 'is_tea': True,
         'description':
             "Чай. # Максим, не забудь додати опис до чаю"
             " Заварюємо в спеціальному 'Ті-поті', щоб б ти мав можливість насолодитися чаєм",
         'volume': '300 мл'},
        {'name': 'Червоний', 'price': 50, 'is_tea': True,
         'description':
             "Чай. # Максим, не забудь додати опис до чаю"
             " Заварюємо в спеціальному 'Ті-поті', щоб б ти мав можливість насолодитися чаєм",
         'volume': '300 мл'},
        {'name': 'Фруктовий', 'price': 50, 'is_tea': True,
         'description':
             "Чай. # Максим, не забудь додати опис до чаю"
             " Заварюємо в спеціальному 'Ті-поті', щоб б ти мав можливість насолодитися чаєм",
         'volume': '300 мл'},
        {'name': 'Білий', 'price': 50, 'is_tea': True,
         'description':
             "Чай. # Максим, не забудь додати опис до чаю"
             " Заварюємо в спеціальному 'Ті-поті', щоб б ти мав можливість насолодитися чаєм",
         'volume': '300 мл'},
        {'name': 'Да Хун Пао', 'price': 50, 'is_tea': True,
         'description':
             "Чай. # Максим, не забудь додати опис до чаю"
             " Заварюємо в спеціальному 'Ті-поті', щоб б ти мав можливість насолодитися чаєм",
         'volume': '300 мл'},
        {'name': 'Молочний Улун', 'price': 50, 'is_tea': True,
         'description':
             "Чай. # Максим, не забудь додати опис до чаю"
             " Заварюємо в спеціальному 'Ті-поті', щоб б ти мав можливість насолодитися чаєм",
         'volume': '300 мл'},
        {'name': 'Зелений з Жасміном', 'price': 50, 'is_tea': True,
         'description':
             "Чай. # Максим, не забудь додати опис до чаю"
             " Заварюємо в спеціальному 'Ті-поті', щоб б ти мав можливість насолодитися чаєм",
         'volume': '300 мл'},
        {'name': 'Ройбуш', 'price': 50, 'is_tea': True,
         'description':
             "Чай. # Максим, не забудь додати опис до чаю"
             " Заварюємо в спеціальному 'Ті-поті', щоб б ти мав можливість насолодитися чаєм",
         'volume': '300 мл'},
        {'name': 'Травяний', 'price': 50, 'is_tea': True,
         'description':
             "Чай. # Максим, не забудь додати опис до чаю"
             " Заварюємо в спеціальному 'Ті-поті', щоб б ти мав можливість насолодитися чаєм",
         'volume': '300 мл'},
        {'name': 'Шу Пуер', 'price': 70, 'is_tea': True,
         'description':
             "Чай. # Максим, не забудь додати опис до чаю"
             " Заварюємо в спеціальному 'Ті-поті', щоб б ти мав можливість насолодитися чаєм",
         'volume': '300 мл'},
        {'name': 'Шень Пуер', 'price': 70, 'is_tea': True,
         'description':
             "Чай. # Максим, не забудь додати опис до чаю"
             " Заварюємо в спеціальному 'Ті-поті', щоб б ти мав можливість насолодитися чаєм",
         'volume': '300 мл'},

        {'name': 'Матча Шот', 'price': 60, "is_matcha": True,
         'description':
             "Матча, взбита до шовкової текстури з невеликою кількістю води."
             " Найкращий варіант, якщо бажаешь спробувати нейкед матчу",
         'volume': '80 мл'},
        {'name': 'Матча Оранж', 'price': 80, "is_matcha": True, "is_fresh": True,
         'description':
             "Матча та взбитий апельсиновий фреш",
         'volume': '180 мл'},
        {'name': 'Айс Матча Оранж', 'price': 80, "is_matcha": True, "is_fresh": True, "is_cold": True,
         'description':
             "Матча, апельсиновий фреш та лід. Допомагає побороти спеку.",
         'volume': '270 мл'},
        {'name': 'Матча Тонік', 'price': 75, "is_matcha": True, "is_cold": True,
         'description':
             "Матча з тоніком. Допомагає побороти спеку.",
         'volume': '270 мл'},
        {'name': 'Матча Лате', 'price': 60, "is_matcha": True, "is_milk": True,
         'description':
             "Напій основою якого є матча,"
             " з правильним вмішуванням в нього взбитого молока",
         'volume': '260 мл'},
        {'name': 'Айс Матча Лате', 'price': 60, "is_matcha": True, 'is_cold': True, "is_milk": True,
         'description':
             "Матча, молоко та лід. Гарно смакує у спеку",
         'volume': '270 мл'},
        {'name': 'Айс Беррі Матча Лате', 'price': 70, "is_matcha": True, 'is_cold': True, "is_milk": True,
         'description':
             "Матча, молоко, лід та ягідне пюре. Гарно смакує у спеку",
         'volume': '270 мл'},
        {'name': 'Айс Беррі Матча [Б/Л]', 'price': 80, "is_matcha": True, 'is_cold': True,
         'is_lact_free_milk': True,
         'description':
             "Матча, молоко, лід та ягідне пюре. Гарно смакує у спеку",
         'volume': '270 мл'},
        {'name': 'Айс Беррі Матча [Р]', 'price': 90, "is_matcha": True, 'is_cold': True,
         'is_vegan_milk': True,
         'description':
             "Матча, молоко, лід та ягідне пюре. Гарно смакує у спеку",
         'volume': '270 мл'},
        {'name': 'Матча Лате [Б/Л]', 'price': 70, "is_matcha": True, 'is_lact_free_milk': True,
         'description':
             "Напій основою якого є матча,"
             " з правильним вмішуванням в нього взбитого молока",
         'volume': '260 мл'},
        {'name': 'Айс Матча Лате [Б/Л]', 'price': 70, "is_matcha": True, 'is_cold': True,
         'is_lact_free_milk': True,
         'description':
             "Матча, молоко та лід. Гарно смакує у спеку",
         'volume': '270 мл'},
        {'name': 'Матча Лате [Р]', 'price': 80, "is_matcha": True, 'is_vegan_milk': True,
         'description':
             "Напій основою якого є матча,"
             " з правильним вмішуванням в нього взбитого молока",
         'volume': '260 мл'},
        {'name': 'Айс Матча Лате [Р]', 'price': 80, "is_matcha": True, 'is_cold': True,
         'is_vegan_milk': True,
         'description':
             "Матча, молоко та лід. Гарно смакує у спеку",
         'volume': '270 мл'},

        {'name': 'Ванільний Еклер', 'price': 30, 'is_deserts': True},
        {'name': 'Шоколадний Еклер', 'price': 30, 'is_deserts': True},
        {'name': 'Фісташка-Малина Еклер', 'price': 40, 'is_deserts': True},
        {'name': 'Чізкейк', 'price': 65, 'is_deserts': True},
        {'name': 'Тірамісу', 'price': 60, 'is_deserts': True},

    ]
    for i in menu_items:
        op.bulk_insert(table, [i])


def downgrade() -> None:
    op.drop_table('menu_item')
