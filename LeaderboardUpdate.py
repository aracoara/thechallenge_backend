from tennis_app.utils import (
    gatherFormattedTournamentPicks, trackTournamentEliminations, compileValidTournamentPicks, 
    calculatePossiblePointsByTournament, calculateEarnedPoints, mergePossibleAndEarnedPoints,
    process_round_results_and_extract_ids, update_leaderboard_data
)
from tennis_app import app, db
import os

# Configuração inicial
app.app_context().push()
tournament_short_name = 'AO'
tournament_year = 2024
base_path = f'tennis_app/assets/{tournament_short_name}{tournament_year}'
os.makedirs(base_path, exist_ok=True)

tournament_stages = ["R1", "R2", "R3", "R4", "QF", "SF", "F", "Champion"]
weights = {"QF": 1, "SF": 2, "F": 3, "Champion": 4}

# Carrega os picks dos usuários uma única vez
TournamentPicks_df = gatherFormattedTournamentPicks(tournament_short_name, tournament_year)

# Inicializa a lista para armazenar as atualizações de rodada
round_updates = []

for stage in tournament_stages:
    csv_path = f'{base_path}/{tournament_short_name}-{tournament_year}-Results - {stage}.csv'
    player_ids = process_round_results_and_extract_ids(stage, csv_path, tournament_short_name, tournament_year)[1]

    ## Atualiza a lista de atualizações com os IDs dos jogadores para a etapa atual
    round_updates.append((stage, player_ids))
    print(f'Atualizações para a etapa {stage}:' + '\n', round_updates)

    ## Gera TournamentEliminations_df e ValidTournamentsPicks_df para a etapa atual
    TournamentEliminations_df = trackTournamentEliminations(TournamentPicks_df, round_updates)
    ValidTournamentsPicks_df = compileValidTournamentPicks(TournamentPicks_df, TournamentEliminations_df, round_updates)

    ## Salva os DataFrames gerados para a etapa atual
    elim_path = os.path.join(base_path, f'TournamentEliminations_{stage}_{tournament_short_name}_{tournament_year}.csv')
    valid_picks_path = os.path.join(base_path, f'ValidTournamentsPicks_{stage}_{tournament_short_name}_{tournament_year}.csv')
    TournamentEliminations_df.to_csv(elim_path, sep=';', encoding='utf-8', index=False)
    ValidTournamentsPicks_df.to_csv(valid_picks_path, sep=';', encoding='utf-8', index=False)

    ## Calcula os pontos possíveis e ganhos para a etapa atual
    LatestRound = round_updates[-1][0]
    PossiblePoints_df = calculatePossiblePointsByTournament(ValidTournamentsPicks_df, weights, round_updates)
    EarnedPoints_df = calculateEarnedPoints(ValidTournamentsPicks_df, round_updates, weights)
    Leaderboard_df = mergePossibleAndEarnedPoints(PossiblePoints_df, EarnedPoints_df, LatestRound)
    print(f'Leaderboard para a etapa {stage}:' + '\n', Leaderboard_df)

## if __name__ == '__main__':
    # Supondo que Leaderboard_df seja um DataFrame válido
    update_leaderboard_data(Leaderboard_df)
    print("Pontuações atualizadas com sucesso!")

###############################################################
    

# from tennis_app.utils import (gatherFormattedTournamentPicks, trackTournamentEliminations, compileValidTournamentPicks, 
#                               calculatePossiblePointsByTournament, calculateEarnedPoints, mergePossibleAndEarnedPoints,
#                               process_and_update_rounds)
# from tennis_app.models import Pontuacoes
# from tennis_app import app
# from tennis_app.extensions import db
# # import pandas as pd
# from datetime import datetime, timezone
# import os

# # Crie uma instância do aplicativo Flask se ainda não tiver uma
# app.app_context()

# tournament_short_name = 'AO'
# tournament_year = 2024

# ##########################################################################################
# #########################ATUALIZAR OS RESULTADOS DA RODADA################################
# ##########################################################################################

# # Definindo os caminhos dos arquivos em um dicionário
# # Supondo que process_results_data_position já esteja definida e retorne um DataFrame

# etapas_torneio = {
#     ## RIO 2024
#     # "R1": 'tennis_app/assets/RIO24/RIO-24-Results - R1.csv',
#     # "R2": 'tennis_app/assets/RIO24/RIO-24-Results - R2.csv',
#     # "R3": 'tennis_app/assets/RIO24/RIO-24-Results - R3.csv',
#     # "R4": 'tennis_app/assets/RIO24/RIO-24-Results - R4.csv',
#     # "QF": 'tennis_app/assets/RIO24/RIO-24-Results - QF.csv',
#     # "SF": 'tennis_app/assets/RIO24/RIO-24-Results - SF.csv',
#     # "F": 'tennis_app/assets/RIO24/RIO-24-Results - F.csv',
#     # "Champion": 'tennis_app/assets/RIO24/RIO-24-Results - Champion.csv',

#     ## AO 2024
#     "R1": 'tennis_app/assets/AO2024/AO-2024-Results - R1.csv',
#     "R2": 'tennis_app/assets/AO2024/AO-2024-Results - R2.csv',
#     "R3": 'tennis_app/assets/AO2024/AO-2024-Results - R3.csv',
#     "R4": 'tennis_app/assets/AO2024/AO-2024-Results - R4.csv',
#     "QF": 'tennis_app/assets/AO2024/AO-2024-Results - QF.csv',
#     "SF": 'tennis_app/assets/AO2024/AO-2024-Results - SF.csv',
#     "F": 'tennis_app/assets/AO2024/AO-2024-Results - F.csv',
#     "Champion": 'tennis_app/assets/AO2024/AO-2024-Results - Champion.csv',    
# }


# # Chamada da função para processar e atualizar as rodadas
# RoundUpdates = process_and_update_rounds(etapas_torneio, tournament_short_name, tournament_year)

# ## Imprimindo as atualizações
# # for round_update in RoundUpdates:
# #     print(round_update)

# # ##########################################################################################

# # ##########################################################################################
# # #########################PROCESSAR OS RESULTADOS DA RODADA################################
# # ##########################################################################################

# # Defina o caminho para o diretório 'assets' dentro de 'tennis_app'
# assets_path = os.path.join('tennis_app', 'assets')
# # Certifique-se de que o diretório 'assets' existe
# os.makedirs(assets_path, exist_ok=True)

# TournamentPicks_df = gatherFormattedTournamentPicks(tournament_short_name, tournament_year)
# # print("Print do DF dos picks por usuário:")
# # print(TournamentPicks_df)

# # Usando f-string para incluir variáveis no nome do arquivo
# # Crie o nome do arquivo com o caminho completo
# filename1 = f'TournamentPicks_{tournament_short_name}_{tournament_year}.csv'
# full_path1 = os.path.join(assets_path, filename1)
# ## Salve o DataFrame no caminho especificado
# TournamentPicks_df.to_csv(full_path1, sep=';', encoding='utf-8', index=False)

# # # # # Chamar a função com os palpites dos usuários e os dados dos classificados
# TournamentEliminations_df = trackTournamentEliminations(TournamentPicks_df, RoundUpdates)
# # print("Print dos jogadores eliminados:")
# # print(TournamentEliminations_df)
# filename2 = f'TournamentEliminations_{tournament_short_name}_{tournament_year}.csv'
# full_path2 = os.path.join(assets_path, filename2)
# # Salve o DataFrame no caminho especificado
# TournamentEliminations_df.to_csv(full_path2, sep=';', encoding='utf-8', index=False)

# # # # # # Chamada da função para determinar os picks válidos dos usuários
# ValidTournamentsPicks_df = compileValidTournamentPicks(TournamentPicks_df, TournamentEliminations_df, RoundUpdates)
# # # # # Exibir o DataFrame dos palpites válidos
# # print("DataFrame dos Palpites Válidos:")
# # print(ValidTournamentsPicks_df)
# filename3 = f'ValidTournamentsPicks_{tournament_short_name}_{tournament_year}.csv'
# full_path3 = os.path.join(assets_path, filename3)
# # Salve o DataFrame no caminho especificado
# ValidTournamentsPicks_df.to_csv(full_path3, sep=';', encoding='utf-8', index=False)


# # # # # # # # # ##########################################################################################
# # # # # # # # # #########################CALCULAR OS PONTOS DA RODADA#####################################
# # # # # # # # # ##########################################################################################

# # # # # # # Definindo os pesos para cada rodada
# weights = {"QF": 1, "SF": 2, "F": 3, "Champion": 4}

# # # # # # Calculando os pontos possíveis por usuário
# LatestRound = RoundUpdates[-1][0]  # Obtém a última rodada, assumindo que 'atualizacoes' esteja ordenado

# PossiblePoints_df = calculatePossiblePointsByTournament(ValidTournamentsPicks_df, weights, RoundUpdates)
# # # # print("Print dos Pontos Possíveis por Usuário:")
# # # # print(PossiblePoints_df)

# # # # # # # Calculando os pontos ganhos por usuário
# EarnedPoints_df = calculateEarnedPoints(ValidTournamentsPicks_df, RoundUpdates, weights)
# # # # # print("Print dos Pontos Ganhos por Usuário:")
# # # # # print(EarnedPoints_df)

# # # # # # ## DataFrame Final
# Leaderboard_df = mergePossibleAndEarnedPoints(PossiblePoints_df, EarnedPoints_df, LatestRound)
# # # # Leaderboard_df.to_csv('ScoreFinal_df.csv', sep=';', encoding='utf-8', index=False)
# print(f'Leaderboard para a etapa {LatestRound}:' + '\n', Leaderboard_df)



# # def update_leaderboard_data(Leaderboard_df):
# #     with app.app_context():
# #         current_tournament_id = int(Leaderboard_df['tournament_id'].iloc[0])
# #         current_rodada = Leaderboard_df['Rodada'].iloc[0]

# #         try:
# #             # Deletar registros existentes para a mesma rodada e torneio
# #             Pontuacoes.query.filter_by(tournament_id=current_tournament_id, rodada=current_rodada).delete()
# #             db.session.commit()

# #             # Preparar os objetos Pontuacoes para inserção
# #             for index, row in Leaderboard_df.fillna(0).iterrows():
# #                 new_record = Pontuacoes(
# #                     ranking_pp=int(row.get('Ranking PP', 0)),
# #                     ranking_pg=int(row.get('Ranking PG', 0)),
# #                     username=row['Participante'],
# #                     pontos_possiveis=int(row.get('Pontos Possíveis', 0)),
# #                     pontos_ganhos=int(row.get('Pontos Ganhos', 0)),
# #                     rodada=row['Rodada'],
# #                     # data_atualizacao=datetime.utcnow(),
# #                     data_atualizacao = datetime.now(timezone.utc),
# #                     tournament_id=int(row['tournament_id'])
# #                 )
# #                 db.session.add(new_record)

# #             db.session.commit()
# #             print("Dados de pontuação atualizados com sucesso para a rodada e torneio específicos.")
# #         except Exception as e:
# #             db.session.rollback()
# #             print(f"Ocorreu um erro ao atualizar os dados de pontuação: {e}")


# # if __name__ == '__main__':
# #     # Supondo que Leaderboard_df seja um DataFrame válido
# #     update_leaderboard_data(Leaderboard_df)
# #     print("Pontuações atualizadas com sucesso!")    