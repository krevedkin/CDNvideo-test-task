"""add coords fields to city model

Revision ID: 2c5a927d5f6d
Revises: 1221e2049c92
Create Date: 2024-01-26 02:53:45.072023

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2c5a927d5f6d"
down_revision: Union[str, None] = "1221e2049c92"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("cities", sa.Column("longitude", sa.Float(), nullable=False))
    op.add_column("cities", sa.Column("latitude", sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("cities", "latitude")
    op.drop_column("cities", "longitude")
    # ### end Alembic commands ###
