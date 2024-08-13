from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'caeac9069b95'
down_revision = 'f2722ace39c4'
branch_labels = None
depends_on = None

def upgrade():
    # Create an inspector to check if the table exists
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    if 'profile_picture' in inspector.get_table_names():
        op.drop_table('profile_picture')

    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_picture', sa.String(length=20), nullable=True))
        batch_op.alter_column('age', existing_type=sa.INTEGER(), nullable=False)
        batch_op.alter_column('nationality', existing_type=sa.VARCHAR(length=50), nullable=False)
        batch_op.alter_column('height', existing_type=sa.VARCHAR(length=10), nullable=False)
        batch_op.alter_column('stats', existing_type=sa.VARCHAR(length=50), type_=sa.String(length=10), nullable=False)
        batch_op.alter_column('dress_size', existing_type=sa.VARCHAR(length=10), nullable=False)
        batch_op.alter_column('hair_color', existing_type=sa.VARCHAR(length=50), type_=sa.String(length=20), nullable=False)
        batch_op.alter_column('eye_color', existing_type=sa.VARCHAR(length=50), type_=sa.String(length=20), nullable=False)
        batch_op.alter_column('service_level', existing_type=sa.VARCHAR(length=50), type_=sa.String(length=20), nullable=False)
        batch_op.alter_column('languages', existing_type=sa.VARCHAR(length=100), nullable=False)

def downgrade():
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.alter_column('languages', existing_type=sa.VARCHAR(length=100), nullable=True)
        batch_op.alter_column('service_level', existing_type=sa.String(length=20), type_=sa.VARCHAR(length=50), nullable=True)
        batch_op.alter_column('eye_color', existing_type=sa.String(length=20), type_=sa.VARCHAR(length=50), nullable=True)
        batch_op.alter_column('hair_color', existing_type=sa.String(length=20), type_=sa.VARCHAR(length=50), nullable=True)
        batch_op.alter_column('dress_size', existing_type=sa.VARCHAR(length=10), nullable=True)
        batch_op.alter_column('stats', existing_type=sa.String(length=10), type_=sa.VARCHAR(length=50), nullable=True)
        batch_op.alter_column('height', existing_type=sa.VARCHAR(length=10), nullable=True)
        batch_op.alter_column('nationality', existing_type=sa.VARCHAR(length=50), nullable=True)
        batch_op.alter_column('age', existing_type=sa.INTEGER(), nullable=True)
        batch_op.drop_column('profile_picture')

    op.create_table('profile_picture',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('image_path', sa.VARCHAR(length=255), nullable=False),
        sa.Column('profile_id', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
