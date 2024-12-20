"""empty message

Revision ID: 52b8e36de97f
Revises: e221e790bf34
Create Date: 2024-11-26 08:01:42.446365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52b8e36de97f'
down_revision = 'e221e790bf34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_type', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('sku', sa.String(length=50), nullable=False),
    sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sku')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('isbn', sa.String(length=13), nullable=False),
    sa.Column('author', sa.String(length=255), nullable=False),
    sa.Column('page_count', sa.Integer(), nullable=False),
    sa.Column('cover_type', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('isbn')
    )
    op.create_table('comic_books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('issue_number', sa.Integer(), nullable=False),
    sa.Column('series_title', sa.String(length=255), nullable=False),
    sa.Column('cover_type', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pricing',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('base_price', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('discount', sa.DECIMAL(precision=5, scale=2), nullable=True),
    sa.Column('tax_rate', sa.DECIMAL(precision=5, scale=2), nullable=True),
    sa.Column('final_price', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tshirts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('size', sa.String(length=10), nullable=False),
    sa.Column('color', sa.String(length=50), nullable=False),
    sa.Column('material', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('children_books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('age_group', sa.String(length=50), nullable=False),
    sa.Column('illustration_style', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['books.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('children_books')
    op.drop_table('tshirts')
    op.drop_table('pricing')
    op.drop_table('comic_books')
    op.drop_table('books')
    op.drop_table('users')
    op.drop_table('products')
    # ### end Alembic commands ###
