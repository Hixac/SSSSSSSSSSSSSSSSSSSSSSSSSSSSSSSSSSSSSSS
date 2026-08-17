"""drop groups roles add postponed group domain

Revision ID: 5f8a1b2c3d4e
Revises: eb97220641d6
Create Date: 2026-08-17 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f8a1b2c3d4e'
down_revision: Union[str, Sequence[str], None] = 'eb97220641d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Replace postponed_items.group_id FK with plain group_domain column; drop groups and roles tables."""
    op.drop_constraint(
        'postponed_items_group_id_fkey',
        'postponed_items',
        type_='foreignkey',
    )
    op.drop_column('postponed_items', 'group_id')
    op.add_column(
        'postponed_items',
        sa.Column(
            'group_domain',
            sa.String(length=255),
            nullable=False,
            server_default='',
        ),
    )
    op.create_index(
        op.f('ix_postponed_items_group_domain'),
        'postponed_items',
        ['group_domain'],
        unique=False,
    )
    op.alter_column('postponed_items', 'group_domain', server_default=None)

    op.drop_index(op.f('ix_roles_created_at'), table_name='roles')
    op.drop_index(op.f('ix_roles_deleted_at'), table_name='roles')
    op.drop_table('roles')

    op.drop_index(op.f('ix_groups_domain'), table_name='groups')
    op.drop_index(op.f('ix_groups_deleted_at'), table_name='groups')
    op.drop_index(op.f('ix_groups_created_at'), table_name='groups')
    op.drop_table('groups')

    sa.Enum(name='roletype').drop(op.get_bind(), checkfirst=True)


def downgrade() -> None:
    """Restore groups and roles tables. group_id values are lost — column restored as nullable."""
    op.create_table(
        'groups',
        sa.Column('domain', sa.String(length=255), nullable=False),
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('modified_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('groups_pkey')),
    )
    op.create_index(op.f('ix_groups_created_at'), 'groups', ['created_at'], unique=False)
    op.create_index(op.f('ix_groups_deleted_at'), 'groups', ['deleted_at'], unique=False)
    op.create_index(op.f('ix_groups_domain'), 'groups', ['domain'], unique=True)

    roletype = sa.Enum('admin', 'editor', name='roletype')
    roletype.create(op.get_bind(), checkfirst=True)
    op.create_table(
        'roles',
        sa.Column('role', roletype, nullable=False),
        sa.Column('group_id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('modified_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name=op.f('roles_group_id_fkey')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('roles_user_id_fkey')),
        sa.PrimaryKeyConstraint('role', 'group_id', 'user_id', name=op.f('roles_pkey')),
    )
    op.create_index(op.f('ix_roles_created_at'), 'roles', ['created_at'], unique=False)
    op.create_index(op.f('ix_roles_deleted_at'), 'roles', ['deleted_at'], unique=False)

    op.drop_index(op.f('ix_postponed_items_group_domain'), table_name='postponed_items')
    op.drop_column('postponed_items', 'group_domain')
    op.add_column('postponed_items', sa.Column('group_id', sa.Uuid(), nullable=True))
    op.create_foreign_key(
        'postponed_items_group_id_fkey',
        'postponed_items',
        'groups',
        ['group_id'],
        ['id'],
    )
