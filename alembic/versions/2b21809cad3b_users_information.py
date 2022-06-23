"""users information

Revision ID: 2b21809cad3b
Revises: e7165d6581f3
Create Date: 2022-06-23 18:08:53.827292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b21809cad3b'
down_revision = 'e7165d6581f3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    table = op.create_table(
        'user_info',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('user_verified', sa.Boolean, server_default='0'),
        sa.Column('user_first.name', sa.String(50), nullable=False),
        sa.Column('user_last.name', sa.String(50), nullable=False),
        sa.Column('user_name', sa.String(50), nullable=False),
        sa.Column('sweet_samosy_ordered', sa.Integer, nullable=False),
        sa.Column('salty_samosy_ordered', sa.Integer, nullable=False),
        sa.Column('total_samosy_ordered', sa.Integer, nullable=False),

    )

    user_information = []

    for i in user_information:
        op.bulk_insert(table, [i])


def downgrade() -> None:
    op.drop_table('user_info')
