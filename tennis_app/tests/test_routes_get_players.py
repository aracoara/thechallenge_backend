# import sys
# sys.path.append('D:/TENIS/Smash_Picks/SF_app')  # Ajuste para o caminho correto no seu sistema

# from tennis_app.models import Tournament
# from tennis_app import app

# # Define os valores para procurar um torneio existente
# short_name = "AO"  # Substitua pelo nome abreviado do torneio que você deseja encontrar
# year = 2024        # Substitua pelo ano do torneio que você deseja encontrar

# with app.app_context():
#     tournament = Tournament.query.filter_by(short_name=short_name, year=year).first()
#     if tournament:
#         print(f"Torneio encontrado: {tournament.name}, Short Name: {tournament.short_name}, Year: {tournament.year}, Status: {tournament.status}")
#     else:
#         print("Torneio não encontrado.")
