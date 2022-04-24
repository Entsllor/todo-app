"""add refresh token model

Revision ID: 6636e49cbd16
Revises: fc3351d428d1
Create Date: 2022-04-24 13:08:26.795205

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6636e49cbd16'
down_revision = 'fc3351d428d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('refresh_token',
    sa.Column('body', sa.String(length=127), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('expire_at', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('body')
    )
    op.create_index(op.f('ix_refresh_token_expire_at'), 'refresh_token', ['expire_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_refresh_token_expire_at'), table_name='refresh_token')
    op.drop_table('refresh_token')
    # ### end Alembic commands ###
