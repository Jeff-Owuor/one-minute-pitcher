"""Downvotes  Migration

Revision ID: 260906369891
Revises: 33b2303b6849
Create Date: 2022-05-09 22:34:50.773862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '260906369891'
down_revision = '33b2303b6849'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('downvotes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('pitch_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pitch_id'], ['pitches.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('downvotes')
    # ### end Alembic commands ###
