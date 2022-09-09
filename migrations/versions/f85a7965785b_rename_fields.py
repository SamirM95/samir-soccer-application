"""rename fields

Revision ID: f85a7965785b
Revises: 1ef6bf78a10f
Create Date: 2022-09-08 09:33:13.704758

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f85a7965785b'
down_revision = '1ef6bf78a10f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('accounts', 'Username')
    op.drop_column('accounts', 'Password')
    op.add_column('accounts', sa.Column('username', sa.String(length=20), nullable=False))
    op.add_column('accounts', sa.Column('password', sa.String(length=20), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('accounts', 'password')
    op.drop_column('accounts', 'username')
    op.add_column('accounts', sa.Column('Password', mysql.VARCHAR(length=20), nullable=False))
    op.add_column('accounts', sa.Column('Username', mysql.VARCHAR(length=20), nullable=False))
    # ### end Alembic commands ###
