"""revert last migration of role_id

Revision ID: f90501c16f82
Revises: 91236e6a87d4
Create Date: 2022-02-21 04:05:26.265923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f90501c16f82'
down_revision = '91236e6a87d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_login_role_id_fkey', 'user_login', type_='foreignkey')
    op.drop_column('user_login', 'role_id')
    op.add_column('user_profile', sa.Column('role_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'user_profile', 'role', ['role_id'], ['role_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_profile', type_='foreignkey')
    op.drop_column('user_profile', 'role_id')
    op.add_column('user_login', sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('user_login_role_id_fkey', 'user_login', 'role', ['role_id'], ['role_id'], ondelete='CASCADE')
    # ### end Alembic commands ###
