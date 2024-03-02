from tennis_app import app
from tennis_app.extensions import db
from tennis_app.models import User, Pick, Game, Player, Tournament


users_data = [
    {'username': 'Ana', 'email': 'ana@example.com', 'password_hash': 'hash_ana'},
    {'username': 'Bruno', 'email': 'bruno@example.com', 'password_hash': 'hash_bruno'},
    {'username': 'Carla', 'email': 'carla@example.com', 'password_hash': 'hash_carla'},
    {'username': 'Diego', 'email': 'diego@example.com', 'password_hash': 'hash_diego'},
    {'username': 'Eduarda', 'email': 'eduarda@example.com', 'password_hash': 'hash_eduarda'},
    {'username': 'Fábio', 'email': 'fábio@example.com', 'password_hash': 'hash_fábio'},
    {'username': 'Gisele', 'email': 'gisele@example.com', 'password_hash': 'hash_gisele'},
    {'username': 'Henrique', 'email': 'henrique@example.com', 'password_hash': 'hash_henrique'},
    {'username': 'Isabela', 'email': 'isabela@example.com', 'password_hash': 'hash_isabela'},
    {'username': 'João', 'email': 'joão@example.com', 'password_hash': 'hash_joão'},
    {'username': 'Larissa', 'email': 'larissa@example.com', 'password_hash': 'hash_larissa'},
    {'username': 'Márcio', 'email': 'márcio@example.com', 'password_hash': 'hash_márcio'},
    {'username': 'Nívea', 'email': 'nívea@example.com', 'password_hash': 'hash_nívea'},
    {'username': 'Otávio', 'email': 'otávio@example.com', 'password_hash': 'hash_otávio'},
    {'username': 'Patrícia', 'email': 'patrícia@example.com', 'password_hash': 'hash_patrícia'},
    {'username': 'Quintino', 'email': 'quintino@example.com', 'password_hash': 'hash_quintino'},
    {'username': 'Rafaela', 'email': 'rafaela@example.com', 'password_hash': 'hash_rafaela'},
    {'username': 'Sandro', 'email': 'sandro@example.com', 'password_hash': 'hash_sandro'},
    {'username': 'Tatiane', 'email': 'tatiane@example.com', 'password_hash': 'hash_tatiane'},
    {'username': 'Umberto', 'email': 'umberto@example.com', 'password_hash': 'hash_umberto'},
    {'username': 'Viviane', 'email': 'viviane@example.com', 'password_hash': 'hash_viviane'},
    {'username': 'William', 'email': 'william@example.com', 'password_hash': 'hash_william'},
    {'username': 'Xuxa', 'email': 'xuxa@example.com', 'password_hash': 'hash_xuxa'},
    {'username': 'Yasmin', 'email': 'yasmin@example.com', 'password_hash': 'hash_yasmin'},
    {'username': 'Zilda', 'email': 'zilda@example.com', 'password_hash': 'hash_zilda'},
    {'username': 'Ricardo', 'email': 'ricardo@example.com', 'password_hash': 'hash_ricardo'},
    {'username': 'Priscila', 'email': 'priscila@example.com', 'password_hash': 'hash_priscila'},
    {'username': 'Olga', 'email': 'olga@example.com', 'password_hash': 'hash_olga'},
    {'username': 'Natan', 'email': 'natan@example.com', 'password_hash': 'hash_natan'},
    {'username': 'Mônica', 'email': 'mônica@example.com', 'password_hash': 'hash_mônica'},
    {'username': 'Leonardo', 'email': 'leonardo@example.com', 'password_hash': 'hash_leonardo'},
    {'username': 'Kátia', 'email': 'kátia@example.com', 'password_hash': 'hash_kátia'},
    {'username': 'Júlio', 'email': 'júlio@example.com', 'password_hash': 'hash_júlio'},
    {'username': 'Íris', 'email': 'íris@example.com', 'password_hash': 'hash_íris'},
    {'username': 'Hugo', 'email': 'hugo@example.com', 'password_hash': 'hash_hugo'}
]


def add_users_to_database(users_data):
    with app.app_context():
        # Verifica se os usuários já existem para evitar duplicatas
        existing_usernames = {user.username for user in User.query.all()}
        for user_info in users_data:
            if user_info['username'] not in existing_usernames:
                new_user = User(**user_info)
                db.session.add(new_user)
        db.session.commit()

if __name__ == '__main__':
    add_users_to_database(users_data)
    print("Usuários adicionados com sucesso.")

games_data =  [
    {"round": "QF", "player1_id": 1, "player2_id": 31, "winner_id": 1, "tournament_id":1},
    {"round": "QF", "player1_id": 32, "player2_id": 63, "winner_id": 32, "tournament_id":1},
    {"round": "QF", "player1_id": 77, "player2_id": 91, "winner_id": 91, "tournament_id":1},
    {"round": "QF", "player1_id": 92, "player2_id": 121, "winner_id": 121, "tournament_id":1},
    {"round": "SF", "player1_id": 1, "player2_id": 32, "winner_id": 1, "tournament_id":1},
    {"round": "SF", "player1_id": 91, "player2_id": 121, "winner_id": 121, "tournament_id":1},
    {"round": "F", "player1_id": 1, "player2_id": 121, "winner_id": 1, "tournament_id":1}
]

def add_games_to_database(games_data):
    from tennis_app.models import Game
    with app.app_context():
        # Verifica se os jogos já existem para evitar duplicatas
        existing_games = {game.round for game in Game.query.all()}
        for game_info in games_data:
            if game_info['round'] not in existing_games:
                new_game = Game(**game_info)
                db.session.add(new_game)
        db.session.commit()

if __name__ == '__main__':
    add_games_to_database(games_data)
    print("Jogos adicionados com sucesso.")  

picks_data = [
    {"user_id": 1, "game_id": 1, "winner_id": 1, "player1_id": 1, "player2_id": 31, "round": "QF"},
    {"user_id": 1, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 1, "game_id": 3, "winner_id": 78, "player1_id": 77, "player2_id": 78, "round": "QF"},
    {"user_id": 1, "game_id": 4, "winner_id": 92, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 1, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 1, "game_id": 6, "winner_id": 92, "player1_id": 78, "player2_id": 92, "round": "SF"},
    {"user_id": 1, "game_id": 7, "winner_id": 32, "player1_id": 32, "player2_id": 92, "round": "F"},
    {"user_id": 2, "game_id": 1, "winner_id": 1, "player1_id": 1, "player2_id": 17, "round": "QF"},
    {"user_id": 2, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 55, "round": "QF"},
    {"user_id": 2, "game_id": 3, "winner_id": 91, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 2, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 2, "game_id": 5, "winner_id": 1, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 2, "game_id": 6, "winner_id": 121, "player1_id": 91, "player2_id": 121, "round": "SF"},
    {"user_id": 2, "game_id": 7, "winner_id": 1, "player1_id": 1, "player2_id": 121, "round": "F"},
    {"user_id": 3, "game_id": 1, "winner_id": 1, "player1_id": 1, "player2_id": 24, "round": "QF"},
    {"user_id": 3, "game_id": 1, "winner_id": 1, "player1_id": 1, "player2_id": 24, "round": "QF"},
    {"user_id": 3, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 3, "game_id": 3, "winner_id": 91, "player1_id": 77, "player2_id": 91, "round": "QF"},
    {"user_id": 3, "game_id": 4, "winner_id": 92, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 3, "game_id": 5, "winner_id": 1, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 3, "game_id": 6, "winner_id": 91, "player1_id": 91, "player2_id": 92, "round": "SF"},
    {"user_id": 3, "game_id": 7, "winner_id": 1, "player1_id": 1, "player2_id": 91, "round": "F"},
    {"user_id": 4, "game_id": 1, "winner_id": 1, "player1_id": 1, "player2_id": 24, "round": "QF"},
    {"user_id": 4, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 4, "game_id": 3, "winner_id": 91, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 4, "game_id": 4, "winner_id": 92, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 4, "game_id": 5, "winner_id": 1, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 4, "game_id": 6, "winner_id": 91, "player1_id": 91, "player2_id": 121, "round": "SF"},
    {"user_id": 4, "game_id": 7, "winner_id": 32, "player1_id": 32, "player2_id": 121, "round": "F"},
    {"user_id": 5, "game_id": 1, "winner_id": 1, "player1_id": 1, "player2_id": 24, "round": "QF"},
    {"user_id": 5, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 5, "game_id": 3, "winner_id": 91, "player1_id": 77, "player2_id": 91, "round": "QF"},
    {"user_id": 5, "game_id": 4, "winner_id": 92, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 5, "game_id": 5, "winner_id": 1, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 5, "game_id": 6, "winner_id": 91, "player1_id": 91, "player2_id": 121, "round": "SF"},
    {"user_id": 5, "game_id": 7, "winner_id": 1, "player1_id": 1, "player2_id": 121, "round": "F"},
    {"user_id": 6, "game_id": 1, "winner_id": 1, "player1_id": 24, "player2_id": 1, "round": "QF"},
    {"user_id": 6, "game_id": 2, "winner_id": 32, "player1_id": 48, "player2_id": 32, "round": "QF"},
    {"user_id": 6, "game_id": 3, "winner_id": 91, "player1_id": 77, "player2_id": 91, "round": "QF"},
    {"user_id": 6, "game_id": 4, "winner_id": 92, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 6, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 6, "game_id": 6, "winner_id": 121, "player1_id": 78, "player2_id": 121, "round": "SF"},
    {"user_id": 6, "game_id": 7, "winner_id": 32, "player1_id": 32, "player2_id": 121, "round": "F"},
    {"user_id": 7, "game_id": 1, "winner_id": 1, "player1_id": 31, "player2_id": 1, "round": "QF"},
    {"user_id": 7, "game_id": 2, "winner_id": 63, "player1_id": 40, "player2_id": 63, "round": "QF"},
    {"user_id": 7, "game_id": 3, "winner_id": 64, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 7, "game_id": 4, "winner_id": 92, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 7, "game_id": 5, "winner_id": 1, "player1_id": 1, "player2_id": 63, "round": "SF"},
    {"user_id": 7, "game_id": 6, "winner_id": 92, "player1_id": 64, "player2_id": 92, "round": "SF"},
    {"user_id": 7, "game_id": 7, "winner_id": 1, "player1_id": 1, "player2_id": 92, "round": "F"},
    {"user_id": 8, "game_id": 1, "winner_id": 1, "player1_id": 29, "player2_id": 1, "round": "QF"},
    {"user_id": 8, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 56, "round": "QF"},
    {"user_id": 8, "game_id": 3, "winner_id": 91, "player1_id": 77, "player2_id": 91, "round": "QF"},
    {"user_id": 8, "game_id": 4, "winner_id": 92, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 8, "game_id": 5, "winner_id": 1, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 8, "game_id": 6, "winner_id": 92, "player1_id": 91, "player2_id": 92, "round": "SF"},
    {"user_id": 8, "game_id": 7, "winner_id": 1, "player1_id": 1, "player2_id": 92, "round": "F"},
    {"user_id": 9, "game_id": 1, "winner_id": 16, "player1_id": 31, "player2_id": 16, "round": "QF"},
    {"user_id": 9, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 56, "round": "QF"},
    {"user_id": 9, "game_id": 3, "winner_id": 78, "player1_id": 64, "player2_id": 78, "round": "QF"},
    {"user_id": 9, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 9, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 9, "game_id": 6, "winner_id": 121, "player1_id": 78, "player2_id": 121, "round": "SF"},
    {"user_id": 9, "game_id": 7, "winner_id": 32, "player1_id": 32, "player2_id": 121, "round": "F"},
    {"user_id": 10, "game_id": 1, "winner_id": 1, "player1_id": 17, "player2_id": 1, "round": "QF"},
    {"user_id": 10, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 10, "game_id": 3, "winner_id": 77, "player1_id": 77, "player2_id": 78, "round": "QF"},
    {"user_id": 10, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 10, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 10, "game_id": 6, "winner_id": 92, "player1_id": 78, "player2_id": 92, "round": "SF"},
    {"user_id": 10, "game_id": 7, "winner_id": 32, "player1_id": 32, "player2_id": 92, "round": "F"},
    {"user_id": 11, "game_id": 1, "winner_id": 1, "player1_id": 17, "player2_id": 1, "round": "QF"},
    {"user_id": 11, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 55, "round": "QF"},
    {"user_id": 11, "game_id": 3, "winner_id": 77, "player1_id": 77, "player2_id": 78, "round": "QF"},
    {"user_id": 11, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 11, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 11, "game_id": 6, "winner_id": 121, "player1_id": 77, "player2_id": 121, "round": "SF"},
    {"user_id": 11, "game_id": 7, "winner_id": 32, "player1_id": 32, "player2_id": 121, "round": "F"},
    {"user_id": 12, "game_id": 1, "winner_id": 1, "player1_id": 17, "player2_id": 1, "round": "QF"},
    {"user_id": 12, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 12, "game_id": 3, "winner_id": 91, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 12, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 12, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 12, "game_id": 6, "winner_id": 121, "player1_id": 91, "player2_id": 121, "round": "SF"},
    {"user_id": 12, "game_id": 7, "winner_id": 121, "player1_id": 121, "player2_id": 1, "round": "F"},
    {"user_id": 13, "game_id": 1, "winner_id": 1, "player1_id": 17, "player2_id": 1, "round": "QF"},
    {"user_id": 13, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 48, "round": "QF"},
    {"user_id": 13, "game_id": 3, "winner_id": 64, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 13, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 13, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 13, "game_id": 6, "winner_id": 121, "player1_id": 64, "player2_id": 121, "round": "SF"},
    {"user_id": 13, "game_id": 7, "winner_id": 64, "player1_id": 64, "player2_id": 121, "round": "F"},
    {"user_id": 14, "game_id": 1, "winner_id": 1, "player1_id": 31, "player2_id": 1, "round": "QF"},
    {"user_id": 14, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 14, "game_id": 3, "winner_id": 64, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 14, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 14, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 14, "game_id": 6, "winner_id": 64, "player1_id": 64, "player2_id": 121, "round": "SF"},
    {"user_id": 14, "game_id": 7, "winner_id": 1, "player1_id": 1, "player2_id": 64, "round": "F"},
    {"user_id": 15, "game_id": 1, "winner_id": 1, "player1_id": 17, "player2_id": 1, "round": "QF"},
    {"user_id": 15, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 15, "game_id": 3, "winner_id": 64, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 15, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 15, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 15, "game_id": 6, "winner_id": 91, "player1_id": 91, "player2_id": 121, "round": "SF"},
    {"user_id": 15, "game_id": 7, "winner_id": 91, "player1_id": 91, "player2_id": 32, "round": "F"},
    {"user_id": 16, "game_id": 1, "winner_id": 1, "player1_id": 31, "player2_id": 1, "round": "QF"},
    {"user_id": 16, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 48, "round": "QF"},
    {"user_id": 16, "game_id": 3, "winner_id": 77, "player1_id": 77, "player2_id": 91, "round": "QF"},
    {"user_id": 16, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 16, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 16, "game_id": 6, "winner_id": 121, "player1_id": 91, "player2_id": 121, "round": "SF"},
    {"user_id": 16, "game_id": 7, "winner_id": 121, "player1_id": 121, "player2_id": 1, "round": "F"},
    {"user_id": 17, "game_id": 1, "winner_id": 1, "player1_id": 31, "player2_id": 1, "round": "QF"},
    {"user_id": 17, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 17, "game_id": 3, "winner_id": 91, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 17, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 17, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 17, "game_id": 6, "winner_id": 121, "player1_id": 77, "player2_id": 121, "round": "SF"},
    {"user_id": 17, "game_id": 7, "winner_id": 32, "player1_id": 32, "player2_id": 121, "round": "F"},
    {"user_id": 18, "game_id": 1, "winner_id": 1, "player1_id": 31, "player2_id": 1, "round": "QF"},
    {"user_id": 18, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 18, "game_id": 3, "winner_id": 91, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 18, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 18, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 18, "game_id": 6, "winner_id": 91, "player1_id": 91, "player2_id": 121, "round": "SF"},
    {"user_id": 18, "game_id": 7, "winner_id": 121, "player1_id": 121, "player2_id": 1, "round": "F"},
    {"user_id": 19, "game_id": 1, "winner_id": 1, "player1_id": 17, "player2_id": 1, "round": "QF"},
    {"user_id": 19, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 48, "round": "QF"},
    {"user_id": 19, "game_id": 3, "winner_id": 64, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 19, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 19, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 19, "game_id": 6, "winner_id": 121, "player1_id": 91, "player2_id": 121, "round": "SF"},
    {"user_id": 19, "game_id": 7, "winner_id": 121, "player1_id": 121, "player2_id": 1, "round": "F"},
    {"user_id": 20, "game_id": 1, "winner_id": 1, "player1_id": 17, "player2_id": 1, "round": "QF"},
    {"user_id": 20, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 20, "game_id": 3, "winner_id": 91, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 20, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 20, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 20, "game_id": 6, "winner_id": 91, "player1_id": 91, "player2_id": 121, "round": "SF"},
    {"user_id": 20, "game_id": 7, "winner_id": 121, "player1_id": 121, "player2_id": 1, "round": "F"},
    {"user_id": 21, "game_id": 1, "winner_id": 1, "player1_id": 24, "player2_id": 1, "round": "QF"},
    {"user_id": 21, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 56, "round": "QF"},
    {"user_id": 21, "game_id": 3, "winner_id": 64, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 21, "game_id": 4, "winner_id": 121, "player1_id": 121, "player2_id": 99, "round": "QF"},
    {"user_id": 21, "game_id": 5, "winner_id": 32, "player1_id": 32, "player2_id": 1, "round": "SF"},
    {"user_id": 21, "game_id": 6, "winner_id": 121, "player1_id": 121, "player2_id": 91, "round": "SF"},
    {"user_id": 21, "game_id": 7, "winner_id": 121, "player1_id": 121, "player2_id": 32, "round": "F"},
    {"user_id": 22, "game_id": 1, "winner_id": 1, "player1_id": 17, "player2_id": 1, "round": "QF"},
    {"user_id": 22, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 22, "game_id": 3, "winner_id": 91, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 22, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 22, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 22, "game_id": 6, "winner_id": 121, "player1_id": 91, "player2_id": 121, "round": "SF"},
    {"user_id": 22, "game_id": 7, "winner_id": 121, "player1_id": 121, "player2_id": 1, "round": "F"},
    {"user_id": 23, "game_id": 1, "winner_id": 1, "player1_id": 17, "player2_id": 1, "round": "QF"},
    {"user_id": 23, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 23, "game_id": 3, "winner_id": 91, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 23, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 23, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 23, "game_id": 6, "winner_id": 91, "player1_id": 91, "player2_id": 121, "round": "SF"},
    {"user_id": 23, "game_id": 7, "winner_id": 121, "player1_id": 121, "player2_id": 1, "round": "F"},
    {"user_id": 24, "game_id": 1, "winner_id": 1, "player1_id": 29, "player2_id": 1, "round": "QF"},
    {"user_id": 24, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 24, "game_id": 3, "winner_id": 91, "player1_id": 91, "player2_id": 77, "round": "QF"},
    {"user_id": 24, "game_id": 4, "winner_id": 121, "player1_id": 121, "player2_id": 98, "round": "QF"},
    {"user_id": 24, "game_id": 5, "winner_id": 32, "player1_id": 32, "player2_id": 1, "round": "SF"},
    {"user_id": 24, "game_id": 6, "winner_id": 91, "player1_id": 91, "player2_id": 121, "round": "SF"},
    {"user_id": 24, "game_id": 7, "winner_id": 121, "player1_id": 121, "player2_id": 1, "round": "F"},
    {"user_id": 25, "game_id": 1, "winner_id": 1, "player1_id": 17, "player2_id": 1, "round": "QF"},
    {"user_id": 25, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 25, "game_id": 3, "winner_id": 91, "player1_id": 91, "player2_id": 77, "round": "QF"},
    {"user_id": 25, "game_id": 4, "winner_id": 121, "player1_id": 121, "player2_id": 98, "round": "QF"},
    {"user_id": 25, "game_id": 5, "winner_id": 32, "player1_id": 32, "player2_id": 1, "round": "SF"},
    {"user_id": 25, "game_id": 6, "winner_id": 91, "player1_id": 91, "player2_id": 121, "round": "SF"},
    {"user_id": 25, "game_id": 7, "winner_id": 121, "player1_id": 121, "player2_id": 1, "round": "F"},
    {"user_id": 26, "game_id": 1, "winner_id": 1, "player1_id": 17, "player2_id": 1, "round": "QF"},
    {"user_id": 26, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 26, "game_id": 3, "winner_id": 91, "player1_id": 91, "player2_id": 77, "round": "QF"},
    {"user_id": 26, "game_id": 4, "winner_id": 121, "player1_id": 121, "player2_id": 98, "round": "QF"},
    {"user_id": 26, "game_id": 5, "winner_id": 32, "player1_id": 32, "player2_id": 1, "round": "SF"},
    {"user_id": 26, "game_id": 6, "winner_id": 91, "player1_id": 91, "player2_id": 121, "round": "SF"},
    {"user_id": 26, "game_id": 7, "winner_id": 121, "player1_id": 121, "player2_id": 1, "round": "F"},
    {"user_id": 27, "game_id": 1, "winner_id": 1, "player1_id": 31, "player2_id": 1, "round": "QF"},
    {"user_id": 27, "game_id": 2, "winner_id": 48, "player1_id": 48, "player2_id": 32, "round": "QF"},
    {"user_id": 27, "game_id": 3, "winner_id": 91, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 27, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 27, "game_id": 5, "winner_id": 1, "player1_id": 1, "player2_id": 48, "round": "SF"},
    {"user_id": 27, "game_id": 6, "winner_id": 121, "player1_id": 121, "player2_id": 91, "round": "SF"},
    {"user_id": 27, "game_id": 7, "winner_id": 121, "player1_id": 121, "player2_id": 1, "round": "F"},
    {"user_id": 28, "game_id": 1, "winner_id": 1, "player1_id": 31, "player2_id": 1, "round": "QF"},
    {"user_id": 28, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 48, "round": "QF"},
    {"user_id": 28, "game_id": 3, "winner_id": 91, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 28, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 28, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 28, "game_id": 6, "winner_id": 121, "player1_id": 91, "player2_id": 121, "round": "SF"},
    {"user_id": 28, "game_id": 7, "winner_id": 121, "player1_id": 121, "player2_id": 1, "round": "F"},
    {"user_id": 29, "game_id": 1, "winner_id": 1, "player1_id": 17, "player2_id": 1, "round": "QF"},
    {"user_id": 29, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 29, "game_id": 3, "winner_id": 78, "player1_id": 78, "player2_id": 77, "round": "QF"},
    {"user_id": 29, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 29, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 29, "game_id": 6, "winner_id": 78, "player1_id": 78, "player2_id": 121, "round": "SF"},
    {"user_id": 29, "game_id": 7, "winner_id": 32, "player1_id": 32, "player2_id": 78, "round": "F"},
    {"user_id": 30, "game_id": 1, "winner_id": 1, "player1_id": 30, "player2_id": 1, "round": "QF"},
    {"user_id": 30, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 48, "round": "QF"},
    {"user_id": 30, "game_id": 3, "winner_id": 91, "player1_id": 77, "player2_id": 91, "round": "QF"},
    {"user_id": 30, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 30, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 30, "game_id": 6, "winner_id": 121, "player1_id": 121, "player2_id": 91, "round": "SF"},
    {"user_id": 30, "game_id": 7, "winner_id": 121, "player1_id": 121, "player2_id": 1, "round": "F"},
    {"user_id": 31, "game_id": 1, "winner_id": 1, "player1_id": 31, "player2_id": 16, "round": "QF"},
    {"user_id": 31, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 48, "round": "QF"},
    {"user_id": 31, "game_id": 3, "winner_id": 91, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 31, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 31, "game_id": 5, "winner_id": 1, "player1_id": 31, "player2_id": 16, "round": "SF"},
    {"user_id": 31, "game_id": 6, "winner_id": 121, "player1_id": 121, "player2_id": 91, "round": "SF"},
    {"user_id": 31, "game_id": 7, "winner_id": 1, "player1_id": 31, "player2_id": 121, "round": "F"},
    {"user_id": 32, "game_id": 1, "winner_id": 1, "player1_id": 17, "player2_id": 1, "round": "QF"},
    {"user_id": 32, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 63, "round": "QF"},
    {"user_id": 32, "game_id": 3, "winner_id": 91, "player1_id": 64, "player2_id": 91, "round": "QF"},
    {"user_id": 32, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 32, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 32, "game_id": 6, "winner_id": 121, "player1_id": 91, "player2_id": 121, "round": "SF"},
    {"user_id": 32, "game_id": 7, "winner_id": 121, "player1_id": 121, "player2_id": 1, "round": "F"},
    {"user_id": 33, "game_id": 1, "winner_id": 1, "player1_id": 31, "player2_id": 16, "round": "QF"},
    {"user_id": 33, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 48, "round": "QF"},
    {"user_id": 33, "game_id": 3, "winner_id": 78, "player1_id": 78, "player2_id": 77, "round": "QF"},
    {"user_id": 33, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 33, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 33, "game_id": 6, "winner_id": 78, "player1_id": 78, "player2_id": 121, "round": "SF"},
    {"user_id": 33, "game_id": 7, "winner_id": 32, "player1_id": 32, "player2_id": 78, "round": "F"},
    {"user_id": 34, "game_id": 1, "winner_id": 1, "player1_id": 17, "player2_id": 1, "round": "QF"},
    {"user_id": 34, "game_id": 2, "winner_id": 32, "player1_id": 32, "player2_id": 48, "round": "QF"},
    {"user_id": 34, "game_id": 3, "winner_id": 78, "player1_id": 78, "player2_id": 77, "round": "QF"},
    {"user_id": 34, "game_id": 4, "winner_id": 121, "player1_id": 92, "player2_id": 121, "round": "QF"},
    {"user_id": 34, "game_id": 5, "winner_id": 32, "player1_id": 1, "player2_id": 32, "round": "SF"},
    {"user_id": 34, "game_id": 6, "winner_id": 78, "player1_id": 78, "player2_id": 121, "round": "SF"},
    {"user_id": 34, "game_id": 7, "winner_id": 32, "player1_id": 32, "player2_id": 78, "round": "F"},                            

]

def add_picks_to_database(picks_data, tournament_id=1):
    with app.app_context():
        # Suponha que você deseja verificar se a Pick para um determinado jogo já existe, você precisará de uma chave única.
        # Vamos assumir que a combinação de user_id e game_id possa ser essa chave única.
        existing_picks = {(pick.user_id, pick.game_id) for pick in Pick.query.all()}
        
        for pick_info in picks_data:
            # A chave única é uma tupla de user_id e game_id
            unique_key = (pick_info['user_id'], pick_info['game_id'])
            if unique_key not in existing_picks:
                # Atualizando pick_info para incluir tournament_id antes de criar o objeto Game
                pick_info['tournament_id'] = tournament_id
                new_pick = Pick(**pick_info)
                db.session.add(new_pick)
        
        db.session.commit()

if __name__ == '__main__':
    add_picks_to_database(picks_data)
    print("Picks adicionados com sucesso.")  

players_data = [
    {"name": "Novak Djokovic", "country": "SRB", "seed": 1, "qf_number": 1},
    {"name": "Dino PRIZMIC", "country": "CRO", "seed": None, "qf_number": 1},
    {"name": "Alexei Popyrin", "country": "AUS", "seed": None, "qf_number": 1},
    {"name": "Marc Polmans", "country": "AUS", "seed": "WC", "qf_number": 1},
    {"name": "Yannick Hanfmann", "country": "GER", "seed": None, "qf_number": 1},
    {"name": "Gael Monfils", "country": "FRA", "seed": None, "qf_number": 1},
    {"name": "Andy Murray", "country": "GBR", "seed": None, "qf_number": 1},
    {"name": "Tomas Martin Etcheverry", "country": "ARG", "seed": "30", "qf_number": 1},
    {"name": "Adrian Mannarino", "country": "FRA", "seed": "20", "qf_number": 1},
    {"name": "Stan Wawrinka", "country": "SUI", "seed": None, "qf_number": 1},
    {"name": "Alexander Shevchenko", "country": "RUS", "seed": None, "qf_number": 1},
    {"name": "Jaume Munar", "country": "ESP", "seed": None, "qf_number": 1},
    {"name": "Christopher O'Connell", "country": "AUS", "seed": None, "qf_number": 1},
    {"name": "Cristian Garin", "country": "CHI", "seed": None, "qf_number": 1},
    {"name": "Roberto Bautista Agut", "country": "ESP", "seed": None, "qf_number": 1},
    {"name": "Ben Shelton", "country": "USA", "seed": "16", "qf_number": 1},

    {"name": "Taylor Fritz", "country": "USA", "seed": 12, "qf_number": 2},
    {"name": "Facundo Diaz Acosta", "country": "ARG", "seed": None, "qf_number": 2},
    {"name": "Roberto Carballes Baena", "country": "ESP", "seed": None, "qf_number": 2},
    {"name": "Borna Gojo", "country": "CRO", "seed": None, "qf_number": 2},
    {"name": "Fabian Marozsan", "country": "HUN", "seed": None, "qf_number": 2},
    {"name": "Marin Cilic", "country": "CRO", "seed": None, "qf_number": 2},
    {"name": "Francisco Cerundolo", "country": "ARG", "seed": 22, "qf_number": 2},
    {"name": "Lorenzo Musetti", "country": "ITA", "seed": 25, "qf_number": 2},
    {"name": "Lucca Van Assche", "country": "FRA", "seed": None, "qf_number": 2},
    {"name": "James Duckworth", "country": "AUS", "seed": "WC", "qf_number": 2},
    {"name": "Luca Van Assche", "country": "FRA", "seed": None, "qf_number": 2},
    {"name": "Aleksandar Vukic", "country": "AUS", "seed": None, "qf_number": 2},
    {"name": "Jordan Thompson", "country": "AUS", "seed": None, "qf_number": 2},
    {"name": "Matteo Berrettini", "country": "ITA", "seed": None, "qf_number": 2},
    {"name": "Stefanos Tsitsipas", "country": "GRE", "seed": 7, "qf_number": 2},

    {"name": "Jannik Sinner", "country": "ITA", "seed": 4, "qf_number": 3},
    {"name": "Botic van de Zandschulp", "country": "NED", "seed": None, "qf_number": 3},
    {"name": "Pedro Cachin", "country": "ARG", "seed": None, "qf_number": 3},
    {"name": "Jesper DE JONG", "country": "NED", "seed": None, "qf_number": 3},
    {"name": "Daniel Elahi Galan", "country": "COL", "seed": None, "qf_number": 3},
    {"name": "Jason Kubler", "country": "AUS", "seed": "WC", "qf_number": 3},
    {"name": "J.J. Wolf", "country": "USA", "seed": None, "qf_number": 3},
    {"name": "Sebastian Baez", "country": "ARG", "seed": 26, "qf_number": 3},
    {"name": "Frances Tiafoe", "country": "USA", "seed": 17, "qf_number": 3},
    {"name": "Borna Coric", "country": "CRO", "seed": None, "qf_number": 3},
    {"name": "Tomas Machac", "country": "CZE", "seed": None, "qf_number": 3},
    {"name": "Aleksandar KOVACEVIC", "country": "USA", "seed": None, "qf_number": 3},
    {"name": "Alejandro Tabilo", "country": "CHI", "seed": None, "qf_number": 3},
    {"name": "Flavio COBOLLI", "country": "ITA", "seed": None, "qf_number": 3},
    {"name": "Daniel Altmaier", "country": "GER", "seed": None, "qf_number": 3},
    {"name": "Karen Khachanov", "country": "RUS", "seed": 15, "qf_number": 3},

    {"name": "Alex de Minaur", "country": "AUS", "seed": 10, "qf_number": 4},
    {"name": "Milos Raonic", "country": "CAN", "seed": None, "qf_number": 4},
    {"name": "Matteo Arnaldi", "country": "ITA", "seed": None, "qf_number": 4},
    {"name": "Adam Walton", "country": "AUS", "seed": "WC", "qf_number": 4},
    {"name": "Pavel Kotov", "country": "RUS", "seed": None, "qf_number": 4},
    {"name": "Arthur Rinderknech", "country": "FRA", "seed": None, "qf_number": 4},
    {"name": "Flavio COBOLLI,", "country": "ITA", "seed": None, "qf_number": 4},
    {"name": "Nicolas Jarry", "country": "CHI", "seed": 18, "qf_number": 4},
    {"name": "Sebastian Korda", "country": "USA", "seed": 29, "qf_number": 4},
    {"name": "HALYS, Quentin", "country": "FRA", "seed": None, "qf_number": 4},
    {"name": "Vit KOPRIVA", "country": "CZE", "seed": None, "qf_number": 4},
    {"name": "HARRIS, Lloyd", "country": "RSA", "seed": None, "qf_number": 4},
    {"name": "Christopher Eubanks", "country": "USA", "seed": None, "qf_number": 4},
    {"name": "Taro Daniel", "country": "JPN", "seed": None, "qf_number": 4},
    {"name": "Thiago Seyboth Wild", "country": "BRA", "seed": None, "qf_number": 4},
    {"name": "Andrey Rublev", "country": "RUS", "seed": 5, "qf_number": 4},

    {"name": "Holger Rune", "country": "DEN", "seed": 8, "qf_number": 5},
    {"name": "Yoshihito Nishioka", "country": "JPN", "seed": None, "qf_number": 5},
    {"name": "Laslo Djere", "country": "SRB", "seed": None, "qf_number": 5},
    {"name": "Arthur Cazaux", "country": "FRA", "seed": "WC", "qf_number": 5},
    {"name": "Arthur Fils", "country": "FRA", "seed": None, "qf_number": 5},
    {"name": "Jiri Vesely", "country": "CZE", "seed": None, "qf_number": 5},
    {"name": "Roman Safiullin", "country": "RUS", "seed": None, "qf_number": 5},
    {"name": "Tallon Griekspoor", "country": "NED", "seed": 28, "qf_number": 5},
    {"name": "Ugo Humbert", "country": "FRA", "seed": 21, "qf_number": 5},
    {"name": "GOFFIN, David", "country": "BEL", "seed": None, "qf_number": 5},
    {"name": "Zhizhen Zhang", "country": "CHN", "seed": None, "qf_number": 5},
    {"name": "Federico Coria", "country": "ARG", "seed": None, "qf_number": 5},
    {"name": "Denis Shapovalov", "country": "CAN", "seed": None, "qf_number": 5},
    {"name": "Hubert Hurkacz", "country": "POL", "seed": 9, "qf_number": 5},

    {"name": "Grigor Dimitrov", "country": "BUL", "seed": 13, "qf_number": 6},
    {"name": "Marton Fucsovics", "country": "HUN", "seed": None, "qf_number": 6},
    {"name": "Sebastian Ofner", "country": "AUT", "seed": None, "qf_number": 6},
    {"name": "Thanasi Kokkinakis", "country": "AUS", "seed": None, "qf_number": 6},
    {"name": "Maximilian Marterer", "country": "GER", "seed": None, "qf_number": 6},
    {"name": "Nuno Borges", "country": "POR", "seed": None, "qf_number": 6},
    {"name": "Constant Lestienne", "country": "FRA", "seed": None, "qf_number": 6},
    {"name": "Alejandro Davidovich Fokina", "country": "ESP", "seed": 23, "qf_number": 6},
    {"name": "Felix Auger-Aliassime", "country": "CAN", "seed": 27, "qf_number": 6},
    {"name": "Dominic Thiem", "country": "AUT", "seed": None, "qf_number": 6},
    {"name": "Alexandre Muller", "country": "FRA", "seed": None, "qf_number": 6},
    {"name": "Q", "country": None, "seed": None, "qf_number": 6},
    {"name": "Emil Ruusuvuori", "country": "FIN", "seed": None, "qf_number": 6},
    {"name": "Daniil Medvedev", "country": "RUS", "seed": 3, "qf_number": 6},

    {"name": "Alexander Zverev", "country": "GER", "seed": 6, "qf_number": 7},
    {"name": "Dominik Koepfer", "country": "GER", "seed": None, "qf_number": 7},
    {"name": "Soonwoo Kwon", "country": "KOR", "seed": None, "qf_number": 7},
    {"name": "James McCabe", "country": "AUS", "seed": "WC", "qf_number": 7},
    {"name": "Alex Michelsen", "country": "USA", "seed": None, "qf_number": 7},
    {"name": "Bernabe Zapata Miralles", "country": "ESP", "seed": None, "qf_number": 7},
    {"name": "Jiri Lehecka", "country": "CZE", "seed": 32, "qf_number": 7},
    {"name": "Cameron Norrie", "country": "GBR", "seed": 19, "qf_number": 7},
    {"name": "Juan Pablo Varillas", "country": "PER", "seed": None, "qf_number": 7},
    {"name": "Dusan Lajovic", "country": "SRB", "seed": None, "qf_number": 7},
    {"name": "ZEPPIERI, Giulio", "country": "ITA", "seed": None, "qf_number": 7},
    {"name": "Max Purcell", "country": "AUS", "seed": None, "qf_number": 7},
    {"name": "Albert Ramos-Vinolas", "country": "ESP", "seed": None, "qf_number": 7},
    {"name": "Casper Ruud", "country": "NOR", "seed": 11, "qf_number": 7},

    {"name": "Tommy Paul", "country": "USA", "seed": 14, "qf_number": 8},
    {"name": "Gregoire Barrere", "country": "FRA", "seed": None, "qf_number": 8},
    {"name": "Marcos Giron", "country": "USA", "seed": None, "qf_number": 8},
    {"name": "Jack Draper", "country": "GBR", "seed": None, "qf_number": 8},
    {"name": "Miomir Kecmanovic", "country": "SRB", "seed": None, "qf_number": 8},
    {"name": "Yosuke Watanuki", "country": "JPN", "seed": None, "qf_number": 8},
    {"name": "Rinky Hijikata", "country": "AUS", "seed": None, "qf_number": 8},
    {"name": "Jan-Lennard Struff", "country": "GER", "seed": 24, "qf_number": 8},
    {"name": "Alexander Bublik", "country": "KAZ", "seed": 31, "qf_number": 8},
    {"name": "NAGAL, Sumit", "country": "IND", "seed": None, "qf_number": 8},
    {"name": "Mackenzie McDonald", "country": "USA", "seed": None, "qf_number": 8},
    {"name": "Juncheng Shang", "country": "CHN", "seed": "WC", "qf_number": 8},
    {"name": "Daniel Evans", "country": "GBR", "seed": None, "qf_number": 8},
    {"name": "Lorenzo Sonego", "country": "ITA", "seed": None, "qf_number": 8},
    {"name": "Richard Gasquet", "country": "FRA", "seed": None, "qf_number": 8},
    {"name": "Carlos Alcaraz", "country": "ESP", "seed": 2, "qf_number": 8}

]

def add_players_to_database(players_data, tournament_id=1):
    with app.app_context():
        # Verifica se os jogadores já existem para evitar duplicatas
        existing_players = {player.name for player in Player.query.all()}
        
        for player_info in players_data:
            # A chave única aqui é assumida como o nome do jogador
            if player_info['name'] not in existing_players:
                # Atualizando player_info para incluir tournament_id antes de criar o objeto Player
                player_info['tournament_id'] = tournament_id
                new_player = Player(**player_info)
                db.session.add(new_player)
        
        db.session.commit()

if __name__ == '__main__':
    add_players_to_database(players_data)
    print("Picks adicionados com sucesso.")  

tournament_data = [{"name": "Australian Open", "short_name": "AO", "year": 2024, "status": "open"}]

def add_tournaments_to_database(tournament_data):
    with app.app_context():
        existing_tournaments = {tournament.name for tournament in Tournament.query.all()}

        for tournament_info in tournament_data:
            if tournament_info['name'] not in existing_tournaments:
                new_tournament = Tournament(**tournament_info)
                db.session.add(new_tournament)

        db.session.commit()

if __name__ == '__main__':
    add_tournaments_to_database(tournament_data)
    print("Torneios adicionados com sucesso.")     