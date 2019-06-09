"""user model and other mods

Revision ID: 56b6e488b81e
Revises: cbb2054b549f
Create Date: 2019-06-08 19:10:29.300981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56b6e488b81e'
down_revision = 'cbb2054b549f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=140), nullable=True),
    sa.Column('email_confirmed', sa.Boolean(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.add_column('address', sa.Column('address_path', sa.String(length=140), nullable=True))
    op.add_column('address', sa.Column('report_path', sa.String(length=140), nullable=True))
    op.add_column('address', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_index('ix_address_address', table_name='address')
    op.create_unique_constraint(None, 'address', ['address_path'])
    op.create_unique_constraint(None, 'address', ['report_path'])
    op.create_foreign_key(None, 'address', 'user', ['user_id'], ['id'])
    op.drop_column('address', 'report_folder')
    op.drop_column('address', 'address_folder')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('address', sa.Column('address_folder', sa.VARCHAR(length=140), autoincrement=False, nullable=True))
    op.add_column('address', sa.Column('report_folder', sa.VARCHAR(length=140), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'address', type_='foreignkey')
    op.drop_constraint(None, 'address', type_='unique')
    op.drop_constraint(None, 'address', type_='unique')
    op.create_index('ix_address_address', 'address', ['address'], unique=True)
    op.drop_column('address', 'user_id')
    op.drop_column('address', 'report_path')
    op.drop_column('address', 'address_path')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
