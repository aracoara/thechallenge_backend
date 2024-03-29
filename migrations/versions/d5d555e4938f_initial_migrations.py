"""initial migrations

Revision ID: d5d555e4938f
Revises: 
Create Date: 2024-02-20 13:38:45.856227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5d555e4938f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tournaments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('short_name', sa.String(length=20), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('country', sa.String(length=3), nullable=True),
    sa.Column('seed', sa.Integer(), nullable=True),
    sa.Column('qf_number', sa.Integer(), nullable=True),
    sa.Column('tournament_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tournament_id'], ['tournaments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pontuacoes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ranking_pp', sa.Integer(), nullable=True),
    sa.Column('ranking_pg', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('pontos_possiveis', sa.Integer(), nullable=True),
    sa.Column('pontos_ganhos', sa.Integer(), nullable=True),
    sa.Column('rodada', sa.String(length=50), nullable=False),
    sa.Column('data_atualizacao', sa.DateTime(), nullable=True),
    sa.Column('tournament_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tournament_id'], ['tournaments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('games',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('round', sa.Enum('QF', 'SF', 'F', name='roundtype'), nullable=False),
    sa.Column('player1_id', sa.Integer(), nullable=False),
    sa.Column('player2_id', sa.Integer(), nullable=False),
    sa.Column('winner_id', sa.Integer(), nullable=True),
    sa.Column('tournament_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['player1_id'], ['players.id'], ),
    sa.ForeignKeyConstraint(['player2_id'], ['players.id'], ),
    sa.ForeignKeyConstraint(['tournament_id'], ['tournaments.id'], ),
    sa.ForeignKeyConstraint(['winner_id'], ['players.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('picks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('winner_id', sa.Integer(), nullable=True),
    sa.Column('player1_id', sa.Integer(), nullable=True),
    sa.Column('player2_id', sa.Integer(), nullable=True),
    sa.Column('round', sa.Enum('QF', 'SF', 'F', name='roundtype'), nullable=True),
    sa.Column('tournament_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.ForeignKeyConstraint(['tournament_id'], ['tournaments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['winner_id'], ['players.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('picks')
    op.drop_table('games')
    op.drop_table('pontuacoes')
    op.drop_table('players')
    op.drop_table('users')
    op.drop_table('tournaments')
    # ### end Alembic commands ###
