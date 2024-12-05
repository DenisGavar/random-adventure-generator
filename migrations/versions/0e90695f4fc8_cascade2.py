"""cascade2

Revision ID: 0e90695f4fc8
Revises: 1d548b0fa149
Create Date: 2024-12-05 15:13:32.262126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e90695f4fc8'
down_revision = '1d548b0fa149'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('just', sa.String(length=80), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.drop_column('just')

    # ### end Alembic commands ###