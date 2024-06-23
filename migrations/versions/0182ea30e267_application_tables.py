"""application tables

Revision ID: 0182ea30e267
Revises: 
Create Date: 2024-06-22 12:14:24.865039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0182ea30e267'
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
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_firstname'), ['firstname'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_lastname'), ['lastname'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('query',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('query_terms', sa.String(length=240), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('query', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_query_timestamp'), ['timestamp'], unique=False)

    op.create_table('stored_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('query_id', sa.Integer(), nullable=True),
    sa.Column('source', sa.String(length=240), nullable=True),
    sa.Column('author', sa.String(length=240), nullable=True),
    sa.Column('title', sa.String(length=480), nullable=True),
    sa.Column('description', sa.String(length=960), nullable=True),
    sa.Column('url', sa.String(length=960), nullable=True),
    sa.Column('url_to_image', sa.String(length=960), nullable=True),
    sa.Column('published_on', sa.String(length=240), nullable=True),
    sa.Column('content', sa.String(length=1920), nullable=True),
    sa.Column('SentimentScore', sa.String(length=240), nullable=True),
    sa.Column('Compound', sa.Float(), nullable=True),
    sa.Column('Popup', sa.String(length=960), nullable=True),
    sa.Column('LocationNames', sa.String(length=240), nullable=True),
    sa.Column('Coordinates', sa.String(length=120), nullable=True),
    sa.Column('Latitude', sa.Float(), nullable=True),
    sa.Column('Longitude', sa.Float(), nullable=True),
    sa.Column('FrequentWords', sa.String(length=480), nullable=True),
    sa.Column('Colors', sa.String(length=120), nullable=True),
    sa.Column('Ranking', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['query_id'], ['query.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stored_results')
    with op.batch_alter_table('query', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_query_timestamp'))

    op.drop_table('query')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_lastname'))
        batch_op.drop_index(batch_op.f('ix_user_firstname'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###