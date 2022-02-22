"""auto generate reviews table

Revision ID: d4ea4b372ca3
Revises: 12542ae067f9
Create Date: 2022-02-22 13:50:40.036963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4ea4b372ca3'
down_revision = '12542ae067f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('review',
    sa.Column('review_id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('given_by', sa.Integer(), nullable=False),
    sa.Column('given_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['book.book_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['given_by'], ['user_profile.user_profile_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('review_id')
    )
    op.create_index(op.f('ix_review_review_id'), 'review', ['review_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_review_review_id'), table_name='review')
    op.drop_table('review')
    # ### end Alembic commands ###
