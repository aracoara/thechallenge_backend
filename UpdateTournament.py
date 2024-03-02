from tennis_app.models import Tournament, Player
from tennis_app import app
from tennis_app.extensions import db

def add_or_update_tournaments_in_database(tournament_data):
    with app.app_context():
        # Loop através de cada torneio fornecido no tournament_data
        for tournament_info in tournament_data:
            # Tenta encontrar um torneio existente pelo nome
            existing_tournament = Tournament.query.filter_by(name=tournament_info['name']).first()

            if existing_tournament:
                # Se o torneio existir, atualiza seus atributos
                existing_tournament.short_name = tournament_info['short_name']
                existing_tournament.year = tournament_info['year']
                existing_tournament.status = tournament_info['status']
            else:
                # Se não existir, cria um novo torneio com os dados fornecidos
                new_tournament = Tournament(**tournament_info)
                db.session.add(new_tournament)

        # Commit as alterações na sessão do banco de dados
        db.session.commit()

## Status possíveis do torneio: Open, On Progress, Closed
tournament_data = [
    {"name": "Rio Open", "short_name": "RIO", "year": 2024, "status": "Open"},
    {"name": "Australian Open", "short_name": "AO", "year": 2024, "status": "On Progress"},
    {"name": "Wimbledon", "short_name": "WB", "year": 2023, "status": "Closed"},
]

if __name__ == '__main__':
    add_or_update_tournaments_in_database(tournament_data)
    print("Torneios adicionados ou atualizados com sucesso.")
