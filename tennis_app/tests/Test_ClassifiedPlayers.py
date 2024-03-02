
from tennis_app.models import Tournament, Player
from tennis_app import app
from tennis_app.extensions import db
import pandas as pd
# from json import jsonify    
from tennis_app.utils import ResultsPositionTournament


with app.app_context():
    file_paths = {
            'AO': {
                2024: {
                    "R1": 'tennis_app/assets/AO24/AO-24-Results - R1.csv',
                    "R2": 'tennis_app/assets/AO24/AO-24-Results - R2.csv',
                    "R3": 'tennis_app/assets/AO24/AO-24-Results - R3.csv',
                    "R4": 'tennis_app/assets/AO24/AO-24-Results - R4.csv',
                    "QF": 'tennis_app/assets/AO24/AO-24-Results - QF.csv',
                    "SF": 'tennis_app/assets/AO24/AO-24-Results - SF.csv',
                    "F": 'tennis_app/assets/AO24/AO-24-Results - F.csv',
                    "Champion": 'tennis_app/assets/AO24/AO-24-Results - Champion.csv',
                }
            },
            'RIO': {
                2024: {
                    "R1": 'tennis_app/assets/RIO24/RIO-24-Results - R1.csv',
                    "R2": 'tennis_app/assets/RIO24/RIO-24-Results - R2.csv',
                    "R3": 'tennis_app/assets/RIO24/RIO-24-Results - R3.csv',
                    "R4": 'tennis_app/assets/RIO24/RIO-24-Results - R4.csv',
                    "QF": 'tennis_app/assets/RIO24/RIO-24-Results - QF.csv',
                    "SF": 'tennis_app/assets/RIO24/RIO-24-Results - SF.csv',
                    "F": 'tennis_app/assets/RIO24/RIO-24-Results - F.csv',
                    "Champion": 'tennis_app/assets/RIO24/RIO-24-Results - Champion.csv',
                }
            }
        }
    
    short_name = 'AO'
    year = 2024
    paths = file_paths[short_name][year]
    file_path_QF = paths['QF']


    # # # file_path = file_paths['QF']
    df_classified_players_QF = ResultsPositionTournament(paths['QF'], short_name, year)
    df_classified_players_SF = ResultsPositionTournament(paths['SF'], short_name, year)
    df_classified_players_F = ResultsPositionTournament(paths['F'], short_name, year)
    df_classified_players_Champion = ResultsPositionTournament(paths['Champion'], short_name, year)
    # Concatenar os DataFrames
    frames = [df_classified_players_QF, df_classified_players_SF, df_classified_players_F, df_classified_players_Champion]
    df_concatenated = pd.concat(frames)
    result_dict = df_concatenated.to_dict(orient='records')


    print(result_dict)


# if short_name in torneios and year in torneios[short_name]:
#     etapas_torneio = torneios[short_name][year]
# # Obtenção das informações do torneio
# tournament = Tournament.query.filter_by(short_name=short_name, year=year).first()
# df = pd.read_csv(file_paths['QF'], encoding='ISO-8859-1', skiprows=1, names=['Position', 'Player'])
# player_id_map = {player.name: player.id for player in Player.query.filter_by(tournament_id=tournament.id).all()}
# df['Player'] = df['Player'].astype(str)
# df['player_id'] = df['Player'].str.extract(r'^(.*?)\s+\(')[0].map(player_id_map)
# df.dropna(subset=['player_id'], inplace=True)
# df['player_id'] = pd.to_numeric(df['player_id'], downcast='integer', errors='coerce')
# print(df)






    # df_classified_players_QF = process_results_data_position(file_paths['QF'])
    # print(df_classified_players_QF)
    # # df = pd.read_csv('tennis_app/assets/RIO24/RIO-24-Results - QF.csv', encoding='ISO-8859-1', skiprows=1, names=['Position', 'Player'])
    # print(df)


# updates_response_list = []
# for etapa, player_ids in RoundUpdates:
#     # Criação do dicionário para cada atualização de rodada
#     update_dict = {
#         'rodada': etapa,
#         'player_ids': list(player_ids),  # Convertendo set para lista para ser serializável em JSON
#         'tournament_id': tournament.id
#     }
#     updates_response_list.append(update_dict)