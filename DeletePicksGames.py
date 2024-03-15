from sqlalchemy import create_engine, text

# Certifique-se de que o caminho para o banco de dados esteja correto
DATABASE_URI = 'sqlite:///D:/TENIS/thechallenge_backend/instance/thechallenge.db'

def delete_data_from_tables():
    engine = create_engine(DATABASE_URI)
    
    with engine.begin() as connection:  # O método .begin() garante que a transação seja commitada
        connection.execute(text("DELETE FROM games"))
        print('Data from "games" table deleted.')
        connection.execute(text("DELETE FROM picks"))
        print('Data from "picks" table deleted.')

if __name__ == '__main__':
    delete_data_from_tables()
