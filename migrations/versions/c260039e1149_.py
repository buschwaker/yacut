"""empty message

Revision ID: c260039e1149
Revises: 
Create Date: 2022-11-26 09:27:46.947964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c260039e1149'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('URL_map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original', sa.String(), nullable=False),
    sa.Column('short', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short')
    )
    op.create_index(op.f('ix_URL_map_timestamp'), 'URL_map', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_URL_map_timestamp'), table_name='URL_map')
    op.drop_table('URL_map')
    # ### end Alembic commands ###
