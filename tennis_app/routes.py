# routes.py
#
from flask import jsonify, render_template, request, json, url_for, abort
from flask_mail import Message
from flask_login import login_user, logout_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from werkzeug.security import check_password_hash
from tennis_app import app, mail
from werkzeug.security import generate_password_hash
from tennis_app.extensions import db
from tennis_app.models import Player, Game, User, Pontuacoes, Tournament, Pick, Round
from tennis_app.utils import ( extract_picks_with_game_id, process_picks_and_generate_games, ResultsPositionTournament, get_user_name_by_id, get_player_name_by_id)
import pandas as pd
from flask_mail import Message
from flask_wtf.csrf import generate_csrf
from sqlalchemy.exc import IntegrityError
import logging
# Rota para enviar os picks de um participante
from sqlalchemy.orm.exc import NoResultFound

# Configuração de Logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# Configuração do Serializer para gerar o token
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])


print("Definindo rotas...")


@app.route('/players/<short_name>/<int:year>', methods=['GET'])
def get_players_by_tournament(short_name, year):
    print(f"Buscando torneio: {short_name}, Ano: {year}")
    # Busca o torneio pelo short_name e year
    tournament = Tournament.query.filter_by(short_name=short_name, year=year).first()
    if not tournament:
        return jsonify({'error': 'Torneio não encontrado'}), 404

    # Busca jogadores associados a este torneio
    players = Player.query.filter_by(tournament_id=tournament.id).all()
    return jsonify([player.to_dict() for player in players])



@app.route('/submit_picks_tournaments/<short_name>/<int:year>', methods=['POST'])
def submit_picks_tournaments(short_name, year):
    tournament = Tournament.query.filter_by(short_name=short_name, year=year).first()
    if not tournament:
        return jsonify({"error": "Torneio não encontrado"}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    user_id = data.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Apagar registros antigos para evitar duplicidade
    Pick.query.filter_by(user_id=user_id, tournament_id=tournament.id).delete()
    Game.query.filter_by(user_id=user_id, tournament_id=tournament.id).delete()

    # Processar os novos picks e games
    picks_list = extract_picks_with_game_id(data, user_id, tournament.id)
    games_data = process_picks_and_generate_games(data, user_id, tournament.id)

    # Inserir novos picks e games no DB
    for pick in picks_list:
        db.session.add(Pick(**pick))
    
    games_objects = []
    for game in games_data:
        game_obj = Game(**game)
        db.session.add(game_obj)
        games_objects.append(game_obj)

    db.session.flush()  # Para obter IDs dos games inseridos
    
    # Associar game_id corretamente aos picks após games serem inseridos
    for pick in picks_list:
        pick_obj = Pick.query.filter_by(
            position=pick['position'],
            user_id=user_id,
            tournament_id=tournament.id
        ).first()
        
        if pick_obj:
            game_obj = next((g for g in games_objects if g.round_id == pick['round_id'] and 
                             g.player1_id == pick['player_id'] or g.player2_id == pick['player_id']), None)
            
            if game_obj:
                pick_obj.game_id = game_obj.id
    
    try:
        db.session.commit()
        return jsonify({'message': 'Picks and games submitted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/PicksOverview/<short_name>/<int:year>', methods=['GET'])
def picks_overview_by_tournament(short_name, year):
    with app.app_context():
        tournament = Tournament.query.filter_by(short_name=short_name, year=year).first()
        if not tournament:
            return jsonify({"error": "Torneio não encontrado"}), 404

        picks = Pick.query.filter_by(tournament_id=tournament.id).all()
        picks_output = []

        # Organize picks by user
        picks_by_user = {}
        for pick in picks:
            user_id = pick.user_id
            if user_id not in picks_by_user:
                picks_by_user[user_id] = []
            picks_by_user[user_id].append(pick)

        for user_id, user_picks in picks_by_user.items():
            user_output = {"User": get_user_name_by_id(user_id), "tournament_id": tournament.id}
            for pick in user_picks:
                player_name = get_player_name_by_id(pick.player_id)
                user_output[pick.position] = player_name
            picks_output.append(user_output)

        return jsonify(picks_output)

@app.route('/pontuacoes/<short_name>/<int:year>/<rodada>', methods=['GET'])
def get_pontuacoes_por_rodada_torneio(short_name, year, rodada):
    print(f"Rota chamada: /pontuacoes/{short_name}/{year}/{rodada}")
    # Buscar o torneio pelo short_name e year
    tournament = Tournament.query.filter_by(short_name=short_name, year=year).first()
    if not tournament:
        return jsonify({"error": "Torneio não encontrado"}), 404

    # Buscar pontuações para o torneio e rodada especificados
    pontuacoes = Pontuacoes.query.filter_by(tournament_id=tournament.id, rodada=rodada).all()
    if pontuacoes:
        # Adicionando tournament_id ao dicionário de cada pontuação
        pontuacoes_output = [pontuacao.to_dict() for pontuacao in pontuacoes]
        for pontuacao in pontuacoes_output:
            pontuacao['tournament_id'] = tournament.id  # Adiciona o tournament_id ao output
        return jsonify(pontuacoes_output), 200
    return jsonify({'message': 'Nenhuma pontuação encontrada para esta rodada neste torneio'}), 404

# Rota para obter as pontuações por rodada    
@app.route('/pontuacoes/rodada/<rodada>', methods=['GET'])
def get_pontuacoes_por_rodada(rodada):
    print("Rota chamada: /pontuacoes/rodada/<rodada>")
    pontuacoes = Pontuacoes.query.filter_by(rodada=rodada).all()
    if pontuacoes:
        return jsonify([pontuacao.to_dict() for pontuacao in pontuacoes]), 200
    return jsonify({'message': 'Nenhuma pontuação encontrada para esta rodada'}), 404

# Método auxiliar para converter o objeto Pontuacoes em dicionário
def to_dict(self):
    return {
        'id': self.id,
        'ranking_pp': self.ranking_pp,
        'ranking_pg': self.ranking_pg,
        'username': self.username,
        'pontos_possiveis': self.pontos_possiveis,
        'pontos_ganhos': self.pontos_ganhos,
        'rodada': self.rodada,
        'data_atualizacao': self.data_atualizacao.isoformat()
    }

# Adicionando o método to_dict à classe Pontuacoes
Pontuacoes.to_dict = to_dict



@app.route('/classified-players/<short_name>/<int:year>', methods=['GET'])
def classified_players_tournament(short_name, year):
    file_paths = {
        'AO': {
            2024: {
                    "QF": 'tennis_app/assets/AO2024/AO-2024-Results - QF.csv',
                    "SF": 'tennis_app/assets/AO2024/AO-2024-Results - SF.csv',
                    "F": 'tennis_app/assets/AO2024/AO-2024-Results - F.csv',
                    "Champion": 'tennis_app/assets/AO2024/AO-2024-Results - Champion.csv',
            }
        },
        'RIO': {
            2024: {
                "QF": 'tennis_app/assets/RIO2024/RIO-2024-Results - QF.csv',
                "SF": 'tennis_app/assets/RIO2024/RIO-2024-Results - SF.csv',
                "F": 'tennis_app/assets/RIO2024/RIO-2024-Results - F.csv',
                "Champion": 'tennis_app/assets/RIO2024/RIO-2024-Results - Champion.csv',
            }
        },
        'IW': {
            2024: {
                "QF": 'tennis_app/assets/IW2024/IW-2024-Results - QF.csv',
                "SF": 'tennis_app/assets/IW2024/IW-2024-Results - SF.csv',
                "F": 'tennis_app/assets/IW2024/IW-2024-Results - F.csv',
                "Champion": 'tennis_app/assets/IW2024/IW-2024-Results - Champion.csv',
            }
        },
    }

    paths = file_paths[short_name][year]
    result_dict = {}

    # Processa cada estágio do torneio e atualiza o result_dict
    for stage, path in paths.items():
        df = ResultsPositionTournament(path, short_name, year)
        # Para o campeão, precisamos apenas do nome, pois há apenas um campeão
        if stage == "Champion":
            result_dict[stage] = df['name'].iloc[0]
        else:
            for index, row in df.iterrows():
                position = f"{stage}{index + 1}"
                result_dict[position] = row['name']

    # Adiciona o tournament_id assumindo que todos os jogadores têm o mesmo id de torneio
# Adiciona o tournament_id assumindo que todos os jogadores têm o mesmo id de torneio
    if not df.empty:
        result_dict["tournament_id"] = int(df['tournament_id'].iloc[0])  # Converte para int nativo do Python


    return jsonify(result_dict)


# Rota para o login
@app.route('/api/login', methods=['POST'])
def login():
    # Receber dados da solicitação
    email = request.json.get('email')
    password = request.json.get('password')

    # Encontrar usuário pelo email
    user = User.query.filter_by(email=email).first()

    # Verificar se o usuário existe e se a senha está correta
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        # Incluir o 'id' e 'username' no objeto JSON de resposta
        return jsonify({
            'login': True, 
            'redirect': url_for('index'), 
            'username': user.username,
            'user_id': user.id  # Inclui o ID do usuário na resposta
        }), 200
    else:
        # Resposta para falha no login
        return jsonify({
            'login': False, 
            'message': 'Login Unsuccessful. Please check email and password'
        }), 401
# Certifique-se de remover render_template e não usar o Flask-WTF form se você estiver usando JSON para autenticação.

# Rota para realizar o logout
@app.route('/api/logout', methods=['POST'])
def logout():
    logout_user()
    # Retorna uma resposta JSON indicando sucesso no logout
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200
 

@app.route('/api/reset_password', methods=['POST'])
def reset_password():
    email = request.json.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        app.logger.info(f'Reset password attempt for non-existent email: {email}')
        # It's a good practice not to reveal whether an email exists in the system
        return jsonify({'message': 'If your email is registered, you will receive a password reset link.'}), 200

    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    token = serializer.dumps(email, salt='email-reset-salt')
    ## O token é enviado por e-mail
    # reset_url = f'https://solino.pythonanywhere.com/reset_password/{token}'
    reset_url = f'http://localhost:3000/reset_password/{token}'


    # Assuming you have a function to send emails
    send_reset_email(email, reset_url)
    app.logger.info(f'Password reset email sent to: {email}')
    return jsonify({'message': 'If your email is registered, you will receive a password reset link.'}), 200

def send_reset_email(email, url):
    msg = Message('Redefinição de Senha',
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email])
    msg.body = f'Por favor, clique no link para redefinir sua senha: {url}'
    mail.send(msg)

# Rota para redefinir a senha
@app.route('/api/reset_password/<token>', methods=['POST'])
def reset_password_token(token):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-reset-salt', max_age=3600)
    except (SignatureExpired, BadSignature) as e:
        app.logger.error(f'Invalid or expired token: {str(e)}')
        return jsonify({'message': 'Invalid or expired token.'}), 401

    user = User.query.filter_by(email=email).first()
    if not user:
        app.logger.error(f'Token decoding succeeded but no user found for email: {email}')
        return jsonify({'message': 'Invalid token.'}), 401

    data = request.get_json()
    new_password = data.get('password')
    if not new_password or len(new_password) < 6:
        return jsonify({'message': 'Password must be at least 6 characters long.'}), 400

    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    app.logger.info(f'Password reset successful for user: {email}')
    return jsonify({'message': 'Your password has been updated! You are now able to log in'}), 200


## Rota para registrar um novo usuário
@app.route('/api/signup', methods=['POST'])
def signup():
    # 1. Receber dados da solicitação
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # 2. Validação dos dados (exemplo simplificado)
    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    # 3. Verificar existência do usuário ou e-mail
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'Username or email already in use'}), 409

    # 4. Hashing da senha
    password_hash = generate_password_hash(password)

    # 5. Criação do novo usuário
    new_user = User(username=username, email=email, password_hash=password_hash)

    # 6. Salvar usuário no banco de dados
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Could not register user'}), 500
    
@app.route('/tournaments', methods=['GET'])
def get_tournaments():
    tournaments = Tournament.query.all()
    
    if not tournaments:
        abort(404, description="No tournaments found.")
    
    # Mapeamento estático de IDs de torneios para caminhos de PDFs
    pdf_paths = {
        1: '/AO24_v2.pdf',
        2: '/RIO24.pdf',
        3: '/IW24.pdf',
        5: '/IATE3_2024.pdf'
    }

    whatsapp_paths = {
        1: 'https://chat.whatsapp.com/J6A2yZPyTAy34LB4nk4Aqy',
        2: 'https://chat.whatsapp.com/LXJ6gTVP4nuDGJqhpt36uY',
        3: 'https://discord.com/channels/1203007430544465940/1218210454032351324',
        5: 'https://chat.whatsapp.com/BmB60wLYNibCpj7q293uCv'
    }
    
    tournaments_info = [{
        'id': tournament.id,
        'name': tournament.name,
        'short_name': tournament.short_name,
        'year': tournament.year,
        'status': tournament.status,
        'pdfPath': pdf_paths.get(tournament.id),
        'whatsapp_paths': whatsapp_paths.get(tournament.id),    # Utiliza o mapeamento para obter o caminho
    } for tournament in tournaments]

    return jsonify(tournaments_info), 200


@app.route('/csrf_token', methods=['GET'])
def csrf_token():
    return jsonify({'csrf_token': generate_csrf()})


# Rota principal que renderiza a página inicial
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
