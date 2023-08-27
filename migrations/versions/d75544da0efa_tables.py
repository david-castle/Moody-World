"""tables

Revision ID: d75544da0efa
Revises: 
Create Date: 2023-08-27 14:42:02.900917

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd75544da0efa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('firstname', sa.String(length=120), nullable=True),
    sa.Column('lastname', sa.String(length=120), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('registered_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_firstname'), ['firstname'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_lastname'), ['lastname'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('persistent_query',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('query_name', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('searchtermsAny', sa.String(length=240), nullable=True),
    sa.Column('searchtermsAll', sa.String(length=240), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('persistent_query', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_persistent_query_query_name'), ['query_name'], unique=True)
        batch_op.create_index(batch_op.f('ix_persistent_query_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('persistent_query', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_persistent_query_timestamp'))
        batch_op.drop_index(batch_op.f('ix_persistent_query_query_name'))

    op.drop_table('persistent_query')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_lastname'))
        batch_op.drop_index(batch_op.f('ix_user_firstname'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###
