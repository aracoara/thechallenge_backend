"""retirada de round_id de picks

Revision ID: a7d29182988b
Revises: dcb65c720274
Create Date: 2024-03-10 23:59:06.120259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7d29182988b'
down_revision = 'dcb65c720274'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('picks', schema=None) as batch_op:
        batch_op.drop_constraint('fk_picks_rounds', type_='foreignkey')
        batch_op.drop_column('round_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('picks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('round_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key('fk_picks_rounds', 'rounds', ['round_id'], ['id'])

    # ### end Alembic commands ###
