"""empty message

Revision ID: 94c8a3b2507d
Revises: ea9c782f5978
Create Date: 2017-06-17 21:11:08.218011

"""

# revision identifiers, used by Alembic.
revision = '94c8a3b2507d'
down_revision = 'ea9c782f5978'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fq_report_prop', sa.Column('is_filter', sa.Integer(), nullable=True))
    op.add_column('fq_report_prop', sa.Column('req_filter', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fq_report_prop', 'req_filter')
    op.drop_column('fq_report_prop', 'is_filter')
    # ### end Alembic commands ###
