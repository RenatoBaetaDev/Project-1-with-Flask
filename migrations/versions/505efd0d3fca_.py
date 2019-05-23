"""empty message

Revision ID: 505efd0d3fca
Revises: 358ae147d2a5
Create Date: 2019-05-23 09:03:35.486570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '505efd0d3fca'
down_revision = '358ae147d2a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chapters', sa.Column('title', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chapters', 'title')
    # ### end Alembic commands ###
