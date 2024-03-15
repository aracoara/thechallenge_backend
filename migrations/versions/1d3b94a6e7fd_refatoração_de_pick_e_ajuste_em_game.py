"""refatoração de Pick e ajuste em Game

Revision ID: 1d3b94a6e7fd
Revises: 84b442064be1
Create Date: 2024-03-10 07:16:47.936188

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1d3b94a6e7fd'
down_revision = '84b442064be1'
branch_labels = None
depends_on = None

def upgrade():
    # Criando a tabela rounds, se não existir.
    op.create_table(
        'rounds',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True)
    )

    # Adicionando a coluna round_id à tabela games e definindo uma foreign key.
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.add_column(sa.Column('round_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_games_round_id', 'rounds', ['round_id'], ['id'])

    # Adicionando a coluna round_id à tabela picks e definindo uma foreign key.
    with op.batch_alter_table('picks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('round_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_picks_round_id', 'rounds', ['round_id'], ['id'])
        batch_op.create_foreign_key('fk_picks_user_id', 'users', ['user_id'], ['id'])

def downgrade():
    # Removendo as foreign keys e colunas adicionadas nas tabelas 'games' e 'picks', e removendo a tabela 'rounds'.
    with op.batch_alter_table('picks', schema=None) as batch_op:
        batch_op.drop_constraint('fk_picks_user_id', type_='foreignkey')
        batch_op.drop_constraint('fk_picks_round_id', type_='foreignkey')
        batch_op.drop_column('round_id')

    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.drop_constraint('fk_games_round_id', type_='foreignkey')
        batch_op.drop_column('round_id')

    op.drop_table('rounds')
