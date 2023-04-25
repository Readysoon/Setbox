"""empty message

Revision ID: e84a1f150c9f
Revises: 
Create Date: 2023-04-20 15:51:29.645734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e84a1f150c9f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.VARCHAR(length=255), nullable=False),
        sa.Column("password", sa.VARCHAR(length=1024), nullable=False),
        sa.Column("first_name", sa.VARCHAR(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "subjects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.VARCHAR(length=255), nullable=False),
        sa.Column("owner_user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "owner_user_id", name="_name_for_owner"),
    )
    op.create_table(
        "lessons",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("name", sa.VARCHAR(length=255), nullable=True),
        sa.ForeignKeyConstraint(
            ["subject_id"],
            ["subjects.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users_in_subjects",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.Column("editor", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["subject_id"],
            ["subjects.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "subject_id"),
    )
    op.create_table(
        "files",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.VARCHAR(length=255), nullable=False),
        sa.Column("type", sa.VARCHAR(length=20), nullable=True),
        sa.Column("filename", sa.VARCHAR(length=255), nullable=False),
        sa.Column("lesson_id", sa.Integer(), nullable=False),
        sa.Column("reviewed", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["lesson_id"],
            ["lessons.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("files")
    op.drop_table("users_in_subjects")
    op.drop_table("lessons")
    op.drop_table("subjects")
    op.drop_table("users")
    # ### end Alembic commands ###
