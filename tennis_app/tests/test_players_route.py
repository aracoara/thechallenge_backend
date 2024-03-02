# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# from tennis_app import app as flask_app
# from tennis_app.extensions import db
# from tennis_app.models import Player, Tournament
# import pytest
# import logging
# import warnings

# warnings.filterwarnings("ignore", category=DeprecationWarning)

# # Configura o logging globalmente no nível do módulo
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# @pytest.fixture
# def client():
#     flask_app.config.update({
#         'TESTING': True,
#         'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
#     })
#     client = flask_app.test_client()

#     with flask_app.app_context():
#         db.create_all()
#         add_sample_tournament()
#         add_sample_players()
#         yield client
#         db.session.remove()
#         db.drop_all()

# def add_sample_tournament():
#     tournament = Tournament(name="Open Tournament", short_name="OT", year=2024, status="Scheduled")
#     db.session.add(tournament)
#     db.session.commit()

# def add_sample_players():
#     tournament = Tournament.query.filter_by(short_name="OT", year=2024).first()
#     players = [
#         Player(name="Player 1", country="USA", seed=1, qf_number=5, tournament_id=tournament.id),
#         Player(name="Player 2", country="GBR", seed=2, qf_number=1, tournament_id=tournament.id)
#     ]
#     db.session.bulk_save_objects(players)
#     db.session.commit()

# def test_get_players_by_tournament_success(client):
#     # Realiza a requisição GET para a rota /players com short_name e year válidos
#     response = client.get('/players/OT/2024')
#     logger.debug("Requisição GET para /players/OT/2024 realizada.")

#     # Verifica se o status code é 200
#     assert response.status_code == 200
#     logger.debug("Status code 200 confirmado.")

#     # Converte os dados retornados para JSON
#     actual_data = response.get_json()

#     # Extrai apenas os nomes dos jogadores dos dados reais para comparação
#     actual_names = [player['name'] for player in actual_data]

#     # Define os nomes esperados dos jogadores baseados nos dados adicionados no setup do teste
#     expected_names = ["Player 1", "Player 2"]

#     # Verifica se os nomes dos jogadores reais correspondem aos esperados
#     assert set(actual_names) == set(expected_names)
#     logger.debug("Nomes dos jogadores verificados com sucesso.")




# pytest -s test_players_route.py