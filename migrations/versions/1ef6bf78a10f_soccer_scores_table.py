"""soccer_scores_table

Revision ID: 1ef6bf78a10f
Revises: ca3a7af52aad
Create Date: 2022-09-08 09:13:18.295705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ef6bf78a10f'
down_revision = 'ca3a7af52aad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('soccer_score',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('home', sa.String(length=255), nullable=False),
    sa.Column('away', sa.String(length=255), nullable=False),
    sa.Column('score_home_team', sa.String(length=255), nullable=False),
    sa.Column('score_away_team', sa.String(length=255), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('soccer_score')
    # ### end Alembic commands ###
