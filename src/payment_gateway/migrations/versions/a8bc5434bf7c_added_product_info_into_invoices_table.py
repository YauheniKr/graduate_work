"""Added product info into invoices table

Revision ID: a8bc5434bf7c
Revises: 563de231ebda
Create Date: 2022-04-13 19:52:27.532141

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'a8bc5434bf7c'
down_revision = '563de231ebda'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    state_enum = sa.Enum('not_paid', 'paid', 'failed', name='invoicestate')
    state_enum.create(op.get_bind())

    op.add_column('invoices', sa.Column('state', state_enum, nullable=False))
    op.add_column('invoices', sa.Column('product_name', sa.String(), nullable=True))
    op.add_column('invoices', sa.Column('product_count', sa.Integer(), nullable=True))
    op.add_column('invoices', sa.Column('product_price_currency', sa.String(), nullable=True))
    op.add_column('invoices', sa.Column('product_price_amount_total', sa.Float(), nullable=True))
    op.create_unique_constraint(None, 'invoices', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'invoices', type_='unique')
    op.drop_column('invoices', 'product_price_amount_total')
    op.drop_column('invoices', 'product_price_currency')
    op.drop_column('invoices', 'product_count')
    op.drop_column('invoices', 'product_name')
    op.drop_column('invoices', 'state')
    # ### end Alembic commands ###
