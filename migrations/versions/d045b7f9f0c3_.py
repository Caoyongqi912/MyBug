"""empty message

Revision ID: d045b7f9f0c3
Revises: 93f3f273f174
Create Date: 2021-03-05 19:18:55.754859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd045b7f9f0c3'
down_revision = '93f3f273f174'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('module',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=True, comment='模块名'),
    sa.Column('product', sa.Integer(), nullable=False, comment='所属产品'),
    sa.ForeignKeyConstraint(['product'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('bugs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('module', sa.Integer(), nullable=True, comment='所属模块'))
        batch_op.create_foreign_key(None, 'module', ['module'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bugs', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('module')

    op.drop_table('module')
    # ### end Alembic commands ###
