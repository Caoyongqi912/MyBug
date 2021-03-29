"""empty message

Revision ID: 4bdc54131719
Revises: 89d1747933af
Create Date: 2021-03-26 14:30:26.430775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bdc54131719'
down_revision = '89d1747933af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('build', schema=None) as batch_op:
        batch_op.add_column(sa.Column('builder', sa.String(length=20), nullable=True, comment='构建者'))
        batch_op.add_column(sa.Column('desc', sa.String(length=50), nullable=True, comment='描述'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('build', schema=None) as batch_op:
        batch_op.drop_column('desc')
        batch_op.drop_column('builder')

    # ### end Alembic commands ###
