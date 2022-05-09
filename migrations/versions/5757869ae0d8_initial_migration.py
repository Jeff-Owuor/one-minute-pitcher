"""Initial Migration

Revision ID: 5757869ae0d8
Revises: 14e9792401a7
Create Date: 2022-05-08 22:33:03.247378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5757869ae0d8'
down_revision = '14e9792401a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('bio', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('profile_pic_path', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'profile_pic_path')
    op.drop_column('users', 'bio')
    # ### end Alembic commands ###