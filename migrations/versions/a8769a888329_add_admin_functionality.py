"""Add admin functionality

Revision ID: a8769a888329
Revises: b67e32ab0cfe
Create Date: 2020-08-13 11:44:09.412248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8769a888329'
down_revision = 'b67e32ab0cfe'
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