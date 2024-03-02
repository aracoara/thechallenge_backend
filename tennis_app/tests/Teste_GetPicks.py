
import pandas as pd
from pandas import DataFrame

# Dados de input fornecidos
picks_data = {
    "user_id": [1, 1, 1, 1, 1, 1, 1],
    "game_id": [1, 2, 3, 4, 5, 6, 7],
    "winner_id": [1, 32, 78, 92, 32, 92, 32],
    "player1_id": [1, 32, 77, 92, 1, 78, 32],
    "player2_id": [31, 63, 78, 121, 32, 92, 92],
    "round": ["QF", "QF", "QF", "QF", "SF", "SF", "F"],
    "tournament_id": [1, 1, 1, 1, 1, 1, 1],
}

# Convertendo os dados fornecidos para um DataFrame
picks_df = pd.DataFrame(picks_data)

def gatherFormattedTournamentPicks(picks_df):
    # Simulação da lógica para processar os picks e incluir os campeões
    picks_data = []
    for index, pick in picks_df.iterrows():
        picks_data.append({
            "user_id": pick["user_id"],
            "Jogador": pick["player1_id"],
            "Rodada": pick["round"],
            "tournament_id": pick["tournament_id"]
        })
        picks_data.append({
            "user_id": pick["user_id"],
            "Jogador": pick["player2_id"],
            "Rodada": pick["round"],
            "tournament_id": pick["tournament_id"]
        })
        
        # Adicionando o campeão para a rodada final
        if pick["round"] == "F":
            picks_data.append({
                "user_id": pick["user_id"],
                "Jogador": pick["winner_id"],
                "Rodada": "Champion",
                "tournament_id": pick["tournament_id"]
            })

    # Criando o DataFrame com os dados processados
    df_picks_por_usuario = pd.DataFrame(picks_data)

    # Ordenação personalizada para as rodadas
    ordem_rodadas = {"QF": 1, "SF": 2, "F": 3, "Champion": 4}
    df_picks_por_usuario['OrdemRodada'] = df_picks_por_usuario['Rodada'].map(ordem_rodadas)
    df_picks_por_usuario.sort_values(by=['user_id', 'tournament_id', 'Jogador', 'OrdemRodada'], inplace=True)
    df_picks_por_usuario.drop('OrdemRodada', axis=1, inplace=True)

    return df_picks_por_usuario

# Testando a função com os dados fornecidos
df_picks_por_usuario = gatherFormattedTournamentPicks(picks_df)
print(df_picks_por_usuario)
