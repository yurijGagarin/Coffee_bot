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
        sa.Column('parent_id', sa.Integer),
        sa.Column('is_coffee', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_milk', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_lact_free', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_tea', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_matcha', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_cold', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_black_coffee', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_fresh', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_other', sa.Boolean, nullable=False, server_default='0'),

    )

    menu_items = [
        {'name': 'Espresso', 'price': 35, 'is_coffee': True, 'is_black_coffee': True},
        {'name': 'Filter', 'price': 40, 'is_coffee': True, 'is_black_coffee': True},
        {'name': 'Clever', 'price': 65, 'is_coffee': True, 'is_black_coffee': True},
        {'name': 'Octostorm', 'price': 65, 'is_coffee': True, 'is_black_coffee': True},
        {'name': 'Switch', 'price': 65, 'is_coffee': True, 'is_black_coffee': True},
        {'name': 'Aeropress', 'price': 65, 'is_coffee': True, 'is_black_coffee': True},
        {'name': 'Delter', 'price': 65, 'is_coffee': True, 'is_black_coffee': True},

        {'name': 'Cappuccino', 'price': 40, 'is_coffee': True, 'is_milk': True},
        {'name': 'Cappuccino Lactose Free', 'price': 50, 'parent_id': 6, 'is_coffee': True, 'is_milk': True,
         'is_lact_free': True},
        {'name': 'Cappuccino Alternative', 'price': 60, 'parent_id': 6, 'is_coffee': True, 'is_milk': True,
         'is_lact_free': True},
        {'name': 'Caffe Latte', 'price': 45, 'is_coffee': True, 'is_milk': True},
        {'name': 'Caffe Latte Cold', 'price': 45, 'is_coffee': True, 'is_milk': True, 'is_cold': True},
        {'name': 'Ice Berry Latte', 'price': 55, 'is_coffee': True, 'is_milk': True, 'is_cold': True},
        {'name': 'Ice Berry Latte Lactose Free', 'price': 65, 'is_coffee': True,
         'is_milk': True, 'is_lact_free': True, 'is_cold': True},
        {'name': 'Ice Berry Latte Alternative', 'price': 75, 'is_coffee': True,
         'is_milk': True, 'is_lact_free': True, 'is_cold': True},
        {'name': 'Caffe Latte Lactose Free', 'parent_id': 9, 'price': 55, 'is_coffee': True, 'is_milk': True,
         'is_lact_free': True},
        {'name': 'Caffe Latte Lactose Free Cold', 'parent_id': 9, 'price': 55, 'is_coffee': True, 'is_milk': True,
         'is_lact_free': True, 'is_cold': True},
        {'name': 'Caffe Latte Alternative', 'parent_id': 9, 'price': 65, 'is_coffee': True, 'is_milk': True,
         'is_lact_free': True},
        {'name': 'Caffe Latte Alternative Cold', 'parent_id': 9, 'price': 65, 'is_coffee': True,'is_milk': True,
         'is_lact_free': True, 'is_cold': True},
        {'name': 'Flat White', 'price': 45, 'is_coffee': True, 'is_milk': True},
        {'name': 'Flat White Lactose Free', 'parent_id': 12, 'price': 55, 'is_coffee': True, 'is_milk': True,
         'is_lact_free': True},
        {'name': 'Flat White Alternative', 'parent_id': 12, 'price': 65, 'is_coffee': True, 'is_milk': True,
         'is_lact_free': True},
        {'name': 'Double Cappuccino', 'price': 50, 'is_coffee': True, 'is_tea': False, 'is_milk': True},
        {'name': 'Double Cappuccino Lactose Free', 'parent_id': 15, 'price': 60, 'is_coffee': True, 'is_milk': True,
         'is_lact_free': True},
        {'name': 'Double Cappuccino Alternative', 'parent_id': 15, 'price': 70, 'is_coffee': True, 'is_milk': True,
         'is_lact_free': True},
        {'name': 'Raf', 'price': 65, 'is_coffee': True, 'is_milk': True},
        {'name': 'Raf Cold', 'price': 65, 'parent_id': 18, 'is_coffee': True, 'is_milk': True, 'is_cold': True},
        {'name': 'Raf Lactose Free', 'price': 75, 'parent_id': 18, 'is_coffee': True, 'is_milk': True,
         'is_lact_free': True},
        {'name': 'Raf Lactose Free Cold', 'price': 75, 'parent_id': 18, 'is_coffee': True, 'is_milk': True,
         'is_cold': True, 'is_lact_free': True},
        {'name': 'Raf Alternative', 'price': 85, 'parent_id': 18, 'is_coffee': True, 'is_milk': True,
         'is_lact_free': True},
        {'name': 'Raf Alternative Cold', 'price': 85, 'parent_id': 18, 'is_coffee': True, 'is_milk': True,
         'is_cold': True, 'is_lact_free': True},
        {'name': 'Capuorange', 'price': 70, 'is_coffee': True,  'is_fresh': True},
        {'name': 'Capuorange Cold', 'price': 70, 'is_coffee': True,  'is_fresh': True, 'is_cold': True},



        {'name': 'Cocoa', 'price': 55, 'is_other': True, 'is_milk': True},
        {'name': 'Cocoa Cold', 'price': 55, 'is_other': True, 'is_milk': True, 'is_cold': True},
        {'name': 'Cocoa Lactose Free', 'price': 65, 'is_other': True, 'parent_id': 34, 'is_lact_free': True, 'is_milk': True},
        {'name': 'Cocoa Lactose Free Cold', 'price': 65, 'is_other': True, 'parent_id': 34, 'is_lact_free': True,
         'is_milk': True, 'is_cold': True},
        {'name': 'Cocoa Alternative', 'price': 75, 'parent_id': 34, 'is_other': True, 'is_milk': True, 'is_lact_free': True},
        {'name': 'Cocoa Alternative Cold', 'price': 75, 'parent_id': 34, 'is_other': True, 'is_milk': True, 'is_lact_free': True,
         'is_cold': True},


        {'name': 'Cold Brew', 'price': 60, 'is_coffee': True, 'is_cold': True,
         'is_black_coffee': True},
        {'name': 'Cold Brew Colada', 'price': 75, 'is_coffee': True, 'is_lact_free': True, 'is_milk': True,
         'is_cold': True},
        {'name': 'Cold Brew Tonik', 'price': 60, 'is_coffee': True, "is_black_coffee": True,
         'is_cold': True},
        {'name': 'Espresso Tonik', 'price': 60, 'is_coffee': True, "is_black_coffee": True,
         'is_cold': True},



        {'name': 'Gaba Oolong', 'price': 50, 'is_tea': True},
        {'name': 'Grechaniy', 'price': 50, 'is_tea': True},
        {'name': 'Red(Black)', 'price': 50, 'is_tea': True},
        {'name': 'Fruit', 'price': 50, 'is_tea': True},
        {'name': 'White Tea', 'price': 50, 'is_tea': True},
        {'name': 'Da Hong Pao', 'price': 50, 'is_tea': True},
        {'name': 'Milk Oolong', 'price': 50, 'is_tea': True},
        {'name': 'Zhasmine Green', 'price': 50, 'is_tea': True},
        {'name': 'Roybush', 'price': 50, 'is_tea': True},
        {'name': 'Herbal', 'price': 50, 'is_tea': True},
        {'name': 'Pu-Erh Shen', 'price': 70, 'is_tea': True},
        {'name': 'Pu-Erh Shu', 'price': 70, 'is_tea': True},





        {'name': 'Matcha Shot', 'price': 60, "is_matcha": True},
        {'name': 'Matcha Orange', 'price': 80, "is_matcha": True, "is_fresh": True},
        {'name': 'Matcha Orange Cold', 'price': 80, "is_matcha": True, "is_fresh": True, "is_cold": True},
        {'name': 'Matcha Tonic', 'price': 75, "is_matcha": True, "is_cold": True},
        {'name': 'Matcha Latte', 'price': 60, "is_matcha": True, "is_milk": True},
        {'name': 'Matcha Latte Cold', 'price': 60, "is_matcha": True, 'is_cold': True, "is_milk": True},
        {'name': 'Ice Berry Matcha Latte', 'price': 70, "is_matcha": True, 'is_cold': True, "is_milk": True},
        {'name': 'Ice Berry Matcha Lact Free', 'price': 80, "is_matcha": True, 'is_cold': True,
         "is_milk": True, 'is_lact_free': True},
        {'name': 'Ice Berry Matcha Alternative', 'price': 90, "is_matcha": True, 'is_cold': True,
         "is_milk": True, 'is_lact_free': True},
        {'name': 'Matcha Latte Lact Free', 'price': 70, "is_matcha": True, "is_milk": True, 'is_lact_free': True},
        {'name': 'Matcha Latte Lact Free Cold', 'price': 70, "is_matcha": True, 'is_cold': True, "is_milk": True,
         'is_lact_free': True},
        {'name': 'Matcha Latte Alternative', 'price': 80, "is_matcha": True, "is_milk": True, 'is_lact_free': True},
        {'name': 'Matcha Latte Alternative Cold', 'price': 80, "is_matcha": True, 'is_cold': True, "is_milk": True,
         'is_lact_free': True},

    ]
    for i in menu_items:
        op.bulk_insert(table, [i])


def downgrade() -> None:
    op.drop_table('menu_item')
