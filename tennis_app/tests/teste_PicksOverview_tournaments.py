from tennis_app.utils import get_and_process_picks
import json
from flask import jsonify
from tennis_app.models import User, Player, Tournament, Pick
from tennis_app import app
from tennis_app.extensions import db
import pandas as pd

@app.route('/PicksOverview/<short_name>/<int:year>', methods=['GET'])
def get_picks_overview_tournament(short_name, year):
    # Encontra o torneio com base no short_name e no ano
    tournament = Tournament.query.filter_by(short_name=short_name, year=year).first()
    if not tournament:
        return jsonify({'error': 'Torneio não encontrado'}), 404

    # Busca todos os palpites para o torneio selecionado
    picks = Pick.query.filter_by(tournament_id=tournament.id).all()

    # Lista para armazenar os palpites processados
    processed_picks_list = []

    # Itera sobre os palpites para construir a resposta
    for pick in picks:
        user = User.query.get(pick.user_id)
        player1 = Player.query.get(pick.player1_id)
        player2 = Player.query.get(pick.player2_id)
        winner = Player.query.get(pick.winner_id)

        # Estrutura para armazenar os dados de um palpite
        pick_data = {
            'User': user.username if user else 'Unknown',
            'TournamentId': tournament.id,
            'QF1': player1.name if player1 and pick.round == 'QF' and pick.game_id == 1 else None,
            'QF2': player2.name if player2 and pick.round == 'QF' and pick.game_id == 2 else None,
            # Adicione entradas semelhantes para outros quartos de final, semifinais e finais
            'Champion': winner.name if winner and pick.round == 'F' else None
        }

        processed_picks_list.append(pick_data)

    # Cria um DataFrame com os dados processados
    df_picks = pd.DataFrame(processed_picks_list)
    # Converte o DataFrame em um JSON
    picks_json = df_picks.to_json(orient='records')

    return jsonify(picks_json)