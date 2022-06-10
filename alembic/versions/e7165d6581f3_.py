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
        sa.Column('is_lactose_free', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_lact_free', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_tea', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_cold', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('is_black_coffee', sa.Boolean, nullable=False, server_default='0'),

    )

    menu_items = [
        {'name': 'Espresso', 'price': 35, 'is_coffee': True, 'is_tea': False, 'is_black_coffee': True},
        {'name': 'Filter', 'price': 40, 'is_coffee': True, 'is_tea': False, 'is_black_coffee': True},
        {'name': 'Clever', 'price': 65, 'is_coffee': True, 'is_tea': False, 'is_black_coffee': True},
        {'name': 'Aeropress', 'price': 65, 'is_coffee': True, 'is_tea': False, 'is_black_coffee': True},
        {'name': 'Delter', 'price': 65, 'is_coffee': True, 'is_tea': False, 'is_black_coffee': True},
        {'name': 'Cappuccino', 'price': 40, 'is_coffee': True, 'is_tea': False, 'is_milk': True},
        {'name': 'Cappuccino Lactose Free', 'price': 50, 'parent_id': 6, 'is_coffee': True, 'is_tea': False,
         'is_milk': False, 'is_lact_free': True},
        {'name': 'Cappuccino Alternative', 'price': 60, 'parent_id': 6, 'is_coffee': True, 'is_tea': False,
         'is_milk': False, 'is_lact_free': True},
        {'name': 'Caffe Latte', 'price': 45, 'is_coffee': True, 'is_tea': False, 'is_milk': True},
        {'name': 'Caffe Latte Lactose Free', 'price': 55, 'is_coffee': True, 'is_tea': False, 'is_milk': False,
         'is_lact_free': True},
        {'name': 'Caffe Latte Alternative', 'price': 65, 'is_coffee': True, 'is_tea': False, 'is_milk': False,
         'is_lact_free': True},
        {'name': 'Flat White', 'price': 45, 'is_coffee': True, 'is_tea': False, 'is_milk': True},
        {'name': 'Flat White Lactose Free', 'price': 55, 'is_coffee': True, 'is_tea': False, 'is_milk': False,
         'is_lact_free': True},
        {'name': 'Flat White Alternative', 'price': 65, 'is_coffee': True, 'is_tea': False, 'is_milk': False,
         'is_lact_free': True},
        {'name': 'Double Cappuccino', 'price': 50, 'is_coffee': True, 'is_tea': False, 'is_milk': True},
        {'name': 'Double Cappuccino Lactose Free', 'price': 60, 'is_coffee': True, 'is_tea': False, 'is_milk': False,
         'is_lact_free': True},
        {'name': 'Double Cappuccino Alternative', 'price': 70, 'is_coffee': True, 'is_tea': False, 'is_milk': False,
         'is_lact_free': True},
        {'name': 'Raf', 'price': 65, 'is_coffee': True, 'is_tea': False, 'is_milk': True, 'is_lact_free': False},
        {'name': 'Raf Lactose Free', 'price': 75, 'is_coffee': True, 'is_tea': False, 'is_milk': False,
         'is_lact_free': True},
        {'name': 'Raf Alternative', 'price': 85, 'is_coffee': True, 'is_tea': False, 'is_milk': False,
         'is_lact_free': True},
        {'name': 'Capuorange', 'price': 70, 'is_coffee': True, 'is_tea': False, 'is_milk': False, 'is_lact_free': True},

        {'name': 'Cold Brew', 'price': 50, 'is_coffee': True, 'is_cold': True, 'is_black_coffee': True},
        {'name': 'Cold Brew Colada', 'price': 75, 'is_coffee': True, 'is_lact_free': True},
        {'name': 'Gaba', 'price': 50, 'is_coffee': False, 'is_tea': True},
        {'name': 'Grachaniy', 'price': 50, 'is_coffee': False, 'is_tea': True},
        {'name': 'Red', 'price': 50, 'is_coffee': False, 'is_tea': True},
        {'name': 'White', 'price': 50, 'is_coffee': False, 'is_tea': True},
        {'name': 'White', 'price': 50, 'is_coffee': False, 'is_tea': True},
        {'name': 'White', 'price': 50, 'is_coffee': False, 'is_tea': True},
    ]
    for i in menu_items:
        op.bulk_insert(table, [i])


def downgrade() -> None:
    op.drop_table('menu_item')
