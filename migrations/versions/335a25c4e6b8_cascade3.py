"""cascade3

Revision ID: 335a25c4e6b8
Revises: 0e90695f4fc8
Create Date: 2024-12-05 15:14:27.891059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '335a25c4e6b8'
down_revision = '0e90695f4fc8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.drop_column('just')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('just', sa.VARCHAR(length=80), autoincrement=False, nullable=True))

    # ### end Alembic commands ###