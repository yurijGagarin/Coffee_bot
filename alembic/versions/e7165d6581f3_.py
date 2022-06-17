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

    )

    menu_items = [
        {'name': 'Еспресо', 'price': 35, 'is_coffee': True, 'is_black_coffee': True},
        {'name': 'Фільтр Кава', 'price': 40, 'is_coffee': True, 'is_black_coffee': True},
        {'name': 'Клевер', 'price': 65, 'is_coffee': True, 'is_black_coffee': True},
        {'name': 'Октошторм', 'price': 65, 'is_coffee': True, 'is_black_coffee': True},
        {'name': 'Свіч', 'price': 65, 'is_coffee': True, 'is_black_coffee': True},
        {'name': 'Аеропресс', 'price': 65, 'is_coffee': True, 'is_black_coffee': True},
        {'name': 'Дельтер', 'price': 65, 'is_coffee': True, 'is_black_coffee': True},

        {'name': 'Капучино', 'price': 40, 'is_coffee': True, 'is_milk': True},
        {'name': 'Капучино 🐮🚫', 'price': 50, 'is_coffee': True,
         'is_lact_free_milk': True},
        {'name': 'Капучино 🌿', 'price': 60, 'is_coffee': True,
         'is_vegan_milk': True},
        {'name': 'Лате', 'price': 45, 'is_coffee': True, 'is_milk': True},
        {'name': 'Айс Лате', 'price': 45, 'is_coffee': True, 'is_milk': True, 'is_cold': True},
        {'name': 'Айс Беррі Лате', 'price': 55, 'is_coffee': True, 'is_milk': True, 'is_cold': True},
        {'name': 'Айс Беррі Лате 🐮🚫', 'price': 65, 'is_coffee': True,
         'is_lact_free_milk': True, 'is_cold': True},
        {'name': 'Айс Беррі Лате 🌿', 'price': 75, 'is_coffee': True,
         'is_vegan_milk': True, 'is_cold': True},
        {'name': 'Лате 🐮🚫', 'price': 55, 'is_coffee': True,
         'is_lact_free_milk': True},
        {'name': 'Айс Лате 🐮🚫', 'price': 55, 'is_coffee': True,
         'is_lact_free_milk': True, 'is_cold': True},
        {'name': 'Лате 🌿', 'price': 65, 'is_coffee': True,
         'is_vegan_milk': True},
        {'name': 'Айс Лате 🌿', 'price': 65, 'is_coffee': True,
         'is_vegan_milk': True, 'is_cold': True},
        {'name': 'Флет Уайт', 'price': 45, 'is_coffee': True, 'is_milk': True},
        {'name': 'Флет Уайт 🐮🚫', 'price': 55, 'is_coffee': True,
         'is_lact_free_milk': True},
        {'name': 'Флет Уайт 🌿', 'price': 65, 'is_coffee': True,
         'is_vegan_milk': True},
        {'name': 'Подвійний Капучино', 'price': 50, 'is_coffee': True, 'is_tea': False, 'is_milk': True},
        {'name': 'Подвійний Капучино 🐮🚫', 'price': 60, 'is_coffee': True,
         'is_lact_free_milk': True},
        {'name': 'Подвійний Капучино 🌿', 'price': 70, 'is_coffee': True, 'is_milk': True,
         'is_vegan_milk': True},
        {'name': 'Раф', 'price': 65, 'is_coffee': True, 'is_milk': True},
        {'name': 'Айс Раф', 'price': 65, 'is_coffee': True, 'is_milk': True, 'is_cold': True},
        {'name': 'Раф 🐮🚫', 'price': 75, 'is_coffee': True,
         'is_lact_free_milk': True},
        {'name': 'АЙс Раф 🐮🚫', 'price': 75, 'is_coffee': True,
         'is_cold': True, 'is_lact_free_milk': True},
        {'name': 'Раф 🌿', 'price': 85, 'is_coffee': True,
         'is_vegan_milk': True},
        {'name': 'Айс Раф 🌿', 'price': 85, 'is_coffee': True,
         'is_cold': True, 'is_vegan_milk': True},
        {'name': 'Капуоранж', 'price': 70, 'is_coffee': True, 'is_fresh': True},
        {'name': 'Бамбл', 'price': 70, 'is_coffee': True, 'is_fresh': True, 'is_cold': True},

        {'name': 'Какао', 'price': 55, 'is_other': True, 'is_milk': True},
        {'name': 'АЙс Какао', 'price': 55, 'is_other': True, 'is_milk': True, 'is_cold': True},
        {'name': 'Какао 🐮🚫', 'price': 65, 'is_other': True, 'is_lact_free_milk': True},
        {'name': 'Айс Какао 🐮🚫', 'price': 65, 'is_other': True,
         'is_lact_free_milk': True, 'is_cold': True},
        {'name': 'Какао 🌿', 'price': 75, 'is_other': True, 'is_vegan_milk': True},
        {'name': 'Айс Какао 🌿', 'price': 75, 'is_other': True, 'is_vegan_milk': True,
         'is_cold': True},

        {'name': 'Колд Брю', 'price': 60, 'is_coffee': True, 'is_cold': True,
         'is_black_coffee': True},
        {'name': 'Колд Брю Колада', 'price': 75, 'is_coffee': True, 'is_lact_free_milk': True,
         'is_cold': True},
        {'name': 'Колд Брю Тонік', 'price': 60, 'is_coffee': True, "is_black_coffee": True,
         'is_cold': True},
        {'name': 'Еспресо Тонік', 'price': 60, 'is_coffee': True, "is_black_coffee": True,
         'is_cold': True},

        {'name': 'Габа Улун', 'price': 50, 'is_tea': True},
        {'name': 'Гречаний', 'price': 50, 'is_tea': True},
        {'name': 'Червоний', 'price': 50, 'is_tea': True},
        {'name': 'Фруктовий', 'price': 50, 'is_tea': True},
        {'name': 'Білий', 'price': 50, 'is_tea': True},
        {'name': 'Да Хун Пао', 'price': 50, 'is_tea': True},
        {'name': 'Молочний Улун', 'price': 50, 'is_tea': True},
        {'name': 'Зелений з Жасміном', 'price': 50, 'is_tea': True},
        {'name': 'Ройбуш', 'price': 50, 'is_tea': True},
        {'name': 'Травяний', 'price': 50, 'is_tea': True},
        {'name': 'Шу Пуер', 'price': 70, 'is_tea': True},
        {'name': 'Шень Пуер', 'price': 70, 'is_tea': True},

        {'name': 'Маття Шот', 'price': 60, "is_matcha": True},
        {'name': 'Маття Оранж', 'price': 80, "is_matcha": True, "is_fresh": True},
        {'name': 'Айс Маття Оранж', 'price': 80, "is_matcha": True, "is_fresh": True, "is_cold": True},
        {'name': 'Маття Тонік', 'price': 75, "is_matcha": True, "is_cold": True},
        {'name': 'Маття Лате', 'price': 60, "is_matcha": True, "is_milk": True},
        {'name': 'Айс Маття Лате', 'price': 60, "is_matcha": True, 'is_cold': True, "is_milk": True},
        {'name': 'Айс Беррі Маття Лате', 'price': 70, "is_matcha": True, 'is_cold': True, "is_milk": True},
        {'name': 'Айс Беррі Маття 🐮🚫', 'price': 80, "is_matcha": True, 'is_cold': True,
         'is_lact_free_milk': True},
        {'name': 'Айс Беррі Маття 🌿', 'price': 90, "is_matcha": True, 'is_cold': True,
         'is_vegan_milk': True},
        {'name': 'Маття Лате 🐮🚫', 'price': 70, "is_matcha": True, 'is_lact_free_milk': True},
        {'name': 'Айс Маття Лате 🐮🚫', 'price': 70, "is_matcha": True, 'is_cold': True,
         'is_lact_free_milk': True},
        {'name': 'Маття Лате 🌿', 'price': 80, "is_matcha": True, 'is_vegan_milk': True},
        {'name': 'Айс Маття Лате 🌿', 'price': 80, "is_matcha": True, 'is_cold': True,
         'is_vegan_milk': True},

        {'name': 'Ванільний Еклер', 'price': 30, 'is_deserts': True},
        {'name': 'Шоколадний Еклер', 'price': 30, 'is_deserts': True},
        {'name': 'Фісташка-Малина Еклер', 'price': 40, 'is_deserts': True},
        {'name': 'Чізкейк', 'price': 75, 'is_deserts': True},
        {'name': 'Тірамісу', 'price': 60, 'is_deserts': True},

    ]
    for i in menu_items:
        op.bulk_insert(table, [i])


def downgrade() -> None:
    op.drop_table('menu_item')
