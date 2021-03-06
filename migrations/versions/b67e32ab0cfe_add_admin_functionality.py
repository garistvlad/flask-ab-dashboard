"""Add admin functionality

Revision ID: b67e32ab0cfe
Revises: 89ce425914fa
Create Date: 2020-08-13 11:42:57.263942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b67e32ab0cfe'
down_revision = '89ce425914fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('option', 'control_group')
    op.add_column('user', sa.Column('is_admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_admin')
    op.add_column('option', sa.Column('control_group', sa.BOOLEAN(), nullable=True))
    # ### end Alembic commands ###
