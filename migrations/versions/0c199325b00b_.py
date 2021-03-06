"""empty message

Revision ID: 0c199325b00b
Revises: 
Create Date: 2020-07-06 06:49:11.741825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c199325b00b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('corps',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('corpcode', sa.String(length=20), nullable=True),
    sa.Column('corpname', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stockprices',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('target_date', sa.DateTime(), nullable=True),
    sa.Column('corp_id', sa.Integer(), nullable=True),
    sa.Column('is_holiday', sa.Boolean(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['corp_id'], ['corps.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stockprices')
    op.drop_table('corps')
    # ### end Alembic commands ###
