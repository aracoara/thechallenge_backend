from tennis_app import app
from tennis_app.models import Pick, Tournament
from sqlalchemy.orm import joinedload
import pandas as pd

short_name = "IW"
year = 2024

with app.app_context():
    tournament = Tournament.query.filter_by(short_name=short_name, year=year).first()

    if tournament:
        picks = Pick.query.filter_by(tournament_id=tournament.id) \
                            .options(joinedload(Pick.game)) \
                            .all()

        # Função para transformar a posição para apenas QF, SF, F, Champion
        def transform_position(position):
            if 'QF' in position:
                return 'QF'
            elif 'SF' in position:
                return 'SF'
            elif 'F' in position:
                return 'F'
            elif 'Champion' in position:
                return 'Champion'
            return position  # Caso padrão, retorna a posição como está

        picks_data = [{
            "user_id": pick.user_id,
            "Jogador": pick.player_id,
            "Rodada": transform_position(pick.position),  # Aplica a transformação aqui
            "tournament_id": pick.tournament_id
        } for pick in picks]

        df_picks = pd.DataFrame(picks_data)

        df_picks_por_usuario_temp = df_picks.copy()
        df_picks_por_usuario = df_picks_por_usuario_temp.drop_duplicates()

        ordem_rodadas = {"QF": 1, "SF": 2, "F": 3, "Champion": 4}
        df_picks_por_usuario['OrdemRodada'] = df_picks_por_usuario['Rodada'].map(ordem_rodadas)
        
        df_picks_por_usuario.sort_values(by=['user_id', 'tournament_id', 'OrdemRodada', 'Jogador'], inplace=True)
        df_picks_por_usuario.drop('OrdemRodada', axis=1, inplace=True)

        print(df_picks_por_usuario)
    else:
        print("Tournament not found.")
