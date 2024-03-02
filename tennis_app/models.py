# models.py
from enum import Enum
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from tennis_app.extensions import db
from tennis_app import app
# from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_login import UserMixin
from sqlalchemy.orm import validates



# Definir o modelo Player
class Player(db.Model):
    __tablename__ = 'players'
    # Cada atributo da classe será uma coluna na tabela do banco de dados
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(3))  # Código do país ISO Alpha-3
    seed = db.Column(db.Integer)    # seed do jogador
    qf_number = db.Column(db.Integer, nullable=True)  # Novo campo adicionado
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)

    tournament = db.relationship('Tournament', backref='players')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country,
            "seed": self.seed,
            'qf_number': self.qf_number,
            'tournament': {
                "id": self.tournament.id,  # Adicionado para incluir o ID do torneio no retorno JSON
                "name": self.tournament.name,
                "short_name": self.tournament.short_name,
                "year": self.tournament.year,
                "status": self.tournament.status
            }
        }


    def __repr__(self):
        # Método de representação do objeto para facilitar a depuração e o log
        return f'<Player {self.name}, Country: {self.country}, seed: {self.seed},QF_number: {self.qf_number}>'
    
class RoundType(Enum):
    QF = 'QF'
    SF = 'SF'
    F = 'F'

    def __str__(self):
        return self.value


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Enum(RoundType), nullable=False)
    player1_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)  # Corrigido para 'players.id'
    player2_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)  # Corrigido para 'players.id'
    winner_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)    # Corrigido para 'players.id'
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)

    player1 = db.relationship('Player', foreign_keys=[player1_id], backref='games_as_player1')
    player2 = db.relationship('Player', foreign_keys=[player2_id], backref='games_as_player2')
    winner = db.relationship('Player', foreign_keys=[winner_id], backref='won_games')
    tournament = db.relationship('Tournament', backref='games')

    def __repr__(self):
        round_name = self.round.name if isinstance(self.round, Enum) else self.round
        return f'<Game {self.id} - Round: {round_name}, Player 1: {self.player1_id}, Player 2: {self.player2_id}, Winner: {self.winner_id}>' 

class Pick(db.Model):
    __tablename__ = 'picks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Corrigido para 'users.id'
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    winner_id = db.Column(db.Integer, db.ForeignKey('players.id'))  # Certifique-se de que 'players.id' esteja correto
    player1_id = db.Column(db.Integer)
    player2_id = db.Column(db.Integer)
    round = db.Column(db.Enum(RoundType))
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'))
    
    game = db.relationship('Game', foreign_keys=[game_id], backref='picks')
    tournament = db.relationship('Tournament', backref='picks')

    def __repr__(self):
        return f"<Pick - User: {self.user_id}, Game: {self.game_id}, Round: {self.round.name}, Player 1: {self.player1_id}, Player 2: {self.player2_id}, Winner: {self.winner_id}>"

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    picks = db.relationship('Pick', backref='user', lazy='dynamic')

    def get_reset_token(self, expires_sec=1800):
        print("Tipo da SECRET_KEY:", type(app.config['SECRET_KEY']))
        print("Valor da SECRET_KEY:", app.config['SECRET_KEY'])
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    ## Verifica o reset
    @staticmethod
    def verify_reset_token(token):
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, salt='password-reset-salt', max_age=3600)
        except (SignatureExpired, BadSignature):
            return None
        return User.query.get(user_id)

    @property
    def is_active(self):
        # Aqui você pode adicionar lógica para determinar se um usuário está ativo
        # Por exemplo, você pode ter um campo na sua tabela de usuários que indica se eles estão ativos
        # Neste exemplo simples, vamos apenas retornar True para indicar que todos os usuários estão ativos
        return True

    def __repr__(self):
        return f'<User {self.username}>'
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Pontuacoes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ranking_pp = db.Column(db.Integer, nullable=True)  # Coluna para Ranking PP
    ranking_pg = db.Column(db.Integer, nullable=True)  # Coluna para Ranking PG
    username = db.Column(db.String(80), unique=False, nullable=False)
    pontos_possiveis = db.Column(db.Integer, nullable=True)
    pontos_ganhos = db.Column(db.Integer, nullable=True)
    rodada = db.Column(db.String(50), nullable=False)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)

    tournament = db.relationship('Tournament', backref='pontuacoes')

    def __repr__(self):
        return f'<Pontuacoes {self.id}, {self.ranking_pp}, {self.ranking_pg}, {self.username}, {self.pontos_possiveis}, {self.pontos_ganhos}, {self.rodada}, {self.data_atualizacao}, {self.tournament_id}>'

class TournamentStatus:
    OPEN = 'Open'
    ON_PROGRESS = 'On Progress'
    CLOSED = 'Closed'
    VALID_STATUSES = [OPEN, ON_PROGRESS, CLOSED]

class Tournament(db.Model):
    __tablename__ = 'tournaments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    short_name = db.Column(db.String(20), nullable=False)  # Nome reduzido para o torneio
    year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False) # Status do torneio (ex: 'Open', 'On Progress', 'Closed')

    @validates('status')
    def validate_status(self, key, status):
        if status not in TournamentStatus.VALID_STATUSES:
            raise ValueError(f"Status '{status}' is invalid. Valid statuses are: {TournamentStatus.VALID_STATUSES}")
        return status

    def __repr__(self):
            return f'<Tournament {self.name}, Short Name: {self.short_name}, Year: {self.year}, Status: {self.status}>'


# from tennis_app import db

### Para atualizar o banco de dados, execute os seguintes comandos no terminal:
## Ativar o ambiente virtual
## comando para ativar a variável de ambiente no PowerShell
# $env:FLASK_APP = "D:\TENIS\Smash_Picks\SF_app\run.py"
## comando para ativar a variável de ambiente no CMD
# set FLASK_APP=D:\TENIS\Smash_Picks\SF_app\run.py
    
## criar o banco de dados
# flask --app tennis_app db init  
## criar a migração para uma nova tabela
# flask db migrate -m "Descrever migração"
# flask db upgrade