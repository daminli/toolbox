"""empty message

Revision ID: 3370509f0992
Revises: 0fa006f108bf
Create Date: 2017-06-17 21:18:30.500484

"""

# revision identifiers, used by Alembic.
revision = '3370509f0992'
down_revision = '0fa006f108bf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fq_report_prop', sa.Column('is_filter1', sa.Integer(), nullable=True))
    op.add_column('fq_report_prop', sa.Column('req_filter1', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fq_report_prop', 'req_filter1')
    op.drop_column('fq_report_prop', 'is_filter1')
    # ### end Alembic commands ###