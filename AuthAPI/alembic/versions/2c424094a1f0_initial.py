"""initial

Revision ID: 2c424094a1f0
Revises:
Create Date: 2024-05-12 07:46:35.057510

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c424094a1f0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
                    sa.Column('uuid', sa.Uuid(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('users',
                    sa.Column('uuid', sa.Uuid(), nullable=False),
                    sa.Column('login', sa.String(length=255), nullable=False),
                    sa.Column('email', sa.String(length=255), nullable=False),
                    sa.Column('password', sa.String(length=255), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('surname', sa.String(length=255), nullable=True),
                    sa.Column('is_superuser', sa.Boolean(), nullable=False),
                    sa.Column('mail_verified', sa.Boolean(), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('login')
                    )
    op.create_table('user_history',
                    sa.Column('uuid', sa.Uuid(), nullable=False),
                    sa.Column('user_id', sa.Uuid(), nullable=False),
                    sa.Column('user_agent', sa.String(length=255), nullable=True),
                    sa.Column('refresh_token', sa.Text(), nullable=True),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.uuid'], ),
                    sa.PrimaryKeyConstraint('uuid')
                    )
    op.create_table('user_social_services',
                    sa.Column('uuid', sa.Uuid(), nullable=False),
                    sa.Column('user_id', sa.Uuid(), nullable=False),
                    sa.Column('social_user_id', sa.Text(), nullable=False),
                    sa.Column('type', sa.Enum('Yandex', 'Google', name='socialnetworksenum'), nullable=False),
                    sa.Column('data', sa.JSON(), nullable=True),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.uuid'], ),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('social_user_id', 'type')
                    )
    op.create_table('users_roles',
                    sa.Column('uuid', sa.Uuid(), nullable=False),
                    sa.Column('user_id', sa.Uuid(), nullable=False),
                    sa.Column('role_id', sa.Uuid(), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['role_id'], ['roles.uuid'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.uuid'], ),
                    sa.PrimaryKeyConstraint('uuid')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_roles')
    op.drop_table('user_social_services')
    op.drop_table('user_history')
    op.drop_table('users')
    op.drop_table('roles')
    # ### end Alembic commands ###
