import csv
from tennis_app import app
from tennis_app.extensions import db
from tennis_app.models import Player, Tournament

with app.app_context():
    tournament_short_name = 'RIO'
    tournament_year = 2024
    tournament = Tournament.query.filter_by(short_name=tournament_short_name, year=tournament_year).first()
    tournament_id = tournament.id
    players = Player.query.filter_by(tournament_id=tournament_id).all()

    # Formata o nome do arquivo CSV de saída com o nome curto do torneio e o ano
    output_csv_file = f'players_{tournament_short_name}_{tournament_year}.csv'

    # Cria e abre o arquivo CSV para escrita
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Itera sobre os jogadores para escrever suas informações no arquivo com a formatação desejada
        for player in players:
            # Formata a string com nome, país (se disponível) e seed (se disponível)
            player_info = f"{player.name}"
            if player.country:
                player_info += f" ({player.country})"
            if player.seed:
                player_info += f" [{player.seed}]"
            
            # Escreve a linha formatada no arquivo CSV
            writer.writerow([player_info])

if __name__ == '__main__':
    print(f'Arquivo {output_csv_file} gerado com sucesso.')








