"""change_category

Revision ID: 06253ed3ac28
Revises: 9e31625c7978
Create Date: 2024-07-26 11:07:19.507484

"""

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
import db


# revision identifiers, used by Alembic.
revision = "06253ed3ac28"
down_revision = "9e31625c7978"
branch_labels = None
depends_on = None


def upgrade():

    op.execute(
        "ALTER TABLE recommendations ALTER COLUMN category  TYPE json using category::json;"
    )

    op.execute(
        "alter table findings alter column category type json using category::json;"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "recommendations",
        "category",
        existing_type=sa.JSON(),
        type_=sa.VARCHAR(),
        existing_nullable=True,
    )
    op.alter_column(
        "findings",
        "category",
        existing_type=sa.JSON(),
        type_=sa.VARCHAR(),
        existing_nullable=True,
    )
    # ### end Alembic commands ###