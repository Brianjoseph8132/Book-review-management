"""Initial migration.

Revision ID: 680a10d8414e
Revises: 
Create Date: 2025-01-19 00:19:36.036931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '680a10d8414e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('author', sa.String(length=100), nullable=False),
    sa.Column('genre', sa.String(length=50), nullable=False),
    sa.Column('published_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('review_text', sa.Text(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    op.drop_table('users')
    op.drop_table('books')
    # ### end Alembic commands ###
