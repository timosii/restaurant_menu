"""create_tables

Revision ID: 9afcc77e082a
Revises:
Create Date: 2023-08-11 12:45:58.063128

"""
from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9afcc77e082a'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menus',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('title', sa.String(), nullable=True),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('title')
                    )
    op.create_table('submenus',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('title', sa.String(), nullable=True),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('parent_menu_id', sa.UUID(), nullable=True),
                    sa.ForeignKeyConstraint(['parent_menu_id'], ['menus.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('title')
                    )
    op.create_table('dishes',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('title', sa.String(), nullable=True),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('price', sa.Numeric(scale=2), nullable=True),
                    sa.Column('parent_submenu_id', sa.UUID(), nullable=True),
                    sa.ForeignKeyConstraint(['parent_submenu_id'], ['submenus.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('title')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dishes')
    op.drop_table('submenus')
    op.drop_table('menus')
    # ### end Alembic commands ###
