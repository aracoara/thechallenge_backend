import pandas as pd
from io import StringIO
from tennis_app.utils import (gatherFormattedTournamentPicks, trackTournamentEliminations, compileValidTournamentPicks, 
                              process_and_update_rounds, get_user_data)
from tennis_app.models import Tournament, User, Pick
from tennis_app import app


def calculate_points(validTournamentPicks_df, RoundUpdates, weights):
    # Determinar a última rodada atualizada a partir de RoundUpdates
    latest_round = RoundUpdates[-1][0]
    
    # Definir a ordem das rodadas para uso no cálculo do índice, baseando-se nas chaves do dicionário de pesos
    round_order = ["QF", "SF", "F", "Champion"]
    
    # Verificar se latest_round está na ordem definida; se não, retornar DataFrame vazio
    if latest_round not in weights:
        return pd.DataFrame()
    
    # Calcular os pontos baseando-se na ordem das rodadas e nos pesos definidos
    validTournamentPicks_df['Earned_Points'] = validTournamentPicks_df['Rodada'].apply(lambda x: weights[x] if round_order.index(x) <= round_order.index(latest_round) else 0)
    
    # Agrupar os pontos por usuário e torneio, e somar os pontos
    df_earned_points_summed = validTournamentPicks_df.groupby(['user_id', 'tournament_id'], as_index=False)['Earned_Points'].sum()
    
    # Obter os dados do usuário
    user_data_df = get_user_data()
    
    # Mesclar os pontos calculados com os nomes dos usuários
    df_earned_points_with_names = pd.merge(df_earned_points_summed, user_data_df, on='user_id')
    df_earned_points_with_names.rename(columns={'username': 'Participante', 'Earned_Points': 'Pontos Ganhos'}, inplace=True)
    
    # Adicionar a coluna da última rodada atualizada
    df_earned_points_with_names['Rodada'] = latest_round
    
    # Calcular o ranking de pontos ganhos por torneio
    df_earned_points_with_names['Ranking PG'] = df_earned_points_with_names.groupby('tournament_id')['Pontos Ganhos'].rank(ascending=False, method='min')
    
    # Organizar e preparar o DataFrame final
    df_earned_points_with_names.sort_values(by=['tournament_id', 'Pontos Ganhos'], ascending=[True, False], inplace=True)
    df_earned_points_with_names.reset_index(drop=True, inplace=True)
    
    # Selecionar e reordenar as colunas para o output final
    df_earned_points_final = df_earned_points_with_names[['Ranking PG', 'Participante', 'Pontos Ganhos', 'tournament_id', 'Rodada']].copy()
    
    return df_earned_points_final



# Exemplo de uso

etapas_torneio = {
    ## RIO 2024
    # "R1": 'tennis_app/assets/RIO24/RIO-24-Results - R1.csv',
    # "R2": 'tennis_app/assets/RIO24/RIO-24-Results - R2.csv',
    # "R3": 'tennis_app/assets/RIO24/RIO-24-Results - R3.csv',
    # "R4": 'tennis_app/assets/RIO24/RIO-24-Results - R4.csv',
    # "QF": 'tennis_app/assets/RIO24/RIO-24-Results - QF.csv',
    # "SF": 'tennis_app/assets/RIO24/RIO-24-Results - SF.csv',
    # "F": 'tennis_app/assets/RIO24/RIO-24-Results - F.csv',
    # "Champion": 'tennis_app/assets/RIO24/RIO-24-Results - Champion.csv',

    ## AO 2024
    "R1": 'tennis_app/assets/AO24/AO-24-Results - R1.csv',
    "R2": 'tennis_app/assets/AO24/AO-24-Results - R2.csv',
    "R3": 'tennis_app/assets/AO24/AO-24-Results - R3.csv',
    "R4": 'tennis_app/assets/AO24/AO-24-Results - R4.csv',
    "QF": 'tennis_app/assets/AO24/AO-24-Results - QF.csv',
    "SF": 'tennis_app/assets/AO24/AO-24-Results - SF.csv',
    # "F": 'tennis_app/assets/AO24/AO-24-Results - F.csv',
    # "Champion": 'tennis_app/assets/AO24/AO-24-Results - Champion.csv',    
}

RoundUpdates = process_and_update_rounds(etapas_torneio)
# print(RoundUpdates)



tournament_short_name = 'AO'
tournament_year = 2024
TournamentPicks_df = gatherFormattedTournamentPicks(tournament_short_name, tournament_year)
TournamentEliminations_df = trackTournamentEliminations(TournamentPicks_df, RoundUpdates)
ValidTournamentsPicks_df = compileValidTournamentPicks(TournamentPicks_df, TournamentEliminations_df, RoundUpdates)
# print(ValidTournamentsPicks_df)   


weights = {"QF": 1, "SF": 2, "F": 3, "Champion": 4}

## Assumindo que roundUpdates é a lista de atualizações de rodada fornecida
total_earned_points = calculate_points(ValidTournamentsPicks_df, RoundUpdates, weights)
print(f"Total de pontos: {total_earned_points}")


# tournament_short_name = 'AO'
# tournament_year = 2024

# with app.app_context():
#     # Busca o torneio pelo nome e ano
#     tournament = Tournament.query.filter_by(short_name=tournament_short_name, year=tournament_year).first()
#     if not tournament:
#         raise ValueError("Torneio não encontrado.")

#     # Busca todos os usuários associados ao torneio selecionado através de suas escolhas (picks)
#     users_in_tournament = User.query.join(Pick).filter(Pick.tournament_id == tournament.id).distinct()

#     user_data = [
#         {
#             "user_id": user.id,
#             "username": user.username,
#             "tournament_id": tournament.id
#         }
#         for user in users_in_tournament
#     ]

#     # Cria DataFrame com os dados dos usuários
#     df_user_data = pd.DataFrame(user_data)
#     # print(df_user_data)


# # Dados de input
# df_picks_valid_csv = """
# user_id;Jogador;Rodada;tournament_id
# 1;1;QF;1
# 1;1;SF;1
# 1;32;QF;1
# 1;32;SF;1
# 1;32;F;1
# 1;32;Champion;1
# 1;63;QF;1
# 1;77;QF;1
# 1;92;QF;1
# 1;92;SF;1
# 1;121;QF;1
# """
# pg = 1+2+1+2+3+4+1+1+1+2+1
# print(pg) 
# # Convertendo os dados de input para DataFrame
# # df_valid_picks = pd.read_csv(StringIO(df_picks_valid_csv), sep=';')

# # # Pesos para cada rodada
# # weights = {"QF": 1, "SF": 2, "F": 3, "Champion": 4}

# # # Atualizações das rodadas e participantes qualificados
# roundUpdates = [
#     ('R1', {1, 3, 4, 6, 7, 8, 9, 11, 13, 15, 16, 17, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 37, 38, 40, 41, 42, 46, 47, 48, 49, 50, 51, 52, 53, 56, 60, 61, 63, 64, 65, 67, 69, 70, 71, 72, 74, 76, 77, 78, 79, 81, 82, 83, 84, 85, 86, 87, 88, 90, 91, 92, 93, 94, 95, 96, 98, 103, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 116, 117, 118, 119, 120, 122, 125, 126, 127, 129, 130, 132, 133, 134, 135, 136, 137, 138, 140, 141, 142, 144, 145, 146, 147, 148, 149, 153}),
#     ('R2', {1, 130, 3, 129, 134, 8, 9, 138, 140, 13, 144, 16, 17, 147, 148, 21, 145, 24, 153, 27, 29, 31, 32, 37, 40, 42, 47, 48, 50, 52, 56, 60, 63, 64, 67, 70, 72, 74, 76, 77, 78, 81, 83, 85, 86, 88, 90, 91, 92, 94, 96, 98, 103, 105, 106, 109, 110, 113, 114, 116, 119, 122, 125}),
#     ('R3', {1, 130, 129, 8, 9, 138, 16, 17, 145, 24, 153, 31, 32, 42, 47, 48, 56, 63, 67, 72, 77, 78, 83, 86, 91, 92, 98, 105, 106, 110, 114, 122}),
#     ('R4', {32, 1, 67, 9, 77, 110, 47, 48, 17, 83, 153, 122, 91, 92, 63, 31}),
#     ('QF', {32, 1, 77, 17, 122, 91, 92, 63}),
#     ('SF', {32, 1, 91, 92}),
#     ('F', {32, 91}),
#     ('Champion', {32})
# ]

# # qualified_per_round = {round: (qualified if isinstance(qualified, set) else {qualified})
# #                         for round, qualified in roundUpdates}
# # # print(qualified_per_round)

# # earned_points_data = []

# # for _, row in df_valid_picks.iterrows():
# #     user_id = row['user_id']
# #     player_id = row['Jogador']
# #     round = row['Rodada']
# #     tournament_id = row['tournament_id']

# #     if round in weights and player_id in qualified_per_round.get(round, set()):
# #         earned_points_data.append((user_id, tournament_id, weights[round]))

# # df_earned_points = pd.DataFrame(earned_points_data, columns=['user_id', 'tournament_id', 'Earned_Points'])
# # df_earned_points_summed = df_earned_points.groupby(['user_id', 'tournament_id'], as_index=False)['Earned_Points'].sum()
# # print(df_earned_points_summed)

# # df_earned_points_with_names = pd.merge(df_earned_points_summed, df_user_data, on='user_id')
# # df_earned_points_with_names.rename(columns={'username': 'Participante', 'Earned_Points': 'Pontos Ganhos'}, inplace=True)

# # latest_round = roundUpdates[-1][0]
# # df_earned_points_with_names['Rodada'] = latest_round
# # df_earned_points_with_names['Ranking PG'] = df_earned_points_with_names.groupby('tournament_id')['Pontos Ganhos'].rank(ascending=False, method='min')

# # df_earned_points_with_names.sort_values(by=['tournament_id', 'Pontos Ganhos'], ascending=[True, False], inplace=True)
# # df_earned_points_with_names.reset_index(drop=True, inplace=True)

# # df_earned_points_final = df_earned_points_with_names[['Ranking PG', 'Participante', 'Pontos Ganhos', 'tournament_id', 'Rodada']].copy()
# # print(df_earned_points_final)