from tennis_app.extensions import db  # Importe a instância do SQLAlchemy
from tennis_app.models import Tournament  # Importe o modelo Tournament

# # Tentativa de criar um torneio com um status válido
# torneio_valido = Tournament(name="Torneio Teste", short_name="TT", year=2021, status="Open")
# db.session.add(torneio_valido)
# db.session.commit()  # Isso deve funcionar sem problemas

# Tentativa de criar um torneio com um status inválido
try:
    torneio_invalido = Tournament(name="Torneio Inválido", short_name="TI", year=2021, status="Invalido")
    db.session.add(torneio_invalido)
    db.session.commit()
except ValueError as e:
    print(e)  # Deve imprimir a mensagem de erro do validador
