"""initialize

Revision ID: 5a77a313df99
Revises: 
Create Date: 2024-06-12 09:32:28.148889

"""

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
import db


# revision identifiers, used by Alembic.
revision = "5a77a313df99"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "recommendation_task",
        sa.Column(
            "status",
            sa.Enum("PENDING", "COMPLETED", "FAILED", name="taskstatus"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("external_id", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("preferences", sa.String(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "findings",
        sa.Column("title_list", sa.JSON(), nullable=True),
        sa.Column("description_list", sa.JSON(), nullable=True),
        sa.Column("locations_list", sa.JSON(), nullable=True),
        sa.Column("cwe_id_list", sa.JSON(), nullable=True),
        sa.Column("cve_id_list", sa.JSON(), nullable=True),
        sa.Column("priority", sa.String(), nullable=True),
        sa.Column("severity", sa.String(), nullable=True),
        sa.Column("language", sa.String(), nullable=True),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column("report_amount", sa.Integer(), nullable=False),
        sa.Column("raw_data", sa.JSON(), nullable=True),
        sa.Column("recommendation_task_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["recommendation_task_id"], ["recommendation_task.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "recommendations",
        sa.Column("description_short", sa.String(), nullable=True),
        sa.Column("description_long", sa.String(), nullable=True),
        sa.Column("search_terms", sa.String(), nullable=True),
        sa.Column("meta", sa.JSON(), nullable=True),
        sa.Column("finding_id", sa.Integer(), nullable=True),
        sa.Column("recommendation_task_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["finding_id"],
            ["findings.id"],
        ),
        sa.ForeignKeyConstraint(
            ["recommendation_task_id"], ["recommendation_task.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("recommendations")
    op.drop_table("findings")
    op.drop_table("users")
    op.drop_table("recommendation_task")
    # ### end Alembic commands ###
