"""empty message

Revision ID: d14dd3339cd4
Revises: None
Create Date: 2015-12-26 13:14:23.842000

"""

# revision identifiers, used by Alembic.
revision = 'd14dd3339cd4'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('category', 'name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.create_unique_constraint(None, 'category', ['name'])
    op.add_column('post', sa.Column('date', sa.Date(), nullable=False))
    op.add_column('post', sa.Column('slug', sa.String(length=255), nullable=False))
    op.alter_column('post', 'category_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('post', 'content',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('post', 'title',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.create_unique_constraint(None, 'post', ['title'])
    op.create_unique_constraint(None, 'post', ['slug'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='unique')
    op.drop_constraint(None, 'post', type_='unique')
    op.alter_column('post', 'title',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('post', 'content',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('post', 'category_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.drop_column('post', 'slug')
    op.drop_column('post', 'date')
    op.drop_constraint(None, 'category', type_='unique')
    op.alter_column('category', 'name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    ### end Alembic commands ###