"""Added x_request_id field for invoice

Revision ID: 28e8ea5e8a58
Revises: a8bc5434bf7c
Create Date: 2022-04-16 09:55:02.844361

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28e8ea5e8a58'
down_revision = 'a8bc5434bf7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invoices', sa.Column('x_request_id', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'invoices', ['x_request_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'invoices', type_='unique')
    op.drop_column('invoices', 'x_request_id')
    # ### end Alembic commands ###
