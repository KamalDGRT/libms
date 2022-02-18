"""auto-gen-user-login-table

Revision ID: 1be4e7eba80d
Revises: 34671b031325
Create Date: 2022-02-18 06:50:27.695228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1be4e7eba80d'
down_revision = '34671b031325'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_login',
                    sa.Column('user_login_id', sa.Integer(), nullable=False),
                    sa.Column('user_profile_id', sa.Integer(), nullable=False),
                    sa.Column('email_address', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(['user_profile_id'], [
                        'user_profile.user_profile_id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_login_id')
                    )
    op.create_index(op.f('ix_user_login_user_login_id'),
                    'user_login', ['user_login_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_login_user_login_id'), table_name='user_login')
    op.drop_table('user_login')
    # ### end Alembic commands ###
