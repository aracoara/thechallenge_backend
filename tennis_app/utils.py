from tennis_app import app
from tennis_app.extensions import db
from tennis_app.models import Pick, Player, RoundType, User, Game, Tournament, Pontuacoes
import pandas as pd
import numpy as np  # Para usar np.nan que representa um valor vazio (similar a None)
from datetime import datetime, timezone
from sqlalchemy.orm import joinedload  # Para carregamento otimizado das relações
from flask_mail import Message
from tennis_app import mail
from contextlib import contextmanager



# Função para criar jogos de QF
def create_qf_games(data):
    quartasFinal = data.get('quartasFinal', {})
    semiFinal = data.get('semiFinal', {})
    qf_games = []

    # Mapeamento dos jogos de QF para SF corrigido para incluir ambas as entradas de jogadores
    for qf_key1, qf_key2, sf_key in [('QF1', 'QF2', 'SF1'), ('QF3', 'QF4', 'SF2'), ('QF5', 'QF6', 'SF3'), ('QF7', 'QF8', 'SF4')]:
        # Certifica-se que as chaves existem antes de tentar acessá-las para evitar KeyErrors
        if qf_key1 in quartasFinal and qf_key2 in quartasFinal and sf_key in semiFinal:
            player1_id = quartasFinal[qf_key1]
            player2_id = quartasFinal[qf_key2]
            winner_id = semiFinal[sf_key]

            qf_games.append({
                "round": str(RoundType.QF),
                "player1_id": player1_id,
                "player2_id": player2_id,
                "winner_id": winner_id,
            })

    return qf_games


# Exemplo de uso
# qf_games = create_qf_games(data)
# print(qf_games)

# Função para criar jogos de SF
def create_sf_games(data):
    semiFinal = data.get('semiFinal', {})
    final = data.get('final', {})
    sf_games = []

    # Mapeamento dos jogos de SF para F ajustado para incluir ambas as entradas de jogadores
    for sf_key1, sf_key2, f_key in [('SF1', 'SF2', 'F1'), ('SF3', 'SF4', 'F2')]:
        # Certifica-se que as chaves existem antes de tentar acessá-las para evitar KeyErrors
        if sf_key1 in semiFinal and sf_key2 in semiFinal and f_key in final:
            player1_id = semiFinal[sf_key1]
            player2_id = semiFinal[sf_key2]
            # O vencedor é determinado pela chave correspondente em 'final'
            winner_id = final[f_key]

            sf_games.append({
                "round": str(RoundType.SF),
                "player1_id": player1_id,
                "player2_id": player2_id,
                "winner_id": winner_id
            })

    return sf_games


# Exemplo de uso
# sf_games = create_sf_games(data)
# print(sf_games)

# Função para criar o jogo final e identificar o campeão
def create_final_game_and_champion(data):
    final_games = []

    # Identificar os jogadores da final e o campeão
    player1_key = 'F1'
    player2_key = 'F2'
    player1_id = data["final"][player1_key]
    player2_id = data["final"][player2_key]
    champion_id = data["campeao"]

    round_enum = RoundType.F

    # Criar o jogo final
    final_game = {
        "round": round_enum,
        "player1_id": player1_id,
        "player2_id": player2_id,
        "winner_id": champion_id  # O campeão é o vencedor do jogo final
    }
    final_games.append(final_game)

    return final_games

def create_all_games(data):
    all_games = []
    # Mapeamento dos jogos de QF para SF e de SF para F
    next_round_mapping = {
        'QF1': 'SF1', 'QF2': 'SF1',
        'QF3': 'SF2', 'QF4': 'SF2',
        'QF5': 'SF3', 'QF6': 'SF3',
        'QF7': 'SF4', 'QF8': 'SF4',
        'SF1': 'F1', 'SF2': 'F1',
        'SF3': 'F2', 'SF4': 'F2'
    }

    # Criar jogos para quartas de final e semifinal
    for round_key in ['quartasFinal', 'semiFinal']:
        round_data = data[round_key]
        sorted_keys = sorted(round_data.keys())
        
        for i in range(0, len(sorted_keys), 2):
            key1 = sorted_keys[i]
            key2 = sorted_keys[i + 1] if i + 1 < len(sorted_keys) else None

            player1_id = round_data[key1]
            player2_id = round_data[key2] if key2 else None
            winner_id = data["semiFinal"][next_round_mapping[key1]] if round_key == 'quartasFinal' else data["final"][next_round_mapping[key1]]

            round_enum = RoundType.QF if round_key == 'quartasFinal' else RoundType.SF
            
            all_games.append({
                "round": str(round_enum),
                "player1_id": player1_id,
                "player2_id": player2_id,
                "winner_id": winner_id,
                "tournament_id": data['tournament_id']
            })

    # Criar jogo final
    player1_id = data["final"]['F1']
    player2_id = data["final"]['F2']
    champion_id = data["campeao"]

    final_game = {
        "round": str(RoundType.F),
        "player1_id": player1_id,
        "player2_id": player2_id,
        "winner_id": champion_id,
        "tournament_id": data['tournament_id']
    }
    all_games.append(final_game)

    return all_games

@contextmanager
def session_scope():
    """Fornecer um escopo de transação."""
    try:
        yield
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def delete_existing_games():
    """Apaga jogos e picks existentes."""
    Game.query.delete()
    # Pick.query.delete()  # Descomente se também quiser apagar os picks
    print("Jogos e Picks existentes apagados.")

def create_and_save_games(all_games):
    """Cria e salva novos jogos no banco de dados."""
    games_created = []
    for game_data in all_games:
        game = Game(
            round=game_data['round'],
            player1_id=game_data['player1_id'],
            player2_id=game_data['player2_id'],
            winner_id=game_data.get('winner_id'),
            tournament_id=game_data['tournament_id']
        )
        db.session.add(game)
        games_created.append(game)
    db.session.flush()  # Prepara os objetos de jogo para obter IDs
    print(f"Jogos criados com sucesso: {len(games_created)} jogos")

def create_or_update_picks(user, games):
    """Verifica e cria/atualiza previsões."""
    for game in games:
        # Busca por um Pick existente
        pick = Pick.query.filter_by(user_id=user.id, game_id=game.id).first()

        # Se o Pick não existir, cria um novo
        if not pick:
            pick = Pick(
                user_id=user.id,
                game_id=game.id,
                winner_id=game.winner_id,
                player1_id=game.player1_id,
                player2_id=game.player2_id,
                round=game.round,
                tournament_id=game.tournament_id  # Assumindo que 'game' tem um atributo 'tournament_id'
            )
            db.session.add(pick)
        else:
            # Atualiza o Pick existente
            pick.winner_id = game.winner_id
            pick.player1_id = game.player1_id
            pick.player2_id = game.player2_id
            # Não é necessário atualizar tournament_id para um Pick existente, assumindo que um jogo não muda de torneio.
            # No entanto, se for possível mudar, descomente a linha abaixo.
            pick.tournament_id = game.tournament_id
        
        print(f"Pick {(pick.id if pick.id else 'novo')} criado/atualizado com sucesso.")
    
    # db.session.commit()  # Confirma as mudanças no banco de dados após processar todos os jogos.


def process_games_and_picks(data):
    """Processa jogos e previsões."""
    with app.app_context():
        user_id = data.get('user_id')
        user = User.query.get(user_id)
        if not user:
            print(f"Usuário com ID {user_id} não encontrado.")
            return

        all_games = create_all_games(data)
        with session_scope():
            delete_existing_games()
            create_and_save_games(all_games)
            create_or_update_picks(user, Game.query.all())
        print("Processamento de jogos e picks concluído com sucesso.")

# Função para processar o arquivo de resultados
def process_results_data(file_path):
    # Lendo e processando o arquivo CSV
    df = pd.read_csv(file_path, encoding='ISO-8859-1', header=None, names=['result'])
    with app.app_context():
        # Criar um dicionário para mapear nomes de jogadores para seus IDs
        player_id_map = {player.name: player.id for player in Player.query.all()}

        # Extrair o nome do jogador do campo 'result' e mapear para player_id
        df['name'] = df['result'].str.extract(r'^(.*?)\s+\(')
        df['player_id'] = df['name'].map(player_id_map)

        # Removendo linhas com valores NaN em 'player_id'
        df = df.dropna(subset=['player_id'])

        # Convertendo 'player_id' para int, tratando erros
        df['player_id'] = pd.to_numeric(df['player_id'], downcast='integer', errors='coerce').dropna()

    # Convertendo a coluna 'player_id' para um set e descartando NaN
    player_ids = set(df['player_id'].dropna())

    return player_ids

# Função para obter todos os picks
def get_all_picks():
    with app.app_context():
        picks = Pick.query.all()
        picks_df = pd.DataFrame([{
            "id": pick.id,
            "user_id": pick.user_id,
            "game_id": pick.game_id,
            "player1_id": pick.player1_id,
            "player2_id": pick.player2_id,
            "round": pick.round,
            "winner_id": pick.winner_id
            # Inclua outros campos conforme necessário
        } for pick in picks])
        return picks_df


# Método para atualizar os resultados do torneio
def atualizar_resultados_multiplos(atualizacoes):
    # Inicializando o dicionário de resultados do torneio dentro da função
    resultados_torneio = {
        "R1": set(), "R2": set(), "R3": set(), "R4": set(),
        "QF": set(), "SF": set(), "F": set(), "Champion": None
    }

    for rodada, classificados in atualizacoes:
        # Atualizar o dicionário com base nas atualizações fornecidas
        if rodada in resultados_torneio:
            if rodada == "Champion":
                # Tratar "Champion" como um caso especial, se necessário
                resultados_torneio[rodada] = classificados
            else:
                resultados_torneio[rodada] = set(classificados)
        else:
            print(f"Rodada {rodada} inválida. Verifique se a rodada está correta.")

    # Retornando o dicionário atualizado para uso ou inspeção fora da função
    return resultados_torneio



def picks_por_usuario(picks_user):
    # Verifica se 'tournament_id' está presente em 'picks_user'
    if 'tournament_id' not in picks_user[0]:
        raise ValueError("Erro: A coluna 'tournament_id' está faltando nos dados fornecidos.")

    picks_data = []
    for palpite in picks_user:
        user_id = palpite["user_id"]
        player1_id = palpite["player1_id"]
        player2_id = palpite["player2_id"]
        winner_id = palpite["winner_id"]
        pick_round = palpite["round"]
        tournament_id = palpite["tournament_id"]

        picks_data.append((user_id, player1_id, pick_round, tournament_id))
        picks_data.append((user_id, player2_id, pick_round, tournament_id))

        if pick_round == "F":
            picks_data.append((user_id, winner_id, "Champion", tournament_id))

    df_picks_por_usuario = pd.DataFrame(picks_data, columns=['User_ID', 'Jogador', 'Rodada', 'tournament_id'])

    # Mapeamento para a ordenação das rodadas
    ordem_rodadas = {"QF": 1, "SF": 2, "F": 3, "Champion": 4}
    df_picks_por_usuario['OrdemRodada'] = df_picks_por_usuario['Rodada'].map(ordem_rodadas)
    df_picks_por_usuario.sort_values(by=['User_ID', 'tournament_id', 'Jogador', 'OrdemRodada'], inplace=True)

    # Removendo a coluna auxiliar 'OrdemRodada'
    df_picks_por_usuario.drop('OrdemRodada', axis=1, inplace=True)

    return df_picks_por_usuario


def gatherFormattedTournamentPicks(tournament_short_name, tournament_year):
    with app.app_context():
        # Buscando o torneio pelo nome e ano
        tournament = Tournament.query.filter_by(short_name=tournament_short_name, year=tournament_year).first()
        if not tournament:
            print("Torneio não encontrado.")
            return

        # Filtrar as picks para o tournament_id especificado, pré-carregando as relações necessárias
        picks = Pick.query.filter_by(tournament_id=tournament.id) \
                          .options(joinedload(Pick.game)) \
                          .all()

        # Formatando os resultados para criação de um DataFrame
        picks_data = []
        for pick in picks:
            picks_data.extend([
                {
                    "user_id": pick.user_id,
                    "Jogador": pick.player1_id,
                    "Rodada": str(pick.round),
                    "tournament_id": pick.tournament_id
                },
                {
                    "user_id": pick.user_id,
                    "Jogador": pick.player2_id,
                    "Rodada": str(pick.round),
                    "tournament_id": pick.tournament_id
                }
            ])
            
            # Lógica para adicionar o pick de champion
            # print(f"Processando pick: {pick.id}, round: {pick.round}")
            if pick.round.value == 'F':
                # print("Adicionando campeão...")
                champion_id = pick.winner_id  # Certifique-se de que este é o atributo correto
                if champion_id:  # Verificação adicional para garantir que champion_id não é None
                    picks_data.append({
                        "user_id": pick.user_id,
                        "Jogador": champion_id,
                        "Rodada": "Champion",
                        "tournament_id": pick.tournament_id
                    })
                else:
                    print("Atenção: champion_id é None para a pick de ID:", pick.id)

        # Criando o DataFrame
        df_picks_por_usuario_temp = pd.DataFrame(picks_data)
        df_picks_por_usuario = df_picks_por_usuario_temp.copy().drop_duplicates()

        # Mapeamento para a ordenação das rodadas
        ordem_rodadas = {"QF": 1, "SF": 2, "F": 3, "Champion": 4}
        df_picks_por_usuario['OrdemRodada'] = df_picks_por_usuario['Rodada'].map(ordem_rodadas)
        df_picks_por_usuario.sort_values(by=['user_id', 'tournament_id', 'OrdemRodada', 'Jogador'], inplace=True)

        # Removendo a coluna auxiliar 'OrdemRodada'
        df_picks_por_usuario.drop('OrdemRodada', axis=1, inplace=True)

        return df_picks_por_usuario



# def gatherFormattedTournamentPicks():
#     with app.app_context():
#         # Buscando todos os picks e pré-carregando as relações necessárias para evitar N+1 queries
#         picks = Pick.query.options(joinedload(Pick.game)).all()

#         # Formatando os resultados diretamente em uma estrutura adequada para criar um DataFrame
#         picks_data = [
#             {
#                 "user_id": pick.user_id,
#                 "Jogador": pick.player1_id,
#                 "Rodada": str(pick.round),
#                 "tournament_id": pick.tournament_id
#             }
#             for pick in picks
#         ] + [
#             {
#                 "user_id": pick.user_id,
#                 "Jogador": pick.player2_id,
#                 "Rodada": str(pick.round),
#                 "tournament_id": pick.tournament_id
#             }
#             for pick in picks
#         ]

#         # Se necessário, adicione lógica para picks do vencedor final

#         # Criando o DataFrame
#         df_picks_por_usuario = pd.DataFrame(picks_data)

#         # Mapeamento para a ordenação das rodadas
#         ordem_rodadas = {"QF": 1, "SF": 2, "F": 3, "Champion": 4}
#         df_picks_por_usuario['OrdemRodada'] = df_picks_por_usuario['Rodada'].map(ordem_rodadas)
#         df_picks_por_usuario.sort_values(by=['user_id', 'tournament_id', 'Jogador', 'OrdemRodada'], inplace=True)

#         # Removendo a coluna auxiliar 'OrdemRodada'
#         df_picks_por_usuario.drop('OrdemRodada', axis=1, inplace=True)

#         return df_picks_por_usuario

def trackTournamentEliminations(df_picks_por_usuario, atualizacoes):
    # Criar um dicionário para os classificados de cada rodada
    classificados_dict = dict(atualizacoes)

    # Obter uma lista única de (user_id, player_id, tournament_id) a partir de df_picks_por_usuario
    users_picks_players = df_picks_por_usuario[['user_id', 'Jogador', 'tournament_id']].drop_duplicates()

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

    # Ordenar o DataFrame
    ordem_rodadas = {"R1": 1, "R2": 2, "R3": 3, "QF": 4, "SF": 5, "F": 6, "Champion": 7}
    df_players_eliminated['OrdemRodada'] = df_players_eliminated['Rodada_Eliminacao'].map(ordem_rodadas)
    df_players_eliminated.sort_values(by=['user_id', 'tournament_id', 'Rodada_Eliminacao', 'OrdemRodada', 'Jogador'], inplace=True)

    # Remover a coluna auxiliar 'OrdemRodada'
    df_players_eliminated.drop('OrdemRodada', axis=1, inplace=True)

    return df_players_eliminated

# def trackTournamentEliminations(df_picks_por_usuario, atualizacoes):
#     # Criar um dicionário para os classificados de cada rodada
#     classificados_dict = dict(atualizacoes)

#     # Obter uma lista única de (user_id, player_id, tournament_id) a partir de df_picks_por_usuario
#     users_picks_players = df_picks_por_usuario[['user_id', 'Jogador', 'tournament_id']].drop_duplicates()

#     # Preparar uma lista para armazenar os dados dos jogadores eliminados
#     players_eliminated_data = []

#     # Iterar pela lista de palpites dos usuários
#     for _, row in users_picks_players.iterrows():
#         user_id = row['user_id']
#         player_id = row['Jogador']
#         tournament_id = row['tournament_id']

#         # Verificar se o jogador foi eliminado em alguma rodada
#         for i in range(len(atualizacoes) - 1):
#             rodada_atual = atualizacoes[i][0]
#             rodada_seguinte = atualizacoes[i + 1][0]

#             classificados_atual = classificados_dict[rodada_atual]
#             classificados_seguinte = classificados_dict.get(rodada_seguinte, set())

#             if player_id in classificados_atual and player_id not in classificados_seguinte:
#                 # Para a rodada 'Champion', a eliminação é marcada na rodada anterior
#                 rodada_eliminacao = 'Champion' if rodada_seguinte == 'Champion' else rodada_atual
#                 players_eliminated_data.append((user_id, rodada_eliminacao, player_id, tournament_id))

#     # Converter a lista para um DataFrame
#     df_players_eliminated = pd.DataFrame(players_eliminated_data, columns=['user_id', 'Rodada_Eliminacao', 'Jogador', 'tournament_id'])

#     # Ordenar o DataFrame
#     ordem_rodadas = {"R1": 1, "R2": 2, "R3": 3, "QF": 4, "SF": 5, "F": 6, "Champion": 7}
#     df_players_eliminated['OrdemRodada'] = df_players_eliminated['Rodada_Eliminacao'].map(ordem_rodadas)
#     df_players_eliminated.sort_values(by=['user_id', 'tournament_id', 'OrdemRodada', 'Jogador'], inplace=True)

#     # Remover a coluna auxiliar 'OrdemRodada'
#     df_players_eliminated.drop('OrdemRodada', axis=1, inplace=True)

#     return df_players_eliminated

# Método para determinar os picks válidos dos usuários
def compileValidTournamentPicks(picks_user_df, df_eliminados, atualizacoes):
    # Mapeando as rodadas para valores numéricos para facilitar comparações
    ordem_rodadas = {rodada: indice for indice, (rodada, _) in enumerate(atualizacoes)}    
    valid_picks = []  # Lista para armazenar os palpites válidos

    for index, row in picks_user_df.iterrows():
        user_id = row['user_id']
        jogador = row['Jogador']
        rodada_palpite = row['Rodada']
        tournament_id = row['tournament_id']  # Assume-se que essa coluna já existe em picks_user_df

        # Verificando a rodada de classificação do jogador
        jogador_classificado = any(jogador in jogadores for rodada, jogadores in atualizacoes if rodada == rodada_palpite)
        
        # Verificando a rodada de eliminação do jogador
        elim_row = df_eliminados[(df_eliminados['user_id'] == user_id) & 
                                  (df_eliminados['Jogador'] == jogador) & 
                                  (df_eliminados['tournament_id'] == tournament_id)]
        if not elim_row.empty:
            rodada_eliminacao = elim_row['Rodada_Eliminacao'].values[0]
        else:
            rodada_eliminacao = 'Champion'  # Se não eliminado, considerar como se chegasse à final

        # Comparando a ordem das rodadas para determinar validade do palpite
        if jogador_classificado and ordem_rodadas.get(rodada_palpite, -1) <= ordem_rodadas.get(rodada_eliminacao, -1):
            valid_picks.append({**row.to_dict(), 'tournament_id': tournament_id})  # Adicionando o palpite à lista

    # Criando um DataFrame com os palpites válidos
    df_picks_valid = pd.DataFrame(valid_picks)
    df_picks_valid.sort_values(by=['user_id', 'tournament_id', 'Rodada', 'Jogador'], inplace=True)
    df_picks_valid = df_picks_valid.drop_duplicates()

    return df_picks_valid

def compileValidTournamentPicks(picks_user_df, df_eliminados, atualizacoes):
    # Mapeando as rodadas para valores numéricos para facilitar comparações
    ordem_rodadas = {rodada: indice for indice, (rodada, _) in enumerate(atualizacoes)}
    
    valid_picks = []  # Lista para armazenar os palpites válidos

    for index, row in picks_user_df.iterrows():
        user_id = row['user_id']
        jogador = row['Jogador']
        rodada_palpite = row['Rodada']
        tournament_id = row['tournament_id']  # Assume-se que essa coluna já existe em picks_user_df

        # Verificando a rodada de eliminação do jogador
        elim_row = df_eliminados[(df_eliminados['user_id'] == user_id) & (df_eliminados['Jogador'] == jogador)]
        if not elim_row.empty:
            rodada_eliminacao = elim_row['Rodada_Eliminacao'].values[0]
            
            # Comparando a ordem das rodadas para determinar validade do palpite
            if ordem_rodadas.get(rodada_palpite, float('inf')) <= ordem_rodadas.get(rodada_eliminacao, float('inf')):
                valid_picks.append({**row.to_dict(), 'tournament_id': tournament_id})  # Adicionando o palpite à lista
        else:
            valid_picks.append({**row.to_dict(), 'tournament_id': tournament_id})

    # Criando um DataFrame com os palpites válidos
    df_picks_valid = pd.DataFrame(valid_picks)
    # Removendo linhas duplicadas
    df_picks_valid = df_picks_valid.drop_duplicates()

    return df_picks_valid


def calculatePossiblePointsByTournament(df_picks_valid, weights, RoundUpdates):
    """
    Calculates possible points for each user based on valid picks, 
    considering the tournament and incorporating user data.
    
    Parameters:
    - df_picks_valid (DataFrame): DataFrame containing the valid picks.
    - weights (dict): Dictionary with the weights assigned for each round.
    - RoundUpdates (list): List of tuples containing round updates.

    Returns:
    - pontos_possiveis_final_df (DataFrame): DataFrame with Participant, Possible Points,
      Ranking by Possible Points, and the latest round information.
    """
    # Assuming get_user_data() is a function that fetches user data including user_id and username
    user_data_df = get_user_data()
    
    # Merging user data with valid picks based on user_id
    df_picks_valid = pd.merge(df_picks_valid, user_data_df, on='user_id', how='left')
    
    # Obtaining the latest round from RoundUpdates
    LatestRound = RoundUpdates[-1][0]
    
    # Calculating possible points for each user and tournament
    pontos_possiveis_por_usuario = df_picks_valid.groupby(['user_id', 'tournament_id', 'username'])['Rodada'].apply(
        lambda rodadas: sum(weights.get(rodada, 0) for rodada in rodadas)
    ).reset_index(name='Pontos_Possiveis')

    # Renaming columns for clarity
    pontos_possiveis_por_usuario.rename(columns={'username': 'Participante', 'Pontos_Possiveis': 'Pontos Possíveis'}, inplace=True)

    # Sorting by "Pontos Possíveis" in descending order within each tournament
    pontos_possiveis_por_usuario.sort_values(by=['tournament_id', 'Pontos Possíveis'], ascending=[True, False], inplace=True)

    # Adding ranking column based on descending order of possible points within each tournament
    pontos_possiveis_por_usuario['Ranking PP'] = pontos_possiveis_por_usuario.groupby('tournament_id')['Pontos Possíveis'].rank(ascending=False, method='min')

    # Selecting and ordering desired columns
    pontos_possiveis_final_df = pontos_possiveis_por_usuario[['Ranking PP', 'Participante', 'Pontos Possíveis', 'tournament_id']].copy()
    pontos_possiveis_final_df['Rodada'] = LatestRound

    return pontos_possiveis_final_df

def calculateEarnedPoints(validTournamentPicks_df, RoundUpdates, weights):
    # Determinar a última rodada atualizada a partir de RoundUpdates
    latest_round = RoundUpdates[-1][0]
    
    # Definir a ordem das rodadas para uso no cálculo do índice, baseando-se nas chaves do dicionário de pesos
    round_order = ["QF", "SF", "F", "Champion"]
    
    # Verificar se latest_round está na ordem definida; se não, retornar DataFrame vazio
    if latest_round not in weights:
        return pd.DataFrame()
    
    # Calcular os pontos baseando-se na ordem das rodadas e nos pesos definidos
    validTournamentPicks_df['Earned_Points'] = validTournamentPicks_df['Rodada'].apply(
        lambda x: weights[x] if round_order.index(x) <= round_order.index(latest_round) else None
    )
    # Substituir 0 por None
    # validTournamentPicks_df['Earned_Points'].replace(0, None, inplace=True)
    validTournamentPicks_df['Earned_Points'] = validTournamentPicks_df['Earned_Points'].replace(0, None)


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



def mergePossibleAndEarnedPoints(possible_points_df, earned_points_df, latest_round):
    # Assegura a renomeação para 'Participante' em ambos os DataFrames
    possible_points_df.rename(columns={'username': 'Participante'}, inplace=True, errors='ignore')
    earned_points_df.rename(columns={'username': 'Participante'}, inplace=True, errors='ignore')

    # Prepara o DataFrame final diretamente com 'possible_points_df' se 'earned_points_df' estiver vazio
    if earned_points_df.empty:
        final_df = possible_points_df.copy()
        final_df['Pontos Ganhos'] = np.nan  # Usa NaN para 'Pontos Ganhos' quando não há dados
        final_df['Ranking PG'] = np.nan  # Define 'Ranking PG' como vazio quando não há dados de 'earned_points_df'
    else:
        # Realiza o merge se 'earned_points_df' não estiver vazio
        final_df = pd.merge(possible_points_df, earned_points_df, on=['Participante', 'tournament_id'], how='left')
        # final_df['Pontos Ganhos'].fillna(0, inplace=True)  # Preenche valores nulos com 0 após o merge
        final_df['Pontos Ganhos'] = final_df['Pontos Ganhos'].fillna(0)


    # Atualiza 'Rodada' para a última rodada informada
    final_df['Rodada'] = latest_round

    # Calcula 'Ranking PP' para 'Pontos Possíveis' e 'Ranking PG' para 'Pontos Ganhos'
    final_df['Ranking PP'] = final_df.groupby('tournament_id')['Pontos Possíveis'].rank(method='min', ascending=False)
    final_df['Ranking PG'] = final_df.groupby('tournament_id')['Pontos Ganhos'].rank(method='min', ascending=False, na_option='keep')

    # Adiciona ou atualiza colunas para refletir todos os atributos da classe Pontuacoes
    final_df['data_atualizacao'] = pd.Timestamp('now')  # Assume a data atual para a coluna de atualização

    # Se necessário, adicione ou ajuste outras colunas baseadas na classe Pontuacoes aqui
    # Por exemplo, se existirem outras colunas que precisem ser incorporadas ao DataFrame final

    # Define a ordem das colunas conforme os atributos da classe Pontuacoes
    column_order = ['Participante', 'Pontos Possíveis', 'Pontos Ganhos', 'Ranking PP', 'Ranking PG', 'Rodada', 'tournament_id', 'data_atualizacao']
    final_df = final_df.reindex(columns=column_order)

    return final_df




# def mergePossibleAndEarnedPoints(possible_points_df, earned_points_df, latest_round):
#     """
#     Merge the possible and earned points DataFrames, ensuring that if the earned_points_df is empty,
#     the merge still occurs and 'Pontos Ganhos' are filled with 0.
#     """
#     # Garantir que as colunas estejam nomeadas consistentemente para o merge
#     if 'username' in possible_points_df.columns:
#         possible_points_df.rename(columns={'username': 'Participante'}, inplace=True)
#     if 'username' in earned_points_df.columns:
#         earned_points_df.rename(columns={'username': 'Participante'}, inplace=True)

#     # Definir a ordem das colunas desejada para o DataFrame final
#     column_order = ['Participante', 'tournament_id', 'Pontos Possíveis', 'Pontos Ganhos', 'Rodada']

#     # Preparar o DataFrame final com a estrutura de colunas desejada, preenchendo com valores padrão
#     final_df = pd.DataFrame(columns=column_order)
#     final_df['Pontos Possíveis'] = possible_points_df['Pontos Possíveis']
#     final_df['Participante'] = possible_points_df['Participante']
#     final_df['tournament_id'] = possible_points_df['tournament_id']
#     final_df['Rodada'] = latest_round
#     final_df['Pontos Ganhos'] = 0  # Predefinir 'Pontos Ganhos' com 0

#     # Se earned_points_df não estiver vazio, fazer o merge
#     if not earned_points_df.empty:
#         # Merge dos DataFrames com base em 'Participante' e 'tournament_id'
#         merged_df = pd.merge(possible_points_df[['Participante', 'tournament_id', 'Pontos Possíveis']],
#                              earned_points_df[['Participante', 'tournament_id', 'Pontos Ganhos']],
#                              on=['Participante', 'tournament_id'],
#                              how='left')

#         # Atualizar 'Pontos Ganhos' após o merge, preenchendo valores nulos com 0
#         merged_df['Pontos Ganhos'].fillna(0, inplace=True)
#         merged_df['Rodada'] = latest_round  # Atualizar a coluna 'Rodada' para a última rodada disponível

#         # Atualizar final_df com os dados mesclados
#         final_df = merged_df

#     # Certificar-se de que todas as colunas estão na ordem desejada
#     final_df = final_df[column_order]

#     return final_df





# Método para obter todos os picks
def get_picks():
    with app.app_context():
        # Buscando todos os picks e pré-carregando as relações necessárias para evitar N+1 queries
        picks = Pick.query.options(joinedload(Pick.game)).all()
        
        # Formatando os resultados em uma lista de dicionários
        picks_user = [
            {
                "user_id": pick.user_id,
                "player1_id": pick.player1_id,
                "player2_id": pick.player2_id,
                "winner_id": pick.winner_id,
                "round": str(pick.round),
                "tournament_id": pick.tournament_id
            }
            for pick in picks
        ]
        
        return picks_user
    
## Método para obter todos os IDs dos jogadores
def get_player_ids():
    with app.app_context():
        # Dentro deste bloco, você está no contexto da aplicação
        # Agora você pode realizar consultas ao banco de dados
        player_ids = [player.id for player in Player.query.with_entities(Player.id).all()]

        return player_ids
    
# Método para obter os dados dos usuários
def get_user_data():
    with app.app_context():
        # Dentro deste bloco, você está no contexto da aplicação
        # Agora você pode realizar consultas ao banco de dados
        user_data = [
            {
                "user_id": user.id,  # Ajuste feito aqui
                "username": user.username,
            }
            for user in User.query.all()
        ]

        # Aqui não é mais necessário especificar as colunas, pois os dicionários já têm as chaves corretas
        df_user_data = pd.DataFrame(user_data)

        return df_user_data

# Método para obter os picks processados    
def get_and_process_picks():
    with app.app_context():
        # Inicia a sessão do SQLAlchemy
        session = db.session

        users = User.query.all()
        processed_picks_list = []

        for user in users:
            user_picks_dict = {
                'User': user.username,
                'QF1': None, 'QF2': None, 'QF3': None, 'QF4': None,
                'QF5': None, 'QF6': None, 'QF7': None, 'QF8': None,
                'SF1': None, 'SF2': None, 'SF3': None, 'SF4': None,
                'F1': None, 'F2': None, 'Champion': None
            }

            for pick in user.picks:
                # Busca os nomes dos jogadores a partir dos IDs usando a sessão do SQLAlchemy
                player1 = session.get(Player, pick.player1_id) if pick.player1_id else None
                player2 = session.get(Player, pick.player2_id) if pick.player2_id else None
                winner = session.get(Player, pick.winner_id) if pick.winner_id else None
                
                round_key = pick.round.name if hasattr(pick.round, 'name') else str(pick.round)
                # Mapeia os nomes dos jogadores para as fases correspondentes
                if round_key.startswith('QF'):
                    user_picks_dict[f'QF{2*(pick.game_id-1)+1}'] = player1.name if player1 else None
                    user_picks_dict[f'QF{2*(pick.game_id-1)+2}'] = player2.name if player2 else None
                elif round_key.startswith('SF'):
                    # Corrige o mapeamento para SF1 e SF2 baseando-se no game_id 5
                    if pick.game_id == 5:
                        user_picks_dict['SF1'] = player1.name if player1 else None
                        user_picks_dict['SF2'] = player2.name if player2 else None
                    # Corrige o mapeamento para SF3 e SF4 baseando-se no game_id 6
                    elif pick.game_id == 6:
                        user_picks_dict['SF3'] = player1.name if player1 else None
                        user_picks_dict['SF4'] = player2.name if player2 else None
                elif round_key == 'F' and pick.game_id == 7:
                    user_picks_dict['F1'] = player1.name if player1 else None
                    user_picks_dict['F2'] = player2.name if player2 else None
                    user_picks_dict['Champion'] = winner.name if winner else None

            processed_picks_list.append(user_picks_dict)
        
        return pd.DataFrame(processed_picks_list)

# Método para mapear IDs de jogadores para nomes
def map_ids_to_names(player_ids):
    with app.app_context():
        # Inicia a sessão do SQLAlchemy
        session = db.session
        # Busca os jogadores e mapeia seus IDs para nomes
        players = session.query(Player).filter(Player.id.in_(player_ids)).all()
        id_to_name = {player.id: player.name for player in players}
        return id_to_name

# Método para obter os jogadores classificados
def get_classified_players(classificados_QF, classificados_SF, classificados_F, Champion):
    
    # Mapeia os IDs para nomes usando a função auxiliar
    id_to_name = map_ids_to_names(classificados_QF.union(classificados_SF, classificados_F, Champion))

    # Cria listas de nomes dos jogadores para cada fase
    classified_players = []
    for player_id in classificados_QF:
        classified_players.append({'name': id_to_name.get(player_id), 'round': 'QF'})
    for player_id in classificados_SF:
        classified_players.append({'name': id_to_name.get(player_id), 'round': 'SF'})
    for player_id in classificados_F:
        classified_players.append({'name': id_to_name.get(player_id), 'round': 'F'})
    for player_id in Champion:
        classified_players.append({'name': id_to_name.get(player_id), 'round': 'Champion'})

    return classified_players

# Método para processar os dados de resultados com posição
def process_results_data_position(file_path, tournament_short_name, tournament_year):
    # Lendo o arquivo CSV
    df = pd.read_csv(file_path, encoding='ISO-8859-1', skiprows=1, names=['Position', 'Player'])

    with app.app_context():
        tournament = Tournament.query.filter_by(short_name=tournament_short_name, year=tournament_year).first()
        player_id_map = {player.name: player.id for player in Player.query.filter_by(tournament_id=tournament.id).all()}

        # Assegura que a coluna 'Player' é tratada como string
        df['Player'] = df['Player'].astype(str)

        # Extrair o nome do jogador da coluna 'Player' e mapear para player_id
        # O uso de [0] após o .extract() seleciona a primeira coluna do resultado, que contém os nomes extraídos
        df['player_id'] = df['Player'].str.extract(r'^(.*?)\s+\(')[0].map(player_id_map)

        # Removendo linhas com valores NaN em 'player_id'
        df.dropna(subset=['player_id'], inplace=True)

        # Convertendo 'player_id' para int, tratando erros
        df['player_id'] = pd.to_numeric(df['player_id'], downcast='integer', errors='coerce')

    # Retorna o DataFrame ajustado
    return df[['Position', 'player_id']]

def ResultsPositionTournament(file_path, short_name, year):
    # Obtenção das informações do torneio
    tournament = Tournament.query.filter_by(short_name=short_name, year=year).first()
    if not tournament:
        return pd.DataFrame()  # Retornar dataframe vazio se o torneio não for encontrado
    
    # Ler o arquivo CSV e preparar o dataframe
    df = pd.read_csv(file_path, encoding='ISO-8859-1', skiprows=1, names=['Position', 'Player'])
    
    # Mapeamento de nomes de jogadores para player_id
    player_id_map = {player.name: player.id for player in Player.query.filter_by(tournament_id=tournament.id).all()}
    
    # Extrair o nome do jogador e mapear para player_id
    df['player_id'] = df['Player'].str.extract(r'^(.*?)\s+\(')[0].map(player_id_map)
    df.dropna(subset=['player_id'], inplace=True)
    df['player_id'] = pd.to_numeric(df['player_id'], downcast='integer', errors='coerce')
    
    # Mapear player_id para nomes de jogadores
    player_name_map = {v: k for k, v in player_id_map.items()}
    df['name'] = df['player_id'].map(player_name_map)
    
    # Adicionar o tournament_id ao dataframe
    df['tournament_id'] = tournament.id
    
    # Retornar as colunas especificadas incluindo 'player_id'
    return df[['Position', 'name', 'player_id', 'tournament_id']]

# Função para processar e atualizar as rodadas, incluindo a extração de player_ids
def process_and_update_rounds(etapas_torneio, tournament_short_name, tournament_year):
    # Dicionário para armazenar os classificados de cada etapa
    classificados = {}
    # Lista para armazenar as atualizações de cada rodada
    RoundUpdates = []

    # Função interna para extrair os player_ids de um DataFrame
    def extract_player_ids(df):
        return set(df['player_id'])

    for etapa, file_path in etapas_torneio.items():
        # Processa os dados da etapa atual
        df = process_results_data_position(file_path, tournament_short_name, tournament_year)
        # Extrai os player_ids usando a função interna
        player_ids = extract_player_ids(df)
        # Armazena o conjunto de player_ids no dicionário classificados
        classificados[etapa] = player_ids
        # Adiciona a tupla (etapa, conjunto de player_ids) à lista RoundUpdates
        RoundUpdates.append((etapa, player_ids))

    return RoundUpdates

def process_round_results_and_extract_ids(etapa, csv_path, tournament_short_name, tournament_year):
    # Função interna para extrair os player_ids de um DataFrame
    def extract_player_ids(df):
        return set(df['player_id'])

    # Processa os dados da etapa atual
    df = process_results_data_position(csv_path, tournament_short_name, tournament_year)
    # Extrai os player_ids usando a função interna
    player_ids = extract_player_ids(df)

    # Retorna a tupla (etapa, conjunto de player_ids) para a rodada processada
    return (etapa, player_ids)

def update_leaderboard_data(Leaderboard_df):
    with app.app_context():
        current_tournament_id = int(Leaderboard_df['tournament_id'].iloc[0])
        current_rodada = Leaderboard_df['Rodada'].iloc[0]

        try:
            # Deletar registros existentes para a mesma rodada e torneio
            Pontuacoes.query.filter_by(tournament_id=current_tournament_id, rodada=current_rodada).delete()
            db.session.commit()

            # Preparar os objetos Pontuacoes para inserção
            for index, row in Leaderboard_df.fillna(0).iterrows():
                new_record = Pontuacoes(
                    ranking_pp=int(row.get('Ranking PP', 0)),
                    ranking_pg=int(row.get('Ranking PG', 0)),
                    username=row['Participante'],
                    pontos_possiveis=int(row.get('Pontos Possíveis', 0)),
                    pontos_ganhos=int(row.get('Pontos Ganhos', 0)),
                    rodada=row['Rodada'],
                    # data_atualizacao=datetime.utcnow(),
                    data_atualizacao = datetime.now(timezone.utc),
                    tournament_id=int(row['tournament_id'])
                )
                db.session.add(new_record)

            db.session.commit()
            print("Dados de pontuação atualizados com sucesso para a rodada e torneio específicos.")
        except Exception as e:
            db.session.rollback()
            print(f"Ocorreu um erro ao atualizar os dados de pontuação: {e}")

def send_email(subject, recipient, template):
    msg = Message(subject, recipients=[recipient])
    msg.body = template
    mail.send(msg)