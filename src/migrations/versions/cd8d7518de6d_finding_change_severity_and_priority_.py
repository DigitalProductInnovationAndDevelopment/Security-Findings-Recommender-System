"""Finding: Change severity and priority type to Integer

Revision ID: cd8d7518de6d
Revises: d99b83c34c69
Create Date: 2024-07-17 09:50:03.635826

"""

import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from alembic import op

import db

# revision identifiers, used by Alembic.
revision = "cd8d7518de6d"
down_revision = "e12b06b380db"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        "ALTER TABLE findings ALTER COLUMN priority TYPE INTEGER USING priority::integer"
    )
    op.execute(
        "ALTER TABLE findings ALTER COLUMN severity TYPE INTEGER USING severity::integer"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "findings",
        "severity",
        existing_type=sa.Integer(),
        type_=sa.VARCHAR(),
        existing_nullable=True,
    )
    op.alter_column(
        "findings",
        "priority",
        existing_type=sa.Integer(),
        type_=sa.VARCHAR(),
        existing_nullable=True,
    )
    # ### end Alembic commands ###
