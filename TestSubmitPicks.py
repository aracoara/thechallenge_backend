import json

# Dados JSON como string
json_data_str = """
{
  "quartasFinal": { "QF1": "2", "QF2": "18", "QF3": "33", "QF4": "49", "QF5": "65", "QF6": "79", "QF7": "104", "QF8": "119" },
  "semiFinal": { "SF1": "2", "SF2": "49", "SF3": "65", "SF4": "104" },
  "final": { "F1": "2", "F2": "104" },
  "campeao": "2",
  "user_id": 36,
  "tournament_id": 1
}
"""


def extract_picks_with_game_id(data):
    # Mapeamento de position para game_id
    position_to_game_id_map = {
        "QF1": 1, "QF2": 1, "QF3": 2, "QF4": 2,
        "QF5": 3, "QF6": 3, "QF7": 4, "QF8": 4,
        "SF1": 5, "SF2": 5, "SF3": 6, "SF4": 6,
        "F1": 7, "F2": 7, "Champion": 7
    }

    picks_list = []

    # Converter a string JSON em um dicionário
    picks_data = json.loads(data)

    # Processando as partidas por suas fases e adicionando o campeão
    rounds = {**picks_data["quartasFinal"], **picks_data["semiFinal"], **picks_data["final"], "Champion": picks_data["campeao"]}

    for position, player_id in rounds.items():
        game_id = position_to_game_id_map.get(position)
        pick = {
            "position": position,
            "player_id": int(player_id),
            "game_id": game_id,
            "user_id": picks_data["user_id"],
            "tournament_id": picks_data["tournament_id"]
        }
        picks_list.append(pick)

    return picks_list

# Extrair picks incluindo game_id e imprimir
picks_extracted = extract_picks_with_game_id(json_data_str)
for picks in picks_extracted:
    print(picks)

def process_picks_and_generate_games(data_str):
    data = json.loads(data_str)
    
    # Dicionário mapeando game_id para round_id conforme especificado
    game_id_to_round_id = {
        1: 5, 2: 5, 3: 5, 4: 5,
        5: 6, 6: 6, 7: 7
    }
    
    # Lista para armazenar os dados dos jogos processados
    games_data = []

    # Processando os dados de cada rodada do torneio e campeão
    rounds = {
        **data["quartasFinal"], **data["semiFinal"], **data["final"], 
        "Champion": data["campeao"]
    }

    # Função para buscar o player_id pelo seu position
    def get_player_id_by_position(position):
        return int(rounds[position])

    # Gerando a lista de games
    for game_id, round_id in game_id_to_round_id.items():
        game = {
            "game_id": game_id,
            "round_id": round_id,
            "player1_id": None,
            "player2_id": None,
            "winner_id": None,
            "user_id": data["user_id"],
            "tournament_id": data["tournament_id"]
        }
        
        # Atribuindo player1_id, player2_id e winner_id com base nas regras fornecidas
        if game_id <= 4:  # Quartas de Final
            game["player1_id"] = get_player_id_by_position(f"QF{2 * game_id - 1}")
            game["player2_id"] = get_player_id_by_position(f"QF{2 * game_id}")
            game["winner_id"] = get_player_id_by_position(f"SF{game_id}")
        elif game_id <= 6:  # Semi Final
            game["player1_id"] = get_player_id_by_position(f"SF{2 * (game_id - 4) - 1}")
            game["player2_id"] = get_player_id_by_position(f"SF{2 * (game_id - 4)}")
            game["winner_id"] = get_player_id_by_position("F1" if game_id == 5 else "F2")
        else:  # Final
            game["player1_id"] = get_player_id_by_position("F1")
            game["player2_id"] = get_player_id_by_position("F2")
            game["winner_id"] = get_player_id_by_position("Champion")
        
        games_data.append(game)

    return games_data

# Extrair picks, gerar games e imprimir os resultados
games_data = process_picks_and_generate_games(json_data_str)
for game in games_data:
    print(game)