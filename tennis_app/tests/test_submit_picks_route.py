# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# import pytest
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from tennis_app import app as flask_app
# from tennis_app.models import User, Tournament, db  # Ajuste os caminhos de importação conforme necessário
import requests
import json

# Defina o endereço do servidor (ajuste conforme necessário)
server_url = "http://localhost:5000"

# Dados de teste
tournament_data = {
    "short_name": "AO",
    "year": 2024
}

# Substitua 'your_test_user_id' pelo ID do usuário de teste
pick_data = {
    "user_id": your_test_user_id,
    # Adicione mais dados conforme a estrutura esperada pela sua aplicação
}

# Defina os casos de teste
test_cases = [
    ("/submit_picks_tournaments/WrongName/2024", pick_data, "Torneio não encontrado"),
    ("/submit_picks_tournaments/OT/2024", {}, "No data provided"),
    ("/submit_picks_tournaments/OT/2024", {"user_id": 9999}, "User not found"),
    ("/submit_picks_tournaments/OT/2024", pick_data, "Picks submitted successfully")
]

# Execução dos testes
for endpoint, data, expected_msg in test_cases:
    full_url = f"{server_url}{endpoint}"
    response = requests.post(full_url, json=data)
    assert expected_msg in response.json()["error"] or response.json()["message"]

print("Todos os testes foram executados com sucesso.")






# # Ignorar avisos de depreciação
# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# @pytest.fixture
# def client():
#     flask_app.config.update({
#         'TESTING': True,
#         'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
#     })
#     with flask_app.app_context():
#         db.create_all()

#     yield flask_app.test_client()

#     with flask_app.app_context():
#         db.session.remove()
#         db.drop_all()

# @pytest.fixture
# def prepare_data():
#     with flask_app.app_context():
#         # Assegure que 'email' e 'password_hash' tenham valores válidos e não None
#         user = User(id=1, username="testuser", email="testuser@example.com", password_hash="hashed_password")
#         # Supondo que você tenha um torneio para adicionar também
#         tournament = Tournament(name="Open Tournament", short_name="OT", year=2024, status="Scheduled")
#         db.session.add(user)
#         db.session.add(tournament)
#         db.session.commit()



# # 1. Torneio Não Encontrado
# def test_tournament_not_found(client, prepare_data):
#     response = client.post('/submit_picks_tournaments/WrongName/2024', json={'user_id': 1})
#     assert response.status_code == 404
#     assert 'Torneio não encontrado' in response.get_json()['error']


# # 2. Dados da Requisição Ausentes
# def test_no_data_provided(client, prepare_data):
#     response = client.post('/api/submit_picks_tournaments/OT/2024')
#     assert response.status_code == 400
#     assert 'No data provided' in response.get_json()['error']

# # 3. Usuário Não Encontrado
# def test_user_not_found(client, prepare_data):
#     response = client.post('/api/submit_picks_tournaments/OT/2024', json={'user_id': 999})
#     assert response.status_code == 404
#     assert 'User not found' in response.get_json()['error']

# # 4. Processamento bem-sucedido
# def test_submit_picks_success(client, prepare_data):
#     data = {'user_id': 1, 'picks': [...]}  # Substitua [...] pelos dados reais de teste
#     response = client.post('/api/submit_picks_tournaments/OT/2024', json=data)
#     assert response.status_code == 200
#     assert 'Picks submitted successfully' in response.get_json()['message']
#     # Aqui você também pode verificar se os jogos e picks foram criados corretamente.

# # 5. Falha no Processamento
# # Este teste é mais complexo, pois depende de como você implementou `session_scope()`,
# # `delete_existing_games()`, `create_all_games()`, e `create_or_update_picks()`.
# # Você precisaria mockar uma dessas funções para lançar uma exceção e então verificar
# # se a resposta é 500. Isso pode exigir um pouco mais de setup dependendo do seu projeto.


# pytest -s test_submit_picks_route.py