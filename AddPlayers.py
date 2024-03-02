
from tennis_app.models import Tournament, Player
from tennis_app import app
from tennis_app.extensions import db

def add_or_update_players(players_data, tournament_short_name, tournament_year):
    with app.app_context():
        # Encontrar o torneio pelo short_name e year
        tournament = Tournament.query.filter_by(short_name=tournament_short_name, year=tournament_year).first()
        if not tournament:
            print("Torneio não encontrado.")
            return

        tournament_id = tournament.id

        for player_info in players_data:
            player_info['tournament_id'] = tournament_id  # Adiciona tournament_id aos dados do jogador
            existing_player = Player.query.filter_by(name=player_info['name'], tournament_id=tournament_id).first()
            
            if existing_player:
                # Atualiza os dados do jogador existente
                existing_player.country = player_info['country']
                existing_player.seed = player_info.get('seed')
                existing_player.qf_number = player_info.get('qf_number')
            else:
                # Cria um novo registro de jogador
                try:
                    new_player = Player(**player_info)
                    db.session.add(new_player)
                except Exception as e:
                    print(f"Erro ao adicionar jogador {player_info['name']}: {e}")
                    db.session.rollback()
                    continue

        # Salva as alterações no banco de dados
        try:
            db.session.commit()
            print("Jogadores adicionados ou atualizados com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar jogadores no banco de dados: {e}")
            db.session.rollback()

# def add_players_to_database(players_data, tournament_short_name, tournament_year):
#     with app.app_context():
#         # Encontrar o torneio pelo short_name e year
#         tournament = Tournament.query.filter_by(short_name=tournament_short_name, year=tournament_year).first()
#         if not tournament:
#             print("Torneio não encontrado.")
#             return
        
#         tournament_id = tournament.id

#         # Verifica se os jogadores já existem para o torneio filtrado para evitar duplicatas
#         existing_players = {(player.name, player.tournament_id) for player in Player.query.filter_by(tournament_id=tournament_id)}

#         for player_info in players_data:
#             # Verifica se o nome do jogador e o tournament_id já existem no conjunto de jogadores existentes
#             if (player_info['name'], tournament_id) not in existing_players:
#                 player_info['tournament_id'] = tournament_id  # Adiciona tournament_id aos dados do jogador
#                 try:
#                     new_player = Player(**player_info)
#                     db.session.add(new_player)
#                 except Exception as e:
#                     print(f"Erro ao adicionar jogador {player_info['name']}: {e}")
#                     db.session.rollback()
#                     continue

#         try:
#             db.session.commit()
#         except Exception as e:
#             print(f"Erro ao salvar jogadores no banco de dados: {e}")
#             db.session.rollback()

# Exemplo de uso
players_info = [
    {"name": "Carlos Alcaraz", "country": "ESP", "seed": 1, "qf_number": 1},
    {"name": "Thiago Monteiro", "country": "BRA", "seed": "WC", "qf_number": 1},
    {"name": "Felipe Meligeni Alves", "country": "BRA", "seed": "Q", "qf_number": 1},
    {"name": "Pedro Cachin", "country": "ARG", "seed": None, "qf_number": 1},

    {"name": "Facundo Diaz Acosta", "country": "ARG", "seed": None, "qf_number": 2},
    {"name": "Stan Wawrinka", "country": "SUI", "seed": None, "qf_number": 2},
    {"name": "Corentin Moutet", "country": "FRA", "seed": "Q", "qf_number": 2},
    {"name": "Sebastian Baez", "country": "ARG", "seed": 5, "qf_number": 2},

    {"name": "Francisco Cerundolo", "country": "ARG", "seed": 4, "qf_number": 3},
    {"name": "Francisco Comesana", "country": "ARG", "seed": "Q", "qf_number": 3},
    {"name": "Juan Pablo Varillas", "country": "PER", "seed": None, "qf_number": 3},
    {"name": "Albert Ramos-Vinolas", "country": "ESP", "seed": None, "qf_number": 3},
    
    {"name": "Dusan Lajovic", "country": "SRB", "seed": None, "qf_number": 4},
    {"name": "Daniel Elahi Galan", "country": "COL", "seed": None, "qf_number": 4},
    {"name": "Bernabe Zapata Miralles", "country": "ESP", "seed": None, "qf_number": 4},
    {"name": "Laslo Djere", "country": "SRB", "seed": 6, "qf_number": 4},

    {"name": "Arthur Fils", "country": "FRA", "seed": 7, "qf_number": 5},
    {"name": "Joao Fonseca", "country": "BRA", "seed": "WC", "qf_number": 5},
    {"name": "Roberto Carballes Baena", "country": "ESP", "seed": None, "qf_number": 5},
    {"name": "Cristian Garin", "country": "CHI", "seed": None, "qf_number": 5},

    {"name": "Federico Coria", "country": "ARG", "seed": None, "qf_number": 6},
    {"name": "Mariano Navone", "country": "ARG", "seed": "Q", "qf_number": 6},
    {"name": "Yannick Hanfmann", "country": "GER", "seed": None, "qf_number": 6},
    {"name": "Nicolas Jarry", "country": "CHI", "seed": 3, "qf_number": 6},

    {"name": "Sebastian Ofner", "country": "AUT", "seed": 8, "qf_number": 7},
    {"name": "Jaume Munar", "country": "ESP", "seed": None, "qf_number": 7},
    {"name": "Alejandro Tabilo", "country": "CHI", "seed": None, "qf_number": 7},
    {"name": "Thiago Seyboth Wild", "country": "BRA", "seed": None, "qf_number": 7},

    {"name": "Gustavo Heide", "country": "BRA", "seed": "WC", "qf_number": 8},
    {"name": "Tomas Barrios Vera", "country": "CHI", "seed": None, "qf_number": 8},
    {"name": "Hugo Dellien", "country": "BOL", "seed": None, "qf_number": 8},
    {"name": "Cameron Norrie", "country": "GBR", "seed": 2, "qf_number": 8}
]


if __name__ == '__main__':
    ## Adicionando jogadores ao banco de dados
    add_or_update_players(players_info, "RIO", 2024)
    print("Jogadores adicionados com sucesso.")

# from tennis_app.models import Tournament, Player
# from tennis_app import app
# from tennis_app.extensions import db

# players_info = [
#                 {"name": "Carlos Alcaraz", "country": "ESP", "seed": 1, "qf_number": 1},
#                 {"name": "Thiago Monteiro", "country": "BRA", "seed": "WC", "qf_number": 1},
#                 {"name": "Felipe Meligeni Alves", "country": "BRA", "seed": "Q", "qf_number": 1},
#                 {"name": "Pedro Cachin", "country": "ARG", "seed": None, "qf_number": 1},
#                 {"name": "Facundo Diaz Acosta", "country": "ARG", "seed": None, "qf_number": 1},
#                 {"name": "Stan Wawrinka", "country": "SUI", "seed": None, "qf_number": 1},
#                 {"name": "Corentin Moutet", "country": "FRA", "seed": "Q", "qf_number": 1},
#                 {"name": "Sebastian Baez", "country": "ARG", "seed": 5, "qf_number": 1},

#                 {"name": "Francisco Cerundolo", "country": "ARG", "seed": 4, "qf_number": 2},
#                 {"name": "Francisco Comesana", "country": "ARG", "seed": "Q"},
#                 {"name": "Juan Pablo Varillas", "country": "PER", "seed": None},
#                 {"name": "Albert Ramos-Vinolas", "country": "ESP", "seed": None},
#                 {"name": "Dusan Lajovic", "country": "SRB", "seed": None},
#                 {"name": "Daniel Elahi Galan", "country": "COL", "seed": None},
#                 {"name": "Bernabe Zapata Miralles", "country": "ESP", "seed": None},
#                 {"name": "Laslo Djere", "country": "SRB", "seed": 6, "qf_number": 2},

#                 {"name": "Arthur Fils", "country": "FRA", "seed": 7, "qf_number": 3},
#                 {"name": "Joao Fonseca", "country": "BRA", "seed": "WC", "qf_number": 3},
#                 {"name": "Roberto Carballes Baena", "country": "ESP", "seed": None, "qf_number": 3},
#                 {"name": "Cristian Garin", "country": "CHI", "seed": None, "qf_number": 3},
#                 {"name": "Federico Coria", "country": "ARG", "seed": None, "qf_number": 3},
#                 {"name": "Mariano Navone", "country": "ARG", "seed": "Q", "qf_number": 3},
#                 {"name": "Yannick Hanfmann", "country": "GER", "seed": None, "qf_number": 3},
#                 {"name": "Nicolas Jarry", "country": "CHI", "seed": 3, "qf_number": 3},

#                 {"name": "Sebastian Ofner", "country": "AUT", "seed": 8, "qf_number": 4},
#                 {"name": "Jaume Munar", "country": "ESP", "seed": None, "qf_number": 4},
#                 {"name": "Alejandro Tabilo", "country": "CHI", "seed": None, "qf_number": 4},
#                 {"name": "Thiago Seyboth Wild", "country": "BRA", "seed": None, "qf_number": 4},
#                 {"name": "Gustavo Heide", "country": "BRA", "seed": "WC", "qf_number": 4},
#                 {"name": "Tomas Barrios Vera", "country": "CHI", "seed": None, "qf_number": 4},
#                 {"name": "Hugo Dellien", "country": "BOL", "seed": None, "qf_number": 4},
#                 {"name": "Cameron Norrie", "country": "GBR", "seed": 2, "qf_number": 4}
#             ]

# def add_players_to_database(players_data, tournament_id):
#     with app.app_context():
#         # Verifica se os jogadores já existem para o torneio filtrado para evitar duplicatas
#         existing_players = {player.name for player in Player.query.all()}
        
#         for player_info in players_data:
#             # A chave única aqui é assumida como o nome do jogador
#             if player_info['name'] not in existing_players:
#                 # Atualizando player_info para incluir tournament_id antes de criar o objeto Player
#                 player_info['tournament_id'] = tournament_id
#                 new_player = Player(**player_info)
#                 db.session.add(new_player)
        
#         db.session.commit()      

# tournament_id = Tournament.id.query.filter_by(short_name="RIO", year=2024).first()

