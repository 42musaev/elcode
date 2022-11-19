"""update Note: add slug

Revision ID: e363b8170903
Revises: a98cf781c47e
Create Date: 2022-11-19 10:14:22.886326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e363b8170903'
down_revision = 'a98cf781c47e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('slug', sa.String(length=32), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notes', 'slug')
    # ### end Alembic commands ###
