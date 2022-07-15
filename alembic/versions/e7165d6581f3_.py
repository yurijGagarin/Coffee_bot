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
        sa.Column('name', sa.String, nullable=False),
        sa.Column('price', sa.DECIMAL, nullable=False),
        sa.Column('is_coffee', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_milk', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_lact_free_milk', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_vegan_milk', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_tea', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_matcha', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_season', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_black_coffee', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_fresh', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_other', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_deserts', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('description', sa.Text, nullable=False, server_default=' '),
        sa.Column('volume', sa.String, nullable=False, server_default=' '),
        sa.Column('available', sa.Boolean, nullable=False, server_default='0'),

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
         'is_lact_free_milk': True, 'is_milk': True,
         'description':
             "Кавово-молочний напій на основі еспресо,"
             " з ідеальним балансом кави та молока.",
         'volume': '180 мл'},
        {'name': 'Капучино [Р]', 'price': 60, 'is_coffee': True,
         'is_vegan_milk': True, 'is_milk': True,
         'description':
             "Кавово-молочний напій на основі еспресо,"
             " з ідеальним балансом кави та молока.",
         'volume': '180 мл'},
        {'name': 'Лате', 'price': 45, 'is_coffee': True, 'is_milk': True,
         'description':
             "Кавово-молочний напій на основі еспресо,"
             " з балансом зміщенним в сторону молока.",
         'volume': '300 мл'},
        {'name': 'Айс Лате', 'price': 45, 'is_coffee': True, 'is_milk': True, 'is_season': True,
         'description':
             "Класичний напій у холодному виконанні. Смак улюбленої кави у поєднанні з ніжним смаком молока.",
         'volume': '330 мл'},
        {'name': 'Айс Беррі Лате', 'price': 55, 'is_coffee': True, 'is_milk': True, 'is_season': True,
         'description':
             "Айс Лате з додаванням ягідного пюре.",
         'volume': '330 мл'},
        {'name': 'Айс Беррі Лате [Б/Л]', 'price': 65, 'is_coffee': True,
         'is_lact_free_milk': True, 'is_milk': True, 'is_season': True,
         'description':
             "Айс Лате з додаванням ягідного пюре.",
         'volume': '330 мл'},
        {'name': 'Айс Беррі Лате [Р]', 'price': 75, 'is_coffee': True,
         'is_vegan_milk': True, 'is_milk': True, 'is_season': True,
         'description':
             "Айс Лате з додаванням ягідного пюре.",
         'volume': '330 мл'},
        {'name': 'Лате [Б/Л]', 'price': 55, 'is_coffee': True,
         'is_lact_free_milk': True, 'is_milk': True,
         'description':
             "Кавово-молочний напій на основі еспресо,"
             " з балансом зміщенним в сторону молока.",
         'volume': '300 мл'},
        {'name': 'Айс Лате [Б/Л]', 'price': 55, 'is_coffee': True,
         'is_lact_free_milk': True, 'is_milk': True, 'is_season': True,
         'description':
             "Класичний напій у холодному виконанні. Смак улюбленої кави у поєднанні з ніжним смаком молока.",
         'volume': '330 мл'},
        {'name': 'Лате [Р]', 'price': 65, 'is_coffee': True,
         'is_vegan_milk': True, 'is_milk': True,
         'description':
             "Кавово-молочний напій на основі еспресо,"
             " з балансом зміщенним в сторону молока.",
         'volume': '300 мл'},
        {'name': 'Айс Лате [Р]', 'price': 65, 'is_coffee': True,
         'is_vegan_milk': True, 'is_milk': True, 'is_season': True,
         'description':
             "Класичний напій у холодному виконанні. Смак улюбленої кави у поєднанні з ніжним смаком молока.",
         'volume': '330 мл'},
        {'name': 'Флет Уайт', 'price': 45, 'is_coffee': True, 'is_milk': True,
         'description':
             "Кавово-молочний напій на основі подвійного еспресо,"
             " з балансом зміщенним в сторону кави.",
         'volume': '180 мл'},
        {'name': 'Флет Уайт [Б/Л]', 'price': 55, 'is_coffee': True,
         'is_lact_free_milk': True, 'is_milk': True,
         'description':
             "Кавово-молочний напій на основі подвійного еспресо,"
             " з балансом зміщенним в сторону кави.",
         'volume': '180 мл'},
        {'name': 'Флет Уайт [Р]', 'price': 65, 'is_coffee': True,
         'is_vegan_milk': True, 'is_milk': True,
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
         'is_lact_free_milk': True, 'is_milk': True,
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
             "Гарячий кавово-вершковий напій з нотами ванілі. Вершковий та солодкий смак.",
         'volume': '330 мл'},
        {'name': 'Айс Раф', 'price': 65, 'is_coffee': True, 'is_milk': True, 'is_season': True,
         'description':
             "Холодний кавово-вершковий напій з нотами ванілі. Вершковий та солодкий смак. "
             "Більш текстурний ніж його гаряча версія.",
         'volume': '330 мл'},
        {'name': 'Раф [Б/Л]', 'price': 75, 'is_coffee': True,
         'is_lact_free_milk': True, 'is_milk': True,
         'description':
             "Гарячий кавово-вершковий напій з нотами ванілі. Вершковий та солодкий смак.",
         'volume': '330 мл'},
        {'name': 'Айс Раф [Б/Л]', 'price': 75, 'is_coffee': True,
         'is_season': True, 'is_lact_free_milk': True, 'is_milk': True,
         'description':
             "Холодний кавово-вершковий напій з нотами ванілі. Вершковий та солодкий смак. "
             "Більш текстурний ніж його гаряча версія.",
         'volume': '330 мл'},
        {'name': 'Раф [Р]', 'price': 85, 'is_coffee': True,
         'is_vegan_milk': True, 'is_milk': True,
         'description':
             "Гарячий кавово-вершковий напій з нотами ванілі. Вершковий та солодкий смак.",
         'volume': '330 мл'},
        {'name': 'Айс Раф [Р]', 'price': 85, 'is_coffee': True,
         'is_season': True, 'is_vegan_milk': True, 'is_milk': True,
         'description':
             "Холодний кавово-вершковий напій з нотами ванілі. Вершковий та солодкий смак. "
             "Більш текстурний ніж його гаряча версія.",
         'volume': '330 мл'},
        {'name': 'Капуоранж', 'price': 70, 'is_coffee': True, 'is_fresh': True,
         'description':
             "Це як капучино, в якому замість молока - свіжовичавлений апельсиновий фреш.",
         'volume': '180 мл'},
        {'name': 'Бамбл', 'price': 70, 'is_coffee': True, 'is_fresh': True, 'is_season': True,
         'description':
             "Кава, апельсиновий фреш та лід. Допомагає побороти спеку",
         'volume': '330 мл'},

        {'name': 'Какао', 'price': 55, 'is_other': True, 'is_milk': True,
         'description':
             "В нас є як гіркий так і солодкий.  Обирай що тобі до смаку.",
         'volume': '330 мл'},
        {'name': 'Айс Какао', 'price': 55, 'is_other': True, 'is_milk': True, 'is_season': True,
         'description':
             "Холодний Какао. В нас є як гіркий так і солодкий.  Обирай що тобі до смаку.",
         'volume': '330 мл'},
        {'name': 'Какао [Б/Л]', 'price': 65, 'is_other': True, 'is_lact_free_milk': True, 'is_milk': True,
         'description':
             "В нас є як гіркий так і солодкий.  Обирай що тобі до смаку.",
         'volume': '330 мл'},
        {'name': 'Айс Какао [Б/Л]', 'price': 65, 'is_other': True,
         'is_lact_free_milk': True, 'is_milk': True, 'is_season': True,
         'description':
             "Холодний Какао. В нас є як гіркий так і солодкий.  Обирай що тобі до смаку.",
         'volume': '330 мл'},
        {'name': 'Какао [Р]', 'price': 75, 'is_other': True, 'is_vegan_milk': True, 'is_milk': True,
         'description':
             "В нас є як гіркий так і солодкий.  Обирай що тобі до смаку.",
         'volume': '330 мл'},
        {'name': 'Айс Какао [Р]', 'price': 75, 'is_other': True, 'is_vegan_milk': True, 'is_milk': True,
         'is_season': True,
         'description':
             "Холодний Какао. В нас є як гіркий так і солодкий.  Обирай що тобі до смаку.",
         'volume': '330 мл'},

        {'name': 'Колд Брю', 'price': 60, 'is_coffee': True, 'is_season': True,
         'is_black_coffee': True,
         'description':
             "Чорна кава, яка готується методом імерсії протягом 20 годин",
         'volume': '330 мл'},
        {'name': 'Колд Брю Колада', 'price': 75, 'is_coffee': True, 'is_vegan_milk': True, 'is_milk': True,
         'is_season': True,
         'description':
             "Якщо колд брю - то занудно для тебе, то спробуй це."
             " В основі колд брю та два вида рослинного молока",
         'volume': '330 мл'},
        {'name': 'Колд Брю Тонік', 'price': 60, 'is_coffee': True, "is_black_coffee": True,
         'is_season': True,
         'description':
             "Колд брю та тонік, класика сьогодення, що допомагає побороти спеку.",
         'volume': '330 мл'},
        {'name': 'Еспресо Тонік', 'price': 60, 'is_coffee': True, "is_black_coffee": True,
         'is_season': True,
         'description':
             "Еспресо та тонік, класика сьогодення, що допомагає побороти спеку.",
         'volume': '330 мл'},

        {'name': 'Габа Алішань Улун', 'price': 50, 'is_tea': True,
         'description':
             "Представник темних улунів. З особливості цього чаю є те,"
             " що він містить дуже велику кількість гамма-аміномасляної кислоти."
             " Діє на нервову систему м'яко, одночасно розслабляючи і стимулюючи її."
             " Це один з небагатьох чаїв, який у смаку має кислотність.",
         'volume': '400 мл'},
        {'name': 'Гречаний', 'price': 50, 'is_tea': True,
         'description':
             "Чай. Насіння татарскої  або тайванської гречки. Має яскраві ноти імбирного печива та цукрової вати.",
         'volume': '400 мл'},
        {'name': 'Червоний', 'price': 50, 'is_tea': True,
         'description':
             "Чай. Різновид Чжень Шань Сяо Чжун. Чай обсмажуєтьсяв бамбуковій чаші. "
             "У смаку містить яскраво виражені деревинні ноти, з медовим післясмаком.",
         'volume': '400 мл'},
        {'name': 'Фруктовий', 'price': 50, 'is_tea': True,
         'description':
             "Чай. Пелюстки китайської суданської троянди, шматочки малини, апельсина і яблук,"
             " китайський фінік, листя стевії, пелюстки троянди та півонії.",
         'volume': '400 мл'},
        {'name': 'Білий', 'price': 50, 'is_tea': True,
         'description':
             "Чай. Витриманий білий чай з повіту Фудін провінції Фуцзянь."
             " Фудін – це невеликий повіт на півночі провінції Фуцзянь, "
             "який спеціалізується саме на виготовлені білого чаю."
             " В букеті готового чаю приємний сухофруктовий мікс, мед, сливове варення, шоколад, "
             "горіхи, відтінки осені та банного віника. Смак солодкий, насичений, з приємною кислинкою в післясмаку.",
         'volume': '400 мл'},
        {'name': 'Да Хун Пао', 'price': 50, 'is_tea': True,
         'description':
             "Да Хун Пао - це чай-легенда, найвідоміший улун з культового чайного регіону Уїшань."
             "Як і в інших добре прогрітих уїшанських улунах в ньому поєднується карамельна солодкість"
             " і шоколадна терпкість, солодка випічка та димність.",
         'volume': '400 мл'},
        {'name': 'Молочний Улун', 'price': 50, 'is_tea': True,
         'description':
             "Наш молочний улун виготовляють в Китаї, провінції Фуцзянь, там,"
             " де і більшість улунів, в околицях містечка Аньсі."
             " За основу беруть Те Гуань Інь та ароматизують чай натуральним екстрактом ще на стадії виробництва,"
             " без жодної хімії. В ароматі чаю можна вгадати квіткові та молочні ноти,"
             " а також ноти солодкої молочної карамельки та попкорну.",
         'volume': '400 мл'},
        {'name': 'Зелений з Жасміном', 'price': 50, 'is_tea': True,
         'description':
             "Жасминовий чай преміальної якості, раннього весняного збору з провінції Гуансі,"
             " яка славиться своїми жасминовими садами."
             " Майстер змішує сировину із запашними квітами жасмину і залишає чай просочитися їх ароматом."
             " Смак солодкий, мʼякий, без терпких та гірких нот.",
         'volume': '400 мл'},
        {'name': 'Ройбуш', 'price': 50, 'is_tea': True,
         'description':
             "Смачний і ароматний. Не містить кофеїн. Має цілющі та тонізуючі властивості. "
             "Готовий чай має насичений, солодкуватий смак і унікальний горіхово-деревний аромат. "
             "Він бадьорить і освіжає. Ройбос добре втамовує спрагу і тонізує.",
         'volume': '400 мл'},
        {'name': 'Травяний', 'price': 50, 'is_tea': True,
         'description':
             "Купаж на основі високогірного карпатського іван-чаю подвійної ферментації з додаванням квітів,"
             " трав та цедри апельсину.",
         'volume': '400 мл'},
        {'name': 'Шу Пуер', 'price': 70, 'is_tea': True,
         'description':
             "Чай. Провінція Юньнань, 2015 рік. Тонізує, бадьорить, налаштовує на роботу та м'яко концентрує.",
         'volume': '400 мл'},
        {'name': 'Шень Пуер', 'price': 70, 'is_tea': True,
         'description':
             "Чай. Аромат яскравий, солодкий. В букеті готового чаю квітково-травʼянистий профіль,"
             " з відтінками зеленого яблука та солодкого персика. Смак солодкий, освіжаючий, з приємною терпкістю."
             " Післясмак довгий, з солодкістю льодяників.",
         'volume': '400 мл'},

        {'name': 'Матча Шот', 'price': 60, "is_matcha": True,
         'description':
             "Матча, взбита до шовкової текстури з невеликою кількістю води."
             " Найкращий варіант, якщо бажаешь спробувати чисту матчу",
         'volume': '80 мл'},
        {'name': 'Матча Оранж', 'price': 80, "is_matcha": True, "is_fresh": True,
         'description':
             "Гарячий напій який поєднує в собі матчу та апельсиновий фреш. "
             "Яскравий та насичений смак, а також дуже корисний.",
         'volume': '180 мл'},
        {'name': 'Айс Матча Оранж', 'price': 80, "is_matcha": True, "is_fresh": True, "is_season": True,
         'description':
             "Холодний напій який поєднує в собі матчу та апельсиновий фреш. "
             "Яскравий та насичений смак, а також дуже корисний.",
         'volume': '330 мл'},
        {'name': 'Матча Тонік', 'price': 75, "is_matcha": True, "is_season": True,
         'description':
             "Холодний напій який поєднує в собі матчу та тонік. Допомагає побороти спеку.",
         'volume': '270 мл'},
        {'name': 'Матча Лате', 'price': 60, "is_matcha": True, "is_milk": True,
         'description':
             "Напій основою якого є матча,"
             " з правильним вмішуванням в нього взбитого молока",
         'volume': '260 мл'},
        {'name': 'Айс Матча Лате', 'price': 60, "is_matcha": True, 'is_season': True, "is_milk": True,
         'description':
             "Матча, молоко та лід. Гарно смакує у спеку",
         'volume': '270 мл'},
        {'name': 'Айс Беррі Матча Лате', 'price': 70, "is_matcha": True, 'is_season': True, "is_milk": True,
         'description':
             "Матча, молоко, лід та ягідне пюре. Гарно смакує у спеку",
         'volume': '270 мл'},
        {'name': 'Айс Беррі Матча [Б/Л]', 'price': 80, "is_matcha": True, 'is_season': True,
         'is_lact_free_milk': True, 'is_milk': True,
         'description':
             "Матча, молоко, лід та ягідне пюре. Гарно смакує у спеку",
         'volume': '270 мл'},
        {'name': 'Айс Беррі Матча [Р]', 'price': 90, "is_matcha": True, 'is_season': True,
         'is_vegan_milk': True, 'is_milk': True,
         'description':
             "Матча, молоко, лід та ягідне пюре. Гарно смакує у спеку",
         'volume': '270 мл'},
        {'name': 'Матча Лате [Б/Л]', 'price': 70, "is_matcha": True, 'is_lact_free_milk': True, 'is_milk': True,
         'description':
             "Напій основою якого є матча,"
             " з правильним вмішуванням в нього взбитого молока",
         'volume': '260 мл'},
        {'name': 'Айс Матча Лате [Б/Л]', 'price': 70, "is_matcha": True, 'is_season': True,
         'is_lact_free_milk': True, 'is_milk': True,
         'description':
             "Матча, молоко та лід. Гарно смакує у спеку",
         'volume': '270 мл'},
        {'name': 'Матча Лате [Р]', 'price': 80, "is_matcha": True, 'is_vegan_milk': True, 'is_milk': True,
         'description':
             "Напій основою якого є матча,"
             " з правильним вмішуванням в нього взбитого молока",
         'volume': '260 мл'},
        {'name': 'Айс Матча Лате [Р]', 'price': 80, "is_matcha": True, 'is_season': True,
         'is_vegan_milk': True, 'is_milk': True,
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
        if 'available' not in i:
            i['available'] = True
        op.bulk_insert(table, [i])


def downgrade() -> None:
    op.drop_table('menu_item')
