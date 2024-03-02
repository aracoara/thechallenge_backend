import pandas as pd
from tennis_app.utils import trackTournamentEliminations, gatherFormattedTournamentPicks, process_and_update_rounds
import os


tournament_short_name = 'AO'
tournament_year = 2024
user_id = 38


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
    "F": 'tennis_app/assets/AO24/AO-24-Results - F.csv',
    "Champion": 'tennis_app/assets/AO24/AO-24-Results - Champion.csv',    
}

# Chamada da função para processar e atualizar as rodadas
RoundUpdates = process_and_update_rounds(etapas_torneio, tournament_short_name, tournament_year)

## Imprimindo as atualizações
for round_update in RoundUpdates:
    print(round_update)

# #########################PROCESSAR OS RESULTADOS DA RODADA################################

# Defina o caminho para o diretório 'assets' dentro de 'tennis_app'
assets_path = os.path.join('tennis_app', 'assets')
# Certifique-se de que o diretório 'assets' existe
os.makedirs(assets_path, exist_ok=True)

TournamentPicks_df = gatherFormattedTournamentPicks(tournament_short_name, tournament_year)
TournamentPicks_df = TournamentPicks_df[TournamentPicks_df['user_id'] == user_id]
print(TournamentPicks_df)

TournamentEliminations_df = trackTournamentEliminations(TournamentPicks_df, RoundUpdates)
print(TournamentEliminations_df)

ordem_rodadas = {rodada: indice for indice, (rodada, _) in enumerate(RoundUpdates)}    
print(ordem_rodadas)
valid_picks = []  # Lista para armazenar os palpites válidos

for index, row in TournamentPicks_df.iterrows():
    user_id = row['user_id']
    jogador = row['Jogador']
    rodada_palpite = row['Rodada']
    tournament_id = row['tournament_id']  # Assume-se que essa coluna já existe em picks_user_df

    # Verificando a rodada de classificação do jogador
    jogador_classificado = any(jogador in jogadores for rodada, jogadores in RoundUpdates if rodada == rodada_palpite)
    # print(f'Jogador: {jogador} classificado? {jogador_classificado}' ', Rodada do palpite:', rodada_palpite)
    
    # Verificando a rodada de eliminação do jogador
    elim_row = TournamentEliminations_df[(TournamentEliminations_df['user_id'] == user_id) & 
                                (TournamentEliminations_df['Jogador'] == jogador) & 
                                (TournamentEliminations_df['tournament_id'] == tournament_id)]
    if not elim_row.empty:
        rodada_eliminacao = elim_row['Rodada_Eliminacao'].values[0]
    else:
        rodada_eliminacao = 'Champion'  # Se não eliminado, considerar como se chegasse à final
    # print(f'Rodada de eliminação do jogador {jogador}:', rodada_eliminacao)    

    # Comparando a ordem das rodadas para determinar validade do palpite
    if jogador_classificado and ordem_rodadas.get(rodada_palpite, -1) <= ordem_rodadas.get(rodada_eliminacao, -1):
        valid_picks.append({**row.to_dict(), 'tournament_id': tournament_id})  # Adicionando o palpite à lista

    df_picks_valid = pd.DataFrame(valid_picks)
    print(df_picks_valid)
    # df_picks_valid.sort_values(by=['user_id', 'tournament_id', 'Rodada', 'Jogador'], inplace=True)
    # print(df_picks_valid)

# def compileValidTournamentPicks(picks_user_df, df_eliminados, atualizacoes):
#     # Mapeando as rodadas para valores numéricos para facilitar comparações
#     ordem_rodadas = {rodada: indice for indice, (rodada, _) in enumerate(atualizacoes)}    
#     valid_picks = []  # Lista para armazenar os palpites válidos

#     for index, row in picks_user_df.iterrows():
#         user_id = row['user_id']
#         jogador = row['Jogador']
#         rodada_palpite = row['Rodada']
#         tournament_id = row['tournament_id']  # Assume-se que essa coluna já existe em picks_user_df

#         # Verificando a rodada de classificação do jogador
#         jogador_classificado = any(jogador in jogadores for rodada, jogadores in atualizacoes if rodada == rodada_palpite)
        
#         # Verificando a rodada de eliminação do jogador
#         elim_row = df_eliminados[(df_eliminados['user_id'] == user_id) & 
#                                   (df_eliminados['Jogador'] == jogador) & 
#                                   (df_eliminados['tournament_id'] == tournament_id)]
#         if not elim_row.empty:
#             rodada_eliminacao = elim_row['Rodada_Eliminacao'].values[0]
#         else:
#             rodada_eliminacao = 'Champion'  # Se não eliminado, considerar como se chegasse à final

#         # Comparando a ordem das rodadas para determinar validade do palpite
#         if jogador_classificado and ordem_rodadas.get(rodada_palpite, -1) <= ordem_rodadas.get(rodada_eliminacao, -1):
#             valid_picks.append({**row.to_dict(), 'tournament_id': tournament_id})  # Adicionando o palpite à lista

#     # Criando um DataFrame com os palpites válidos
#     df_picks_valid = pd.DataFrame(valid_picks)
#     df_picks_valid.sort_values(by=['user_id', 'tournament_id', 'Rodada', 'Jogador'], inplace=True)


#     return df_picks_valid
