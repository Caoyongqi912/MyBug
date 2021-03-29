"""empty message

Revision ID: 89d1747933af
Revises: 
Create Date: 2021-03-26 10:03:06.046366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89d1747933af'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bug_model',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('name', sa.String(length=32), nullable=True, comment='bug模版'),
    sa.Column('content', sa.TEXT(), nullable=True, comment='模版内容'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('department',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=True, comment='部门名'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('project',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=True, comment='项目名'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True, comment='产品名'),
    sa.Column('projectId', sa.Integer(), nullable=False, comment='所属项目'),
    sa.ForeignKeyConstraint(['projectId'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('account', sa.String(length=20), nullable=True, comment='用户名'),
    sa.Column('name', sa.String(length=20), nullable=True, comment='真实姓名'),
    sa.Column('password', sa.String(length=50), nullable=True, comment='密码'),
    sa.Column('gender', sa.Boolean(), nullable=True, comment='性别'),
    sa.Column('admin', sa.Boolean(), nullable=True, comment='管理员'),
    sa.Column('department', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['department'], ['department.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('build',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=True, comment='版本编号'),
    sa.Column('product', sa.Integer(), nullable=False, comment='所属产品'),
    sa.ForeignKeyConstraint(['product'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('error_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=True, comment='错误类型'),
    sa.Column('product', sa.Integer(), nullable=False, comment='所属产品'),
    sa.ForeignKeyConstraint(['product'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('module',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=True, comment='模块名'),
    sa.Column('product', sa.Integer(), nullable=True, comment='所属产品'),
    sa.ForeignKeyConstraint(['product'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('platform',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=True, comment='平台名称'),
    sa.Column('product', sa.Integer(), nullable=False, comment='所属产品'),
    sa.ForeignKeyConstraint(['product'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('solution',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=True, comment='解决方案名'),
    sa.Column('product', sa.Integer(), nullable=False, comment='所属产品'),
    sa.ForeignKeyConstraint(['product'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bugs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=True, comment='BUG标题'),
    sa.Column('level', sa.Enum('p1', 'p2', 'p3', 'p4'), server_default='p3', nullable=True, comment='BUG严重等级'),
    sa.Column('priority', sa.Enum('p1', 'p2', 'p3', 'p4'), server_default='p3', nullable=True, comment='BUG优先级'),
    sa.Column('status', sa.Enum('ACTIVE', 'RESOLVED', 'CLOSED'), server_default='ACTIVE', nullable=True, comment='BUG状态'),
    sa.Column('confirmed', sa.Boolean(), nullable=True, comment='是否确认'),
    sa.Column('creater', sa.Integer(), nullable=False, comment='创建者'),
    sa.Column('updater', sa.Integer(), nullable=True, comment='修改者'),
    sa.Column('assignedTo', sa.Integer(), nullable=True, comment='指派给'),
    sa.Column('resolvedBy', sa.Integer(), nullable=True, comment='解决者'),
    sa.Column('mailTo', sa.Integer(), nullable=True, comment='抄送给'),
    sa.Column('stepsBody', sa.TEXT(), nullable=True, comment='步骤'),
    sa.Column('solution', sa.Integer(), nullable=True, comment='解决方案'),
    sa.Column('platform', sa.Integer(), nullable=True, comment='测试平台'),
    sa.Column('module', sa.Integer(), nullable=True, comment='所属模块'),
    sa.Column('product', sa.Integer(), nullable=True, comment='所属项目'),
    sa.Column('build', sa.Integer(), nullable=False, comment='版本'),
    sa.Column('errorType', sa.Integer(), nullable=True, comment='错误类型'),
    sa.ForeignKeyConstraint(['assignedTo'], ['user.id'], ),
    sa.ForeignKeyConstraint(['build'], ['build.id'], ),
    sa.ForeignKeyConstraint(['creater'], ['user.id'], ),
    sa.ForeignKeyConstraint(['errorType'], ['error_type.id'], ),
    sa.ForeignKeyConstraint(['mailTo'], ['user.id'], ),
    sa.ForeignKeyConstraint(['module'], ['module.id'], ),
    sa.ForeignKeyConstraint(['platform'], ['platform.id'], ),
    sa.ForeignKeyConstraint(['product'], ['product.id'], ),
    sa.ForeignKeyConstraint(['resolvedBy'], ['user.id'], ),
    sa.ForeignKeyConstraint(['solution'], ['solution.id'], ),
    sa.ForeignKeyConstraint(['updater'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('bugs', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_bugs_title'), ['title'], unique=False)

    op.create_table('bug_file',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('fileName', sa.String(length=60), nullable=True, comment='文件名'),
    sa.Column('filePath', sa.String(length=100), nullable=True, comment='文件地址'),
    sa.Column('bugID', sa.Integer(), nullable=True, comment='所属bug'),
    sa.ForeignKeyConstraint(['bugID'], ['bugs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('note',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('bug', sa.Integer(), nullable=False, comment='所属bug'),
    sa.Column('content', sa.TEXT(), nullable=True, comment='备注内容'),
    sa.Column('noteMan', sa.Integer(), nullable=False, comment='备注人'),
    sa.ForeignKeyConstraint(['bug'], ['bugs.id'], ),
    sa.ForeignKeyConstraint(['noteMan'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('note')
    op.drop_table('bug_file')
    with op.batch_alter_table('bugs', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_bugs_title'))

    op.drop_table('bugs')
    op.drop_table('solution')
    op.drop_table('platform')
    op.drop_table('module')
    op.drop_table('error_type')
    op.drop_table('build')
    op.drop_table('user')
    op.drop_table('product')
    op.drop_table('project')
    op.drop_table('department')
    op.drop_table('bug_model')
    # ### end Alembic commands ###