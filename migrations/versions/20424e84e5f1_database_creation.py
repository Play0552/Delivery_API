"""Database creation

Revision ID: 20424e84e5f1
Revises: 
Create Date: 2023-11-23 17:12:27.228409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '20424e84e5f1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courier_table',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('districts', postgresql.ARRAY(sa.String()), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_courier_table_districts'), 'courier_table', ['districts'], unique=False)
    op.create_table('order_table',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('district', sa.String(), nullable=False),
    sa.Column('status', sa.Enum('in_progress', 'completed', name='status'), nullable=False),
    sa.Column('start_time', sa.TIMESTAMP(), nullable=False),
    sa.Column('end_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('courier_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['courier_id'], ['courier_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_table')
    op.drop_index(op.f('ix_courier_table_districts'), table_name='courier_table')
    op.drop_table('courier_table')
    # ### end Alembic commands ###