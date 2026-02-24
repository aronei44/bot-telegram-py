"""create roles table

Revision ID: 00b5d5da7556
Revises: 0724c468fa41
Create Date: 2023-05-07 14:38:29.136374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00b5d5da7556'
down_revision = '0724c468fa41'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'roles',
        sa.Column('role_name', sa.String, primary_key=True, unique=True),
        sa.Column('min_val', sa.Integer, nullable=True),
        sa.Column('max_val', sa.Integer, nullable=True),
    )


def downgrade() -> None:
    op.drop_table('roles')
