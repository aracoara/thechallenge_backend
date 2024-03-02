import pandas as pd

# Simulando os dados de atualizações
atualizacoes = [
('R1', {1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 
        37, 38, 39, 40, 41, 42, 44, 46, 47, 48, 49, 50, 51, 52, 53, 55, 56, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 74, 75, 
        76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 103, 104, 105, 106, 107, 
        108, 109, 110, 111, 112, 113, 114, 116, 117, 118, 119, 120, 121}),
('R2', {1, 3, 5, 8, 9, 12, 13, 16, 17, 19, 21, 23, 24, 27, 29, 31, 32, 34, 37, 39, 40, 42, 44, 47, 48, 50, 52, 55, 56, 60, 63, 64, 67, 
        68, 70, 72, 74, 76, 77, 78, 81, 83, 85, 86, 88, 90, 91, 92, 94, 96, 98, 99, 101, 103, 105, 106, 109, 110, 113, 114, 116, 119, 121}),
('R3', {1, 8, 9, 16, 17, 23, 24, 31, 32, 39, 42, 47, 48, 55, 56, 63, 67, 68, 72, 77, 78, 83, 86, 91, 92, 98, 99, 105, 106, 110, 114, 121}),
('R4', {32, 1, 67, 99, 9, 77, 110, 47, 48, 17, 83, 121, 91, 92, 63, 31}),
('QF', {32, 1, 77, 17, 121, 91, 92, 63}),
('SF', {32, 1, 91, 92}),
('F', {32, 91}),
# ('Champion', {32, 91})
]

# Simulando os dados para picks_user_df
picks_user_df_data = [
    [38, 2, 'QF', 1],
    [38, 20, 'QF', 1],
    [38, 35, 'QF', 1],
    [38, 52, 'QF', 1],
    [38, 67, 'QF', 1],
    [38, 79, 'QF', 1],
    [38, 105, 'QF', 1],
    [38, 121, 'QF', 1],
    [38, 2, 'SF', 1],
    [38, 35, 'SF', 1],
    [38, 67, 'SF', 1],
    [38, 121, 'SF', 1],
    [38, 2, 'F', 1],
    [38, 121, 'F', 1],
    [38, 121, 'Champion', 1]
]


picks_user_df_columns = ['user_id', 'Jogador', 'Rodada', 'tournament_id']
picks_user_df = pd.DataFrame(picks_user_df_data, columns=picks_user_df_columns)
# print(picks_user_df)

classificados_dict = dict(atualizacoes)

# Obter uma lista única de (user_id, player_id, tournament_id) a partir de df_picks_por_usuario
users_picks_players = picks_user_df[['user_id', 'Jogador', 'tournament_id']].drop_duplicates()
print(f'users_picks_players:\n{users_picks_players}')

# Preparar uma lista para armazenar os dados dos jogadores eliminados
players_eliminated_data = []

# Iterar pela lista de palpites dos usuários
for _, row in users_picks_players.iterrows():
    user_id = row['user_id']
    player_id = row['Jogador']
    tournament_id = row['tournament_id']

    # Verificar se o jogador foi eliminado em alguma rodada
    for i in range(len(atualizacoes) - 1):
        rodada_atual = atualizacoes[i][0]
        rodada_seguinte = atualizacoes[i + 1][0]

        classificados_atual = classificados_dict[rodada_atual]
        classificados_seguinte = classificados_dict.get(rodada_seguinte, set())

        if player_id in classificados_atual and player_id not in classificados_seguinte:
            # Corrigindo a lógica para jogadores que chegam à final mas não ganham
            if rodada_atual == 'F' and rodada_seguinte == 'Champion':
                rodada_eliminacao = 'F'
            else:
                rodada_eliminacao = 'Champion' if rodada_seguinte == 'Champion' else rodada_atual
            players_eliminated_data.append((user_id, rodada_eliminacao, player_id, tournament_id))

# Converter a lista para um DataFrame
df_players_eliminated = pd.DataFrame(players_eliminated_data, columns=['user_id', 'Rodada_Eliminacao', 'Jogador', 'tournament_id'])

# # Ordenar o DataFrame
# ordem_rodadas = {"R1": 1, "R2": 2, "R3": 3, "QF": 4, "SF": 5, "F": 6, "Champion": 7}
# df_players_eliminated['OrdemRodada'] = df_players_eliminated['Rodada_Eliminacao'].map(ordem_rodadas)
# df_players_eliminated.sort_values(by=['user_id', 'tournament_id', 'Rodada_Eliminacao', 'OrdemRodada', 'Jogador'], inplace=True)

# # Remover a coluna auxiliar 'OrdemRodada'
# df_players_eliminated.drop('OrdemRodada', axis=1, inplace=True)