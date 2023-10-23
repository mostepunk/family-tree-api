"""init accounts

Revision ID: e1fc52b2c6d1
Revises:
Create Date: 2023-10-24 00:19:23.953029

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "e1fc52b2c6d1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "roles",
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=10), nullable=False),
        sa.Column(
            "uuid",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("level", "name"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "accounts",
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("is_enabled", sa.Boolean(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("role_uuid", sa.UUID(), nullable=False),
        sa.Column("last_visit", sa.DateTime(), nullable=True),
        sa.Column("person_uuid", sa.UUID(), nullable=True),
        sa.Column(
            "uuid",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["role_uuid"],
            ["roles.uuid"],
        ),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_accounts_username"), "accounts", ["username"], unique=True)
    op.execute(
        """
    INSERT INTO roles (level, name) VALUES
        (0, 'ROOT'),
        (0, 'IT_STAFF'),
        (1, 'ADMIN'),
        (2, 'WRITE'),
        (3, 'READ')
    """
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_accounts_username"), table_name="accounts")
    op.drop_table("accounts")
    op.drop_table("roles")
    # ### end Alembic commands ###
