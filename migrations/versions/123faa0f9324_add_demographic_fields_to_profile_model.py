"""Add demographic fields to Profile model

Revision ID: 123faa0f9324
Revises: 72b00d05ea56
Create Date: 2024-08-09 13:17:17.350491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '123faa0f9324'
down_revision = '72b00d05ea56'
branch_labels = None
depends_on = None




def upgrade():
    with op.batch_alter_table('profile') as batch_op:
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('nationality', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('height', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('stats', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('dress_size', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('hair_color', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('eye_color', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('service_level', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('languages', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('bisexual', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('incall_location', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('outcall_location', sa.String(length=100), nullable=True))

def downgrade():
    with op.batch_alter_table('profile') as batch_op:
        batch_op.drop_column('age')
        batch_op.drop_column('nationality')
        batch_op.drop_column('height')
        batch_op.drop_column('stats')
        batch_op.drop_column('dress_size')
        batch_op.drop_column('hair_color')
        batch_op.drop_column('eye_color')
        batch_op.drop_column('service_level')
        batch_op.drop_column('languages')
        batch_op.drop_column('bisexual')
        batch_op.drop_column('incall_location')
        batch_op.drop_column('outcall_location')

    # ### end Alembic commands ###
