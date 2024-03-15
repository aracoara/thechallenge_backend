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
import json




@contextmanager
def session_scope():
    """Fornecer um escopo de transação."""
    try:
        yield
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


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
        tournament = Tournament.query.filter_by(short_name=tournament_short_name, year=tournament_year).first()

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

        return df_picks_por_usuario



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

# Ajuste essas funções para receberem diretamente o dicionário, não uma string
def extract_picks_with_game_id(data, user_id, tournament_id):
    # Mapeamento de position para game_id
    position_to_game_id_map = {
        "QF1": 1, "QF2": 1, "QF3": 2, "QF4": 2,
        "QF5": 3, "QF6": 3, "QF7": 4, "QF8": 4,
        "SF1": 5, "SF2": 5, "SF3": 6, "SF4": 6,
        "F1": 7, "F2": 7, "Champion": 7
    }

    picks_list = []

    # Agora 'data' é assumido como sendo um dicionário diretamente
    rounds = {**data["quartasFinal"], **data["semiFinal"], **data["final"], "Champion": data["campeao"]}

    for position, player_id in rounds.items():
        game_id = position_to_game_id_map.get(position)
        pick = Pick(
            position=position,
            player_id=int(player_id),
            game_id=game_id,
            user_id=user_id,
            tournament_id=tournament_id
        )
        db.session.add(pick)
    
    return picks_list

def process_picks_and_generate_games(data, user_id, tournament_id):
    game_id_to_round_id = {
        1: 5, 2: 5, 3: 5, 4: 5,
        5: 6, 6: 6, 7: 7
    }

    games_data = []

    rounds = {
        **data["quartasFinal"], **data["semiFinal"], **data["final"], "Champion": data["campeao"]
    }

    # Mapeamento de posições para identificar os players de cada jogo e o vencedor
    game_definitions = [
        ('QF1', 'QF2', 'SF1'), ('QF3', 'QF4', 'SF2'), ('QF5', 'QF6', 'SF3'), ('QF7', 'QF8', 'SF4'),
        ('SF1', 'SF2', 'F1'), ('SF3', 'SF4', 'F2'), ('F1', 'F2', 'Champion')
    ]

    for index, (player1_pos, player2_pos, winner_pos) in enumerate(game_definitions, start=1):
        game = {
            "round_id": game_id_to_round_id[index],
            "player1_id": int(rounds[player1_pos]),
            "player2_id": int(rounds[player2_pos]),
            "winner_id": int(rounds[winner_pos]) if winner_pos in rounds else None,
            "user_id": user_id,
            "tournament_id": tournament_id
        }
        games_data.append(game)
    
    return games_data

def get_user_name_by_id(user_id):
    user = User.query.get(user_id)
    return user.username if user else "Unknown User"
def get_player_name_by_id(player_id):
    player = Player.query.get(player_id)
    return player.name if player else "Unknown"