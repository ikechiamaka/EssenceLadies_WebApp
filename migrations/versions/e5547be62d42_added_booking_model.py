"""Added Booking model

Revision ID: e5547be62d42
Revises: 0613f0e9519f
Create Date: 2024-08-10 18:21:29.802709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5547be62d42'
down_revision = '0613f0e9519f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('booking',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('escort_name', sa.String(length=100), nullable=False),
        sa.Column('telephone', sa.String(length=20), nullable=False),
        sa.Column('time_to_call', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('location', sa.String(length=200), nullable=False),
        sa.Column('length_of_booking', sa.String(length=20), nullable=False),
        sa.Column('date_of_booking', sa.Date(), nullable=False),
        sa.Column('additional_details', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('booking')
    # ### end Alembic commands ###
